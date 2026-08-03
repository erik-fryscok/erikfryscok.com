"""Tests for config dataclasses."""

from agent_eval.config import Profile, Experiment, NormalizedResult, AgentRole


def test_profile_hash_deterministic():
    """Profile hash is deterministic."""
    p1 = Profile(
        name="baseline",
        agent_model_routing={AgentRole.CHAT: "claude-haiku-4.5"},
        prompt_digest={AgentRole.CHAT: "abc123"},
        skill_digest="def456",
        variant="baseline",
        context_limit=32000,
        mcp_mode="production",
        permissions_digest="ghi789",
        provider_endpoint=None,
        source_commit="abc1234567890",
    )
    p2 = Profile(
        name="baseline",
        agent_model_routing={AgentRole.CHAT: "claude-haiku-4.5"},
        prompt_digest={AgentRole.CHAT: "abc123"},
        skill_digest="def456",
        variant="baseline",
        context_limit=32000,
        mcp_mode="production",
        permissions_digest="ghi789",
        provider_endpoint=None,
        source_commit="abc1234567890",
    )
    assert p1.hash() == p2.hash()


def test_profile_hash_changes_with_model():
    """Profile hash changes when model changes."""
    p1 = Profile(
        name="baseline",
        agent_model_routing={AgentRole.CHAT: "claude-haiku-4.5"},
        prompt_digest={AgentRole.CHAT: "abc123"},
        skill_digest="def456",
        variant="baseline",
        context_limit=32000,
        mcp_mode="production",
        permissions_digest="ghi789",
        provider_endpoint=None,
        source_commit="abc1234567890",
    )
    p2 = Profile(
        name="baseline",
        agent_model_routing={AgentRole.CHAT: "gpt-5.4-nano"},
        prompt_digest={AgentRole.CHAT: "abc123"},
        skill_digest="def456",
        variant="baseline",
        context_limit=32000,
        mcp_mode="production",
        permissions_digest="ghi789",
        provider_endpoint=None,
        source_commit="abc1234567890",
    )
    assert p1.hash() != p2.hash()


def test_experiment_hash_deterministic():
    """Experiment hash is deterministic."""
    e1 = Experiment(
        name="baseline",
        baseline_profile="baseline",
        candidate_profiles=[],
        suites=["smoke"],
        attempt_counts={"smoke": 1},
        order_seed=42,
        judge_model="opencode/gpt-5.6-sol",
        judge_reasoning_effort="high",
    )
    e2 = Experiment(
        name="baseline",
        baseline_profile="baseline",
        candidate_profiles=[],
        suites=["smoke"],
        attempt_counts={"smoke": 1},
        order_seed=42,
        judge_model="opencode/gpt-5.6-sol",
        judge_reasoning_effort="high",
    )
    assert e1.hash() == e2.hash()


def test_normalized_result_accepted():
    """Result is accepted when all mandatory dimensions pass."""
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
    assert result.is_accepted() is True


def test_normalized_result_rejected_on_safety_flag():
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
    assert result.is_accepted() is False


def test_normalized_result_rejected_on_dimension():
    """Result is rejected when mandatory dimension fails."""
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
    assert result.is_accepted() is False
