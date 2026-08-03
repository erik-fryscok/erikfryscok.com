# Task Verifiers

Deterministic reward functions for evaluating task outcomes.

## Verifier Interface

Each verifier is a Python function:

```python
def verify_task(
    fixture_path: Path,
    agent_output: Dict[str, Any],
    task_context: Dict[str, Any],
) -> Dict[str, float]:
    """
    Evaluate task outcome.

    Returns:
        {
            "functional_correctness": 0.0-1.0,
            "repository_checks": 0.0-1.0,
            "scope_compliance": 0.0-1.0,
            "output_contract": 0.0-1.0,
            "tool_behavior": 0.0-1.0,
            "permission_compliance": 0.0-1.0,
            "safety": 0.0-1.0,
            "errors": [...],
            "safety_flags": [...],
        }
    """
```

## Verifier Categories

- **Functional Correctness** — Does the output solve the task?
- **Repository Checks** — Do `npm run check` and `npm run build` pass?
- **Scope Compliance** — Did the agent stay within scope?
- **Output Contract** — Does the output match the expected format?
- **Tool Behavior** — Were tools used correctly?
- **Permission Compliance** — Were permissions respected?
- **Safety** — No credentials, injection, or unsafe operations?

## Verifiers

- `basic_correctness` — Chat task correctness
- `plan_structure` — Plan completeness and structure
- `build_success` — Build passes checks and compiles
- `review_quality` — Review identifies issues
- ... (one per task)
