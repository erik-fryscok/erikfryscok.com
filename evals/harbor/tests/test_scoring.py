"""Tests for scoring logic."""

import pytest

from agent_eval.scoring import (
    evaluate_acceptance,
    evaluate_profile_smoke_baseline,
    calculate_cost_per_success,
)
from agent_eval.config import NormalizedResult


def test_evaluate_acceptance_all_pass():
    """Result is accepted when all dimensions pass."""
    result = NormalizedResult(
        job_id="job-1",
        profile_hash="abc123",
        experiment_hash="def456",
        suite="smoke",
        task_id="chat-task",
        attempt=1,
        functional_correctness=1.0,
        repository_checks=1.0,
        scope_compliance=1.0,
        output_contract=1.0,
        tool_behavior=1.0,
        permission_compliance=1.0,
        safety=1.0,
    )
    scoring = evaluate_acceptance(result)
    assert scoring.is_accepted is True
    assert len(scoring.mandatory_failures) == 0


def test_evaluate_acceptance_functional_failure():
    """Result is rejected when functional correctness fails."""
    result = NormalizedResult(
        job_id="job-1",
        profile_hash="abc123",
        experiment_hash="def456",
        suite="smoke",
        task_id="chat-task",
        attempt=1,
        functional_correctness=0.0,
        repository_checks=1.0,
        scope_compliance=1.0,
        output_contract=1.0,
        tool_behavior=1.0,
        permission_compliance=1.0,
        safety=1.0,
    )
    scoring = evaluate_acceptance(result)
    assert scoring.is_accepted is False
    assert "functional_correctness" in scoring.mandatory_failures


def test_evaluate_acceptance_safety_flag():
    """Result is rejected when safety flag present."""
    result = NormalizedResult(
        job_id="job-1",
        profile_hash="abc123",
        experiment_hash="def456",
        suite="smoke",
        task_id="chat-task",
        attempt=1,
        functional_correctness=1.0,
        repository_checks=1.0,
        scope_compliance=1.0,
        output_contract=1.0,
        tool_behavior=1.0,
        permission_compliance=1.0,
        safety=1.0,
        safety_flags=["credential-leak"],
    )
    scoring = evaluate_acceptance(result)
    assert scoring.is_accepted is False


def test_evaluate_smoke_baseline_all_pass():
    """Smoke baseline passes when all 13 tasks pass."""
    results = [
        NormalizedResult(
            job_id=f"job-{i}",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="smoke",
            task_id=f"task-{i}",
            attempt=1,
            functional_correctness=1.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
        )
        for i in range(13)
    ]
    scoring = evaluate_profile_smoke_baseline(results)
    assert scoring["passed"] is True
    assert scoring["accepted_count"] == 13


def test_evaluate_smoke_baseline_partial_pass():
    """Smoke baseline fails when not all 13 tasks pass."""
    results = [
        NormalizedResult(
            job_id=f"job-{i}",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="smoke",
            task_id=f"task-{i}",
            attempt=1,
            functional_correctness=1.0 if i < 12 else 0.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
        )
        for i in range(13)
    ]
    scoring = evaluate_profile_smoke_baseline(results)
    assert scoring["passed"] is False
    assert scoring["accepted_count"] == 12


def test_calculate_cost_per_success():
    """Cost per success calculated correctly."""
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
            delegated_agent_cost_usd=0.10,
        ),
        NormalizedResult(
            job_id="job-2",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="smoke",
            task_id="task-2",
            attempt=1,
            functional_correctness=1.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
            delegated_agent_cost_usd=0.20,
        ),
    ]
    cost = calculate_cost_per_success(results)
    assert cost == pytest.approx(0.15)
