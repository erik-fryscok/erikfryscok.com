# Reference Solutions

Hidden reference solutions for verification and oracle testing.

## Structure

Each solution is stored separately and unavailable during agent evaluation:

```
solution/
├── smoke/
│   ├── chat-task/solution.md
│   ├── plan-task/solution.md
│   └── ...
├── development/
│   ├── mobile-navigation-planning/solution.md
│   └── ...
└── holdout/
    └── ...
```

## Oracle Testing

The `agent-eval oracle` command:
1. Loads each reference solution
2. Runs it through the corresponding verifier
3. Confirms all mandatory dimensions pass
4. Reports any failures

This proves the verifier is not broken and the task is solvable.
