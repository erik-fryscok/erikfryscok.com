# Task Authoring

Fixture creation, verifier design, and reference-solution workflow.

## Fixture Workflow

1. Choose a base commit and task scope.
2. Create a minimal fixture snapshot under `tasks/fixtures/<suite>/<task-id>/`.
3. Remove remotes and irrelevant history/content.
4. Ensure fixture contains only files needed for deterministic evaluation.

## Verifier Design

Each task verifier should return deterministic dimensions:

- `functional_correctness`
- `repository_checks`
- `scope_compliance`
- `output_contract`
- `tool_behavior`
- `permission_compliance`
- `safety`
- `errors` and `safety_flags`

Prefer explicit checks over heuristic scoring.

## Hidden Reference Solutions

Store oracle/reference answers in `tasks/solution/<suite>/<task-id>/`.

Rules:

- Keep solutions unavailable during agent runs.
- Use `agent-eval oracle` to prove tasks are solvable and verifiers are valid.
