"""Tests for OpenCode adapter."""

import json
import subprocess
from types import SimpleNamespace

from agent_eval.adapter import OpenCodeAdapter
from agent_eval.config import Profile, AgentRole


def test_adapter_initialization():
    """Adapter initializes with profile."""
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
    adapter = OpenCodeAdapter(profile)
    assert adapter.profile == profile


def test_adapter_isolated_env():
    """Adapter builds isolated environment."""
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
    adapter = OpenCodeAdapter(profile)
    env = adapter._build_isolated_env(AgentRole.CHAT, "claude-haiku-4.5")

    assert "XDG_CONFIG_HOME" in env
    assert "XDG_DATA_HOME" in env
    assert "XDG_CACHE_HOME" in env
    assert "OPENCODE_CONFIG_CONTENT" in env
    assert "GITHUB_TOKEN" not in env


def test_adapter_config_content():
    """Adapter builds valid OpenCode config."""
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
    adapter = OpenCodeAdapter(profile)
    config_str = adapter._build_config_content(AgentRole.CHAT, "claude-haiku-4.5")

    config = json.loads(config_str)
    assert config["default_agent"] == "chat"
    assert config["agent"]["chat"]["model"] == "claude-haiku-4.5"


def test_adapter_run_agent_no_model_route():
    profile = Profile(
        name="baseline",
        agent_model_routing={},
        prompt_digest={AgentRole.CHAT: "abc123"},
        skill_digest="def456",
        variant="baseline",
        context_limit=32000,
        mcp_mode="mock",
        permissions_digest="ghi789",
        provider_endpoint=None,
        source_commit="abc1234567890",
    )
    adapter = OpenCodeAdapter(profile)
    try:
        adapter.run_agent(AgentRole.CHAT, "p", {"working_dir": "."})
    except ValueError as exc:
        assert "No model routing" in str(exc)
    else:
        assert False, "expected ValueError"


def test_adapter_run_agent_timeout(monkeypatch):
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
    adapter = OpenCodeAdapter(profile)

    def raise_timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="opencode", timeout=1)

    monkeypatch.setattr(subprocess, "run", raise_timeout)
    result = adapter.run_agent(AgentRole.CHAT, "p", {"working_dir": "."}, timeout_seconds=1)
    assert result["status"] == "timeout"


def test_adapter_run_agent_invalid_json(monkeypatch):
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
    adapter = OpenCodeAdapter(profile)

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(stdout="not-json", stderr="bad"),
    )
    result = adapter.run_agent(AgentRole.CHAT, "p", {"working_dir": "."})
    assert result["status"] == "error"


def test_adapter_build_command_includes_prompt_file():
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
    adapter = OpenCodeAdapter(profile)
    cmd = adapter._build_command(
        AgentRole.CHAT,
        "claude-haiku-4.5",
        {"prompt_file": "task.txt"},
    )
    assert "--prompt-file" in cmd
