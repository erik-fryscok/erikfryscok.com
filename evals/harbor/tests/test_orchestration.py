"""Tests for orchestration."""

import json
import tempfile
from pathlib import Path

import agent_eval.orchestration as orchestration_module

from agent_eval.orchestration import HarborOrchestrator
from agent_eval.config import Profile, AgentRole


def test_orchestrator_initialization():
    """Orchestrator initializes with jobs directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = HarborOrchestrator(Path(tmpdir))
        assert orchestrator.jobs_dir.exists()


def test_orchestrator_creates_job_directory():
    """Orchestrator creates job directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = HarborOrchestrator(Path(tmpdir))
        profile = Profile(
            name="baseline",
            agent_model_routing={AgentRole.CHAT: "claude-haiku-4.5"},
            prompt_digest={AgentRole.CHAT: "abc123"},
            skill_digest="def456",
            variant="baseline",
            context_limit=32000,
            mcp_mode="mock",
            permissions_digest="ghi789",
            provider_endpoint=None,
            source_commit="abc1234567890",
        )

        assert orchestrator.jobs_dir.exists()
        assert profile.name == "baseline"


def test_orchestrator_run_and_load_job_results(monkeypatch):
    class DummyAdapter:
        def __init__(self, profile):
            self.profile = profile

        def run_agent(self, agent, prompt, task_context, timeout_seconds=3600):
            _ = (agent, prompt, task_context, timeout_seconds)
            return {
                "functional_correctness": 1.0,
                "repository_checks": 1.0,
                "scope_compliance": 1.0,
                "output_contract": 1.0,
                "tool_behavior": 1.0,
                "permission_compliance": 1.0,
                "safety": 1.0,
                "errors": [],
                "safety_flags": [],
                "tokens": {"input": 10, "output": 5},
                "cost_usd": 0.01,
                "latency_seconds": 0.5,
                "hash": "abc",
            }

    monkeypatch.setattr(orchestration_module, "OpenCodeAdapter", DummyAdapter)

    with tempfile.TemporaryDirectory() as tmpdir:
        orchestrator = HarborOrchestrator(Path(tmpdir))
        profile = Profile(
            name="baseline",
            agent_model_routing={AgentRole.CHAT: "claude-haiku-4.5"},
            prompt_digest={AgentRole.CHAT: "abc123"},
            skill_digest="def456",
            variant="baseline",
            context_limit=32000,
            mcp_mode="mock",
            permissions_digest="ghi789",
            provider_endpoint=None,
            source_commit="abc1234567890",
        )
        tasks = [
            {
                "id": "chat-task",
                "agent": "chat",
                "fixture": "smoke/chat-task",
                "suite": "smoke",
                "prompt": "hello",
            }
        ]
        job_id = orchestrator.run_job(profile, "smoke", tasks, attempt=1)
        results = orchestrator.load_job_results(job_id)

        assert len(results) == 1
        assert results[0].task_id == "chat-task"
        assert results[0].tokens_input == 10

        metadata_path = Path(tmpdir) / job_id / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        assert metadata["suite"] == "smoke"
