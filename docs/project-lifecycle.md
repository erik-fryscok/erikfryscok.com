# Project Lifecycle

## Source of truth

Git records durable knowledge: product intent, strategy, decisions, architecture, experiment outcomes, journal entries, and released changes.

GitHub records active delivery work: status, priority, dates, dependencies, release scope, and discussion. The repository's public Project is the current roadmap; issues are the unit of work; milestones define formal releases.

Do not maintain duplicate task lists, live roadmap tables, or release checklists in Markdown.

## Work model

- Use a top-level `type:initiative` issue for a meaningful product outcome.
- Use sub-issues for its features, research, content, documentation, or implementation work.
- Link each issue to the documentation that explains its context or decision.
- Use the project board for status, priority, horizon, and dates.
- Assign each shipped item to a GitHub milestone when it belongs to a formal release.

## Releases

The site may deploy on every merge to `main`. A formal release is a meaningful product checkpoint, not every deployment.

For each formal release, confirm its milestone scope, update [CHANGELOG.md](../CHANGELOG.md), create the corresponding Git tag and GitHub Release, then close the milestone. Add a journal entry only when there is a useful lesson or decision to preserve.

## Documentation decisions

Use the compact [decision log](strategy/decisions.md) for ordinary choices. Create a dedicated ADR only when a structural decision needs alternatives, consequences, and lasting technical context.
