"""Tests for orchestration."""

import tempfile
from pathlib import Path

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
