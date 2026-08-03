# Troubleshooting

Common setup and execution issues.

## Dependency Resolution Fails

- Ensure Python is 3.12–3.14.
- Re-run `uv sync --all-extras`.
- Use a writable UV cache if needed: `UV_CACHE_DIR=<path> uv sync --all-extras`.

## OpenCode Not Found

- Install OpenCode CLI externally.
- Verify with `opencode --version` (expect `1.18.9`).

## Jobs Directory Validation Fails

- Set `ERIKFRYSCOK_HARBOR_JOBS_DIR`.
- Ensure it exists and is outside the repository.

## Docker Preflight Fails

- Start Docker Desktop/daemon.
- Re-run `uv run agent-eval preflight`.

## LM Studio Connectivity Warning

- Confirm endpoint in `LM_STUDIO_ENDPOINT`.
- Verify host/port reachability from your environment.
