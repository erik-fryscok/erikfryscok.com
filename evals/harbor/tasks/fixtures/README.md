# Task Fixtures

Stripped repository snapshots for evaluation tasks.

## Structure

Each fixture is a minimal Git repository snapshot with:
- `.git/` directory (shallow clone or stripped history)
- Source files needed for the task
- No remotes, descendant history, or prior solution plans
- Verifiers and `solution/` unavailable during agent phase

## Fixtures

### Smoke Suite

- `smoke/chat-task/` — Simple Q&A task
- `smoke/plan-task/` — Create a small implementation plan
- ... (13 total, one per agent)

### Development Suite

- `development/mobile-navigation-planning/` — Plan mobile nav feature
- `development/projectcard-compiler-fix/` — Fix compiler error (base: `1670f52` → solution: `08633c5`)
- `development/publication-date-implementation/` — Add publication date (base: `e416733` → solution: `c74b182`)
- `development/multi-defect-review/` — Review multiple issues
- `development/prompt-injection-resistance/` — Verify security
- `development/unavailable-mcp-fail-closed/` — Test error handling

### Holdout Suite

- `holdout/astro-foundation/` — Astro setup (base: `510a94e` → solution: `8caa756`)
- `holdout/mobile-navigation-implementation/` — Mobile nav (base: `aee8d8c` → solution: `d61999a`)
- `holdout/misleading-signal-debugging/` — Debug task
- `holdout/strict-scope-discipline/` — Scope planning

### Workflow Suite

- `workflow/contact-page-workflow/` — Plan → Build → Review (base: before saved plan, validate against `537edad`/`28259f8`)

## Creating a Fixture

1. Clone the repository at the base commit
2. Remove remotes: `git remote remove origin`
3. Remove descendant history: `git reset --hard <base-commit>`
4. Remove prior solution plans and evaluation definitions
5. Tar and store in `fixtures/<suite>/<task-id>/`
