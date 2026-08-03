"""Reporting and sanitization."""

import csv
import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import List, Dict, Any

from agent_eval.config import NormalizedResult


class ReportSanitizer:
    """Sanitizes results for publication."""

    PATTERNS = [
        (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", "[EMAIL]"),
        (r"ghp_[A-Za-z0-9]{36}", "[GITHUB_TOKEN]"),
        (r"sk-[A-Za-z0-9]{48}", "[API_KEY]"),
        (r"/Users/[^/\s]+", "[HOME]"),
        (r"/home/[^/\s]+", "[HOME]"),
        (r"C:\\Users\\[^\\]+", "[HOME]"),
        (r"https://github\.com/[^/]+/[^/]+", "[REPO_URL]"),
    ]

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Redact sensitive patterns from text."""
        for pattern, replacement in ReportSanitizer.PATTERNS:
            text = re.sub(pattern, replacement, text)
        return text

    @staticmethod
    def sanitize_result(result: NormalizedResult) -> Dict[str, Any]:
        """Sanitize a single result."""
        data = asdict(result)

        if "errors" in data:
            data["errors"] = [ReportSanitizer.sanitize_text(e) for e in data["errors"]]
        if "safety_flags" in data:
            data["safety_flags"] = [ReportSanitizer.sanitize_text(f) for f in data["safety_flags"]]

        data.pop("trajectory_hash", None)
        data.pop("trajectory_assertions", None)

        return data


class ReportGenerator:
    """Generates reports in multiple formats."""

    def __init__(self, results: List[NormalizedResult]):
        """Initialize with results."""
        self.results = results
        self.sanitizer = ReportSanitizer()

    def to_json(self, output_path: Path, sanitize: bool = True) -> None:
        """Export results as JSON."""
        data = [self.sanitizer.sanitize_result(r) if sanitize else asdict(r) for r in self.results]
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

    def to_csv(self, output_path: Path, sanitize: bool = True) -> None:
        """Export results as CSV."""
        if not self.results:
            return

        data = [self.sanitizer.sanitize_result(r) if sanitize else asdict(r) for r in self.results]

        fieldnames = list(data[0].keys())
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def to_markdown(self, output_path: Path, sanitize: bool = True) -> None:
        """Export results as Markdown."""
        _ = sanitize
        lines = [
            "# Evaluation Results",
            "",
            f"**Total Results:** {len(self.results)}",
            "",
            "## Summary",
            "",
        ]

        accepted = sum(1 for r in self.results if r.is_accepted())
        lines.append(
            f"- **Accepted:** {accepted}/{len(self.results)} ({accepted / len(self.results) * 100:.1f}%)"
        )

        total_cost = sum(r.delegated_agent_cost_usd for r in self.results)
        lines.append(f"- **Total Cost:** ${total_cost:.2f}")

        avg_latency = (
            sum(r.latency_seconds for r in self.results) / len(self.results) if self.results else 0
        )
        lines.append(f"- **Average Latency:** {avg_latency:.1f}s")

        lines.extend(["", "## Results by Task", ""])

        by_task: Dict[str, List[NormalizedResult]] = {}
        for result in self.results:
            if result.task_id not in by_task:
                by_task[result.task_id] = []
            by_task[result.task_id].append(result)

        for task_id, task_results in sorted(by_task.items()):
            task_accepted = sum(1 for r in task_results if r.is_accepted())
            lines.append(f"### {task_id}")
            lines.append(f"- **Acceptance:** {task_accepted}/{len(task_results)}")
            lines.append("")

        with open(output_path, "w") as f:
            f.write("\n".join(lines))
