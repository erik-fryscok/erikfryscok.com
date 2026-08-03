"""Job orchestration and matrix execution."""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import asdict

from agent_eval.config import Profile, NormalizedResult, AgentRole
from agent_eval.adapter import OpenCodeAdapter


class HarborOrchestrator:
    """Orchestrates Harbor job execution."""

    def __init__(self, jobs_dir: Path):
        """Initialize orchestrator with jobs directory."""
        self.jobs_dir = Path(jobs_dir)
        self.jobs_dir.mkdir(parents=True, exist_ok=True)

    def run_job(
        self,
        profile: Profile,
        suite_name: str,
        suite_tasks: List[Dict[str, Any]],
        attempt: int = 1,
    ) -> str:
        """
        Run a single Harbor job.

        Args:
            profile: Agent/model routing profile
            suite_name: Suite name (smoke, development, holdout, workflow)
            suite_tasks: List of task definitions
            attempt: Attempt number

        Returns:
            Job ID
        """
        job_id = f"{suite_name}-{profile.name}-{attempt}-{uuid.uuid4().hex[:8]}"
        job_dir = self.jobs_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        adapter = OpenCodeAdapter(profile)

        results = []
        for task in suite_tasks:
            result = self._run_task(adapter, task, job_dir)
            results.append(result)

        results_file = job_dir / "results.jsonl"
        with open(results_file, "w") as f:
            for result in results:
                f.write(json.dumps(asdict(result)) + "\n")

        metadata = {
            "job_id": job_id,
            "profile_hash": profile.hash(),
            "suite": suite_name,
            "attempt": attempt,
            "task_count": len(suite_tasks),
            "results_file": str(results_file),
        }
        metadata_file = job_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        return job_id

    def _run_task(
        self,
        adapter: OpenCodeAdapter,
        task: Dict[str, Any],
        job_dir: Path,
    ) -> NormalizedResult:
        """Run a single task and return normalized result."""
        task_id = task["id"]
        agent = AgentRole(task["agent"])

        fixture_path = Path(task.get("fixture_path", f"tasks/fixtures/{task['fixture']}"))

        trajectory = adapter.run_agent(
            agent=agent,
            prompt=task.get("prompt", ""),
            task_context={"working_dir": str(fixture_path)},
        )

        result = NormalizedResult(
            job_id=str(job_dir.name),
            profile_hash=adapter.profile.hash(),
            experiment_hash="",
            suite=task.get("suite", "unknown"),
            task_id=task_id,
            attempt=1,
            functional_correctness=trajectory.get("functional_correctness", 0.0),
            repository_checks=trajectory.get("repository_checks", 0.0),
            scope_compliance=trajectory.get("scope_compliance", 0.0),
            output_contract=trajectory.get("output_contract", 0.0),
            tool_behavior=trajectory.get("tool_behavior", 0.0),
            permission_compliance=trajectory.get("permission_compliance", 0.0),
            safety=trajectory.get("safety", 0.0),
            errors=trajectory.get("errors", []),
            safety_flags=trajectory.get("safety_flags", []),
            tokens_input=trajectory.get("tokens", {}).get("input", 0),
            tokens_output=trajectory.get("tokens", {}).get("output", 0),
            delegated_agent_cost_usd=trajectory.get("cost_usd", 0.0),
            latency_seconds=trajectory.get("latency_seconds", 0.0),
            trajectory_hash=trajectory.get("hash", ""),
        )

        return result

    def load_job_results(self, job_id: str) -> List[NormalizedResult]:
        """Load results from a completed job."""
        job_dir = self.jobs_dir / job_id
        results_file = job_dir / "results.jsonl"

        results = []
        with open(results_file, "r") as f:
            for line in f:
                data = json.loads(line)
                result = NormalizedResult(**data)
                results.append(result)

        return results
