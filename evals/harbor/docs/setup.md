# Setup

Installation, environment, and preflight for local Harbor evaluation runs.

## Requirements

- Python 3.12–3.14
- `uv`
- Docker
- OpenCode CLI 1.18.9 (external prerequisite)

## Install

```bash
uv sync --all-extras
```

## Environment

```bash
cp .env.example .env
```

Set required variables:

- `ERIKFRYSCOK_HARBOR_JOBS_DIR` — absolute path **outside this repository**

Optional variables:

- `LM_STUDIO_ENDPOINT`
- `JUDGE_MODEL`
- `GITHUB_MCP_TOKEN`

## Verify OpenCode

```bash
opencode --version
```

Expected output includes `1.18.9`.

## Preflight Checks

```bash
uv run agent-eval preflight
```

This verifies Docker availability and optional LM Studio connectivity.
