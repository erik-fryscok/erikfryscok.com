"""Tests for scoring logic."""

import pytest

from agent_eval.scoring import (
    evaluate_acceptance,
    evaluate_profile_smoke_baseline,
    evaluate_development_candidate,
    evaluate_holdout_candidate,
    calculate_cost_per_success,
    calculate_latency_per_success,
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


def test_calculate_cost_per_success_inf_when_no_success():
    results = [
        NormalizedResult(
            job_id="job-1",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="smoke",
            task_id="task-1",
            attempt=1,
            functional_correctness=0.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
            delegated_agent_cost_usd=0.10,
        )
    ]
    assert calculate_cost_per_success(results) == float("inf")


def test_calculate_latency_per_success():
    results = []
    for i, lat in enumerate([3.0, 1.0, 2.0]):
        results.append(
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
                latency_seconds=lat,
            )
        )
    assert calculate_latency_per_success(results) == 2.0


def test_evaluate_development_candidate_passes():
    baseline_results = []
    candidate_results = []
    for task_id in ["a", "b"]:
        for attempt in range(3):
            baseline_results.append(
                NormalizedResult(
                    job_id=f"b-{task_id}-{attempt}",
                    profile_hash="abc123",
                    experiment_hash="def456",
                    suite="development",
                    task_id=task_id,
                    attempt=attempt + 1,
                    functional_correctness=1.0,
                    repository_checks=1.0,
                    scope_compliance=1.0,
                    output_contract=1.0,
                    tool_behavior=1.0,
                    permission_compliance=1.0,
                    safety=1.0,
                )
            )
            candidate_results.append(
                NormalizedResult(
                    job_id=f"c-{task_id}-{attempt}",
                    profile_hash="abc123",
                    experiment_hash="def456",
                    suite="development",
                    task_id=task_id,
                    attempt=attempt + 1,
                    functional_correctness=1.0,
                    repository_checks=1.0,
                    scope_compliance=1.0,
                    output_contract=1.0,
                    tool_behavior=1.0,
                    permission_compliance=1.0,
                    safety=1.0,
                )
            )
    result = evaluate_development_candidate(candidate_results, baseline_results)
    assert result["passed"] is True


def test_evaluate_development_candidate_fails_on_zero_three():
    baseline = [
        NormalizedResult(
            job_id="b-1",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="development",
            task_id="task-a",
            attempt=1,
            functional_correctness=1.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
        )
    ]
    candidate = [
        NormalizedResult(
            job_id=f"c-{i}",
            profile_hash="abc123",
            experiment_hash="def456",
            suite="development",
            task_id="task-a",
            attempt=i + 1,
            functional_correctness=0.0,
            repository_checks=1.0,
            scope_compliance=1.0,
            output_contract=1.0,
            tool_behavior=1.0,
            permission_compliance=1.0,
            safety=1.0,
        )
        for i in range(3)
    ]
    result = evaluate_development_candidate(candidate, baseline)
    assert result["passed"] is False
    assert "zero_three_tasks" in result


def test_evaluate_holdout_candidate_paths():
    baseline = []
    candidate = []
    for attempt in range(5):
        baseline.append(
            NormalizedResult(
                job_id=f"b-{attempt}",
                profile_hash="abc123",
                experiment_hash="def456",
                suite="holdout",
                task_id="task-a",
                attempt=attempt + 1,
                functional_correctness=1.0,
                repository_checks=1.0,
                scope_compliance=1.0,
                output_contract=1.0,
                tool_behavior=1.0,
                permission_compliance=1.0,
                safety=1.0,
            )
        )
        candidate.append(
            NormalizedResult(
                job_id=f"c-{attempt}",
                profile_hash="abc123",
                experiment_hash="def456",
                suite="holdout",
                task_id="task-a",
                attempt=attempt + 1,
                functional_correctness=1.0,
                repository_checks=1.0,
                scope_compliance=1.0,
                output_contract=1.0,
                tool_behavior=1.0,
                permission_compliance=1.0,
                safety=1.0,
            )
        )
    ok = evaluate_holdout_candidate(candidate, baseline)
    assert ok["passed"] is True

    bad_acceptance = evaluate_holdout_candidate(candidate[:3], baseline)
    assert bad_acceptance["passed"] is False
