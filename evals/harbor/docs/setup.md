# Setup

## Prerequisites

- Python 3.12–3.14
- `uv`
- Docker
- OpenCode CLI 1.18.9

OpenCode is a runtime CLI prerequisite for this harness and is not installed via Python dependencies.

## Verify OpenCode Version

```bash
opencode --version
```

Expected output includes `1.18.9`.

## Install Python Dependencies

```bash
uv sync --all-extras
```

## Configure Environment

```bash
cp .env.example .env
```

Set `ERIKFRYSCOK_HARBOR_JOBS_DIR` to a path outside this repository.

## Preflight

```bash
uv run agent-eval preflight
```
