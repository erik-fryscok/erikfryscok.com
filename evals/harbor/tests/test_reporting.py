"""Tests for reporting."""

import json
import tempfile
from pathlib import Path

from agent_eval.reporting import ReportSanitizer, ReportGenerator
from agent_eval.config import NormalizedResult


def test_sanitizer_redacts_email():
    """Sanitizer redacts email addresses."""
    text = "Contact me at test@example.com"
    sanitized = ReportSanitizer.sanitize_text(text)
    assert "test@example.com" not in sanitized
    assert "[EMAIL]" in sanitized


def test_sanitizer_redacts_github_token():
    """Sanitizer redacts GitHub tokens."""
    text = "Token: ghp_123456789012345678901234567890123456"
    sanitized = ReportSanitizer.sanitize_text(text)
    assert "ghp_" not in sanitized
    assert "[GITHUB_TOKEN]" in sanitized


def test_sanitizer_redacts_home_path():
    """Sanitizer redacts home directory paths."""
    text = "File at /Users/erik/project/file.txt"
    sanitized = ReportSanitizer.sanitize_text(text)
    assert "/Users/erik" not in sanitized
    assert "[HOME]" in sanitized


def test_report_generator_json():
    """Report generator exports JSON."""
    results = [
        NormalizedResult(
            job_id="job-1",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="smoke",
            task_id="task-1",
            attempt=1,
            functional_correctness=1.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "results.json"
        generator = ReportGenerator(results)
        generator.to_json(output_path)

        assert output_path.exists()
        with open(output_path) as f:
            data = json.load(f)
        assert len(data) == 1


def test_report_generator_csv():
    """Report generator exports CSV."""
    results = [
        NormalizedResult(
            job_id="job-1",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="smoke",
            task_id="task-1",
            attempt=1,
            functional_correctness=1.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "results.csv"
        generator = ReportGenerator(results)
        generator.to_csv(output_path)

        assert output_path.exists()
