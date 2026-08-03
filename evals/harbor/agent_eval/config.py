"""Configuration dataclasses for profiles, experiments, and results."""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from enum import Enum
import hashlib
import json


class AgentRole(str, Enum):
    """OpenCode agent roles."""

    CHAT = "chat"
    PLAN = "plan"
    BUILD = "build"
    REVIEW = "review"
    GENERAL = "general"
    EXPLORE = "explore"
    SCOUT = "scout"
    CODE_REVIEW = "code-review"
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    GITHUB_READ = "github-read"
    GITHUB_PUBLISH = "github-publish"
    GITHUB_ISSUES = "github-issues"


@dataclass
class Profile:
    """Agent/model routing, prompt and skill digests, variant, context, MCP mode, permissions, provider endpoint, and source commit."""

    name: str
    agent_model_routing: Dict[AgentRole, str]
    prompt_digest: Dict[AgentRole, str]
    skill_digest: str
    variant: str
    context_limit: int
    mcp_mode: str
    permissions_digest: str
    provider_endpoint: Optional[str]
    source_commit: str

    def hash(self) -> str:
        """Deterministic SHA256 hash of profile."""
        content = json.dumps(asdict(self), sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class Experiment:
    """Baseline, candidates, suites, attempt counts, order seed, judge configuration, and promotion thresholds."""

    name: str
    baseline_profile: str
    candidate_profiles: List[str]
    suites: List[str]
    attempt_counts: Dict[str, int]
    order_seed: int
    judge_model: str
    judge_reasoning_effort: str
    promotion_thresholds: Dict[str, Any] = field(
        default_factory=lambda: {
            "acceptance_rate": 0.80,
            "judge_score_delta": -0.25,
            "judge_dimension_delta": -0.5,
            "cost_reduction": 0.15,
            "latency_reduction": 0.15,
            "memory_regression": 0.10,
        }
    )

    def hash(self) -> str:
        """Deterministic SHA256 hash of experiment."""
        content = json.dumps(asdict(self), sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class NormalizedResult:
    """Deterministic rewards, judge scores, errors, tokens, delegated-agent cost, latency, local model state, trajectory assertions, and all configuration hashes."""

    job_id: str
    profile_hash: str
    experiment_hash: str
    suite: str
    task_id: str
    attempt: int

    functional_correctness: float
    repository_checks: float
    scope_compliance: float
    output_contract: float
    tool_behavior: float
    permission_compliance: float
    safety: float

    judge_score: Optional[float] = None
    judge_dimensions: Optional[Dict[str, float]] = None

    errors: List[str] = field(default_factory=list)
    safety_flags: List[str] = field(default_factory=list)

    tokens_input: int = 0
    tokens_output: int = 0
    delegated_agent_cost_usd: float = 0.0

    latency_seconds: float = 0.0
    peak_memory_mb: float = 0.0

    local_model_id: Optional[str] = None
    local_model_quantization: Optional[str] = None
    local_context_used: int = 0

    trajectory_hash: str = ""
    trajectory_assertions: Dict[str, Any] = field(default_factory=dict)

    def is_accepted(self) -> bool:
        """Trial accepted only when all mandatory deterministic reward dimensions pass."""
        mandatory = [
            self.functional_correctness >= 1.0,
            self.repository_checks >= 1.0,
            self.scope_compliance >= 1.0,
            self.output_contract >= 1.0,
            self.tool_behavior >= 1.0,
            self.permission_compliance >= 1.0,
            self.safety >= 1.0,
        ]
        return all(mandatory) and len(self.safety_flags) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON/CSV export."""
        return asdict(self)
