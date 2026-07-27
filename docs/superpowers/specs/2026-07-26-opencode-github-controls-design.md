# Project-Level OpenCode GitHub Controls — Design

## Goal

Add a conservative, project-level OpenCode configuration that separates local planning/building from GitHub reads and publication, using fine-grained access controls and exact MCP tool allowlists.

## Context

The repository is a personal website built with Astro, TypeScript, and Tailwind CSS, hosted on Cloudflare Pages. There is no existing OpenCode configuration. The project already documents durable product context in `docs/` and tracks active delivery in GitHub.

## Design decisions

### Single project-level configuration

Use one file at `.opencode/opencode.jsonc` rather than separate safe/publish launch profiles. This keeps the normal workflow simple while still enforcing manual publishing through agent permissions. Separate profiles remain a future option if the project grows into a team workflow.

### Separate read and publish MCP servers

Two remote MCP servers connect to the GitHub Copilot MCP endpoint:

- `github_read`: uses `GITHUB_READ_PAT`, exposes only read tools, and sets `X-MCP-Readonly: true` as a server-side backstop.
- `github_publish`: uses `GITHUB_WRITE_PAT`, exposes only `add_issue_comment` and `create_pull_request` initially.

Both use exact `X-MCP-Tools` lists instead of toolsets to minimize context and keep capabilities predictable.

### Permission model

- Global default: `github_*` is denied for every agent.
- `plan`: local read/search only, no edits, no shell, no GitHub. Can delegate `explore` automatically and must ask before delegating `scout`, `github-read`, `general`, or `github-publish`.
- `build`: local edits and tests allowed, GitHub tools denied, shell commands use ask/deny rules. Can delegate `explore`, `scout`, `github-read`, and `general` with approval, but never `github-publish`.
- `github-read`: only `github_read_*` tools allowed; all local tools denied.
- `github-publish`: only `github_publish_*` tools allowed, all set to `ask`; read-before-write tools (`get_me`, `issue_read`, `pull_request_read`) allowed. No local tools, no nested subagents.
- `general`: disabled to avoid broad, expensive work.
- `explore` and `scout`: short step limits with commented cheap-model placeholders.

### Default agent and depth

- `default_agent: "plan"` so every new session starts in the safe planning agent.
- `subagent_depth: 1` to prevent recursive subagent spawning.

### Prompt files

Agent prompts live in `.opencode/prompts/` and are loaded via `{file:./.opencode/prompts/...}` references:

- `github-read.md`: narrow read-only research agent rules.
- `github-publish.md`: single explicit mutation rules, no follow-on actions.

### Commands

Two isolated subtask commands are provided:

- `/gh-read`: invokes `github-read` for a targeted GitHub question.
- `/gh-publish`: invokes `github-publish` for one explicit mutation.

## Files

- `.opencode/opencode.jsonc` — main configuration
- `.opencode/prompts/github-read.md` — read agent prompt
- `.opencode/prompts/github-publish.md` — publish agent prompt
- `docs/superpowers/specs/2026-07-26-opencode-github-controls-design.md` — this design document
- `docs/superpowers/plans/2026-07-26-opencode-github-controls-plan.md` — implementation plan

## Out of scope

- Separate safe/publish launch profiles (future option).
- Additional publish tools such as `update_pull_request`, `issue_write`, or `pull_request_review_write` until a repeatable need is demonstrated.
- Hard-coded model identifiers for cheap agents; placeholders will be commented so the user can fill them in.

## Success criteria

- `opencode` loads the project-level config without errors.
- `plan` and `build` agents cannot invoke GitHub tools.
- `github-read` can read issues and pull requests but cannot mutate them.
- `github-publish` requires approval before any mutation.
- `/gh-read` and `/gh-publish` commands are available and run as isolated subtasks.
