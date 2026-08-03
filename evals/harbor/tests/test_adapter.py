"""Tests for OpenCode adapter."""

import json

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
