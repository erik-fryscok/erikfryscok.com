# Harbor Evaluation Harness

Reproducible evaluation of 13 OpenCode agents across 24 deterministic tasks.

## Quick Start

### Prerequisites

- Python 3.12–3.14
- `uv`
- OpenCode CLI 1.18.9 (installed externally)

Install and verify OpenCode CLI:

```bash
opencode --version
```

Expected output includes `1.18.9`.

1. Install dependencies: `uv sync --all-extras`
2. Copy `.env.example` to `.env` and set `ERIKFRYSCOK_HARBOR_JOBS_DIR`
3. Run preflight checks: `agent-eval preflight`
4. Run smoke baseline: `agent-eval run --suite smoke --profile baseline`

## CLI Reference

- `validate` — Check schemas, version pins, task layout, hashes, privacy rules
- `preflight` — Verify Docker, credentials, model availability, LM Studio connectivity
- `oracle --suite <name|all>` — Prove every reference solution passes
- `run --suite <name> --profile <id>` — Launch one Harbor job
- `matrix --experiment <file>` — Run paired baseline/candidate jobs
- `compare --baseline <job> --candidate <job>` — Normalize and evaluate promotion gates
- `sanitize-report --experiment <id>` — Create publication-safe output

## Documentation

- [Setup](docs/setup.md) — Installation, environment, LM Studio preflight
- [Task Authoring](docs/task-authoring.md) — Fixture creation, verifier design
- [Prompt Experimentation](docs/prompt-experimentation.md) — Candidate creation, hypothesis recording
- [Result Interpretation](docs/result-interpretation.md) — Scoring rules, promotion gates
- [Privacy](docs/privacy.md) — Sanitization, trajectory handling, credential isolation
- [Troubleshooting](docs/troubleshooting.md) — Common issues, networking, container access

## Architecture

- **Adapter** (`adapter.py`) — Extended OpenCode adapter with explicit agent/model/variant routing
- **Config** (`config.py`) — Profile, Experiment, NormalizedResult dataclasses
- **Scoring** (`scoring.py`) — Acceptance criteria and promotion gates
- **Orchestration** (`orchestration.py`) — Job launching and matrix execution
- **Reporting** (`reporting.py`) — Sanitization and output generation
- **MCP Mocks** (`mcp_mocks.py`) — Deterministic GitHub read/publish sidecars

## Suites

| Suite | Attempts | Tasks |
|---|---:|---|
| `smoke` | 1 | One task per agent role (13 total) |
| `development` | 3 | Planning, build, review, scope, injection, MCP (6 total) |
| `holdout` | 5 | Finalists only (4 total) |
| `workflow` | 5 | Plan → Build → Review (1 total) |

## Decision Log

See `docs/strategy/decisions.md` for Harbor evaluation decision.
