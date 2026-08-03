"""Extended OpenCode adapter for Harbor evaluation."""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, List

from agent_eval.config import Profile, AgentRole


class OpenCodeAdapter:
    """Adapter for running OpenCode agents with explicit routing and isolated environment."""

    def __init__(self, profile: Profile, opencode_bin: str = "opencode"):
        """Initialize adapter with profile."""
        self.profile = profile
        self.opencode_bin = opencode_bin

    def run_agent(
        self,
        agent: AgentRole,
        prompt: str,
        task_context: Dict[str, Any],
        timeout_seconds: int = 3600,
    ) -> Dict[str, Any]:
        """
        Run an OpenCode agent with explicit routing.

        Args:
            agent: Agent role to invoke
            prompt: User prompt/task
            task_context: Task-specific context (files, fixtures, etc.)
            timeout_seconds: Execution timeout

        Returns:
            ATIF trajectory dict with events, tokens, cost, and outcome
        """
        _ = prompt
        model = self.profile.agent_model_routing.get(agent)
        if not model:
            raise ValueError(f"No model routing for agent {agent}")

        env = self._build_isolated_env(agent, model)
        cmd = self._build_command(agent, model, task_context)

        try:
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=task_context.get("working_dir", "."),
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Execution exceeded {timeout_seconds}s",
                "events": [],
                "tokens": {"input": 0, "output": 0},
                "cost_usd": 0.0,
            }

        try:
            trajectory = json.loads(result.stdout)
        except json.JSONDecodeError:
            trajectory = {
                "status": "error",
                "error": f"Invalid ATIF output: {result.stderr}",
                "events": [],
                "tokens": {"input": 0, "output": 0},
                "cost_usd": 0.0,
            }

        return trajectory

    def _build_isolated_env(self, agent: AgentRole, model: str) -> Dict[str, str]:
        """Build isolated environment with XDG overrides and config injection."""
        env = os.environ.copy()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            env["XDG_CONFIG_HOME"] = str(tmpdir_path / "config")
            env["XDG_DATA_HOME"] = str(tmpdir_path / "data")
            env["XDG_CACHE_HOME"] = str(tmpdir_path / "cache")

        config_content = self._build_config_content(agent, model)
        env["OPENCODE_CONFIG_CONTENT"] = config_content

        env.pop("GITHUB_TOKEN", None)
        env.pop("GITHUB_MCP_TOKEN", None)
        env.pop("HOME", None)

        return env

    def _build_config_content(self, agent: AgentRole, model: str) -> str:
        """Build OpenCode config JSON for this agent."""
        config = {
            "default_agent": agent.value,
            "enabled_providers": ["anthropic", "openai", "opencode", "lmstudio"],
            "provider": {
                "lmstudio": {
                    "models": {
                        "qwen/qwen3.5-9b": {"name": "Qwen3.5 9B"},
                        "openai/gpt-oss-120b": {"name": "GPT-OSS 120B"},
                        "qwen/qwen3.6-35b-a3b": {"name": "Qwen3.6 35B A3B"},
                        "openai/gpt-oss-20b": {"name": "GPT-OSS 20B"},
                    }
                }
            },
            "subagent_depth": 1,
            "mcp": {
                "github_read": {
                    "type": "mock" if self.profile.mcp_mode == "mock" else "remote",
                    "enabled": self.profile.mcp_mode != "disabled",
                },
                "github_publish": {
                    "type": "mock" if self.profile.mcp_mode == "mock" else "remote",
                    "enabled": self.profile.mcp_mode != "disabled",
                },
                "github_issues": {
                    "type": "mock" if self.profile.mcp_mode == "mock" else "remote",
                    "enabled": self.profile.mcp_mode != "disabled",
                },
            },
            "permission": {
                "github_*": "deny",
                "github_issues_*": "deny",
            },
            "agent": {
                agent.value: {
                    "temperature": 0.1 if agent == AgentRole.PLAN else 0.2,
                    "model": model,
                }
            },
        }
        return json.dumps(config)

    def _build_command(
        self, agent: AgentRole, model: str, task_context: Dict[str, Any]
    ) -> List[str]:
        """Build OpenCode CLI command."""
        cmd = [
            self.opencode_bin,
            "--agent",
            agent.value,
            "--model",
            model,
            "--variant",
            self.profile.variant,
            "--format",
            "json",
        ]

        if "prompt_file" in task_context:
            cmd.extend(["--prompt-file", task_context["prompt_file"]])

        return cmd
