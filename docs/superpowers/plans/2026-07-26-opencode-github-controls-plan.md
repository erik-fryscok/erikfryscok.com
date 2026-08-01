# Project-Level OpenCode GitHub Controls — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a conservative project-level OpenCode configuration that separates local planning/building from read-only GitHub research and manually approved GitHub publication.

**Architecture:** A single `.opencode/opencode.jsonc` file configures two GitHub MCP servers with exact tool allowlists, globally denies their tools, and re-enables them only for dedicated subagents. Prompt files in `.opencode/prompts/` constrain behavior, and `/gh-read` and `/gh-publish` commands provide isolated subtask entry points.

**Tech Stack:** OpenCode, JSONC, GitHub MCP via `api.githubcopilot.com/mcp/`, fine-grained PATs through environment variables.

## Global Constraints

- Project-level config lives under `.opencode/` at the repository root.
- No employer or client confidential information may be added to config or prompts.
- Keep exact MCP tool allowlists rather than broad toolsets.
- `github_publish` starts with only `add_issue_comment` and `create_pull_request`.
- Cheap-model identifiers are left as comments for later configuration.

---

### Task 1: Create agent prompt files

**Files:**
- Create: `.opencode/prompts/github-read.md`
- Create: `.opencode/prompts/github-publish.md`

**Interfaces:**
- Consumes: nothing
- Produces: two prompt files referenced by `.opencode/opencode.jsonc` via `{file:./.opencode/prompts/...}`

- [ ] **Step 1: Create `.opencode/prompts/github-read.md`**

```markdown
You are a narrow, read-only GitHub research agent.

Use GitHub only for information unavailable from the local workspace or already supplied in the conversation.

Rules:
- Prefer exact owner, repository, issue number, or PR number.
- Make one targeted call at a time.
- Do not browse broadly when a direct lookup is possible.
- Do not fetch complete histories, large diffs, file trees, or logs unless required.
- Do not retrieve information already present in the prompt.
- Use small result limits for searches and listings.
- Stop as soon as the question is answered.
- Return concise findings, identifiers, links, and any unresolved uncertainty.
- Never perform or propose a GitHub mutation.
```

- [ ] **Step 2: Create `.opencode/prompts/github-publish.md`**

```markdown
You are a narrowly scoped GitHub publication agent.

Perform exactly one mutation explicitly requested by the user.

Rules:
- Do not infer publication permission from an implementation request.
- Before calling a mutation tool, identify the repository, target, action, and payload.
- Do not broaden the requested scope.
- Do not create branches, modify repository files, push files, create remote commits, merge pull requests, trigger workflows, or perform cleanup.
- Do not perform follow-on mutations.
- After the approved operation succeeds or fails, stop and report the result.
```

- [ ] **Step 3: Validate prompt files render as Markdown**

Run:

```bash
ls -la .opencode/prompts/
```

Expected: both files exist with `.md` extension and the content above.

- [ ] **Step 4: Commit**

```bash
git add .opencode/prompts/github-read.md .opencode/prompts/github-publish.md
git commit -m "chore: add OpenCode GitHub agent prompts"
```

---

### Task 2: Create the main OpenCode configuration

**Files:**
- Create: `.opencode/opencode.jsonc`

**Interfaces:**
- Consumes: `.opencode/prompts/github-read.md`, `.opencode/prompts/github-publish.md`
- Produces: loaded OpenCode configuration for `plan`, `build`, `github-read`, `github-publish`, `explore`, `scout`, and `general` agents

- [ ] **Step 1: Create `.opencode/opencode.jsonc`**

```jsonc
{
  "$schema": "https://opencode.ai/config.json",

  // Safe starting point. Explicitly switch to Build when implementation begins.
  "default_agent": "plan",

  // Prevent subagents from recursively spawning more subagents.
  "subagent_depth": 1,

  "mcp": {
    /*
     * Remote-only GitHub information:
     * issues, PRs, reviews, comments, and statuses.
     *
     * Use a separate read-only fine-grained PAT restricted to the
     * repositories where this access is required.
     */
    "github_read": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "enabled": true,
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:GITHUB_READ_PAT}",

        // Exact tool allowlist rather than broad toolsets.
        "X-MCP-Tools": "get_me,issue_read,list_issues,search_issues,pull_request_read,list_pull_requests,search_pull_requests",

        // Additional protection against accidentally added write tools.
        "X-MCP-Readonly": "true"
      }
    },

    /*
     * Deliberately small publishing interface.
     *
     * Start with comments and draft PR creation. Add other write tools
     * only after a demonstrated need.
     */
    "github_publish": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "enabled": true,
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:GITHUB_WRITE_PAT}",
        "X-MCP-Tools": "add_issue_comment,create_pull_request"
      }
    }
  },

  /*
   * Keep the MCP servers connected, but hide their tools from all agents
   * unless an agent explicitly re-enables them.
   *
   * Do not use enabled:false here. That disables the entire server rather
   * than making it selectively available to agents.
   */
  "permission": {
    "github_*": "deny"
  },

  "agent": {
    "plan": {
      "temperature": 0.1,
      "steps": 10,
      "permission": {
        "edit": "deny",
        "bash": "deny",
        "github_*": "deny",

        "task": {
          "*": "deny",

          // Fast local read-only exploration.
          "explore": "allow",

          // These can add cost, so require approval before delegation.
          "scout": "ask",
          "github-read": "ask",
          "general": "ask",

          // Publication must never happen through automatic delegation.
          "github-publish": "deny"
        }
      }
    },

    "build": {
      "temperature": 0.2,
      "steps": 20,
      "permission": {
        "edit": "allow",

        // Build works locally and delegates remote reads when necessary.
        "github_*": "deny",

        "task": {
          "*": "deny",
          "explore": "allow",
          "scout": "ask",
          "github-read": "ask",
          "general": "ask",
          "github-publish": "deny"
        },

        /*
         * Allow harmless inspection commands.
         * Ask before local state changes.
         * Deny high-risk/destructive operations.
         *
         * Rules are evaluated in order; the last matching rule wins.
         */
        "bash": {
          "*": "ask",

          "git status*": "allow",
          "git diff*": "allow",
          "git log*": "allow",
          "git show*": "allow",
          "git rev-parse*": "allow",
          "git ls-files*": "allow",

          "git commit*": "ask",
          "git push*": "ask",

          "git push *--force*": "deny",
          "git reset --hard*": "deny",
          "git clean*": "deny",
          "git branch -D*": "deny",

          /*
           * Prevent GitHub CLI from silently bypassing your MCP rules.
           * Specific read-only gh commands can be allowed later.
           */
          "gh *": "ask",
          "gh pr merge*": "deny",
          "gh repo delete*": "deny"
        }
      }
    },

    "github-read": {
      "description": "Use only when the task depends on remote GitHub issue or pull-request state that is unavailable locally. Make one targeted query at a time, limit lists to 10 items, avoid diffs unless requested, and return a concise summary.",
      "mode": "subagent",

      // Explicitly assign your cheapest reliable tool-capable model.
      // "model": "provider/cheap-model",

      "temperature": 0,
      "steps": 5,

      "permission": {
        "edit": "deny",
        "bash": "deny",
        "read": "deny",
        "glob": "deny",
        "grep": "deny",
        "lsp": "deny",
        "webfetch": "deny",
        "websearch": "deny",
        "task": "deny",

        "github_read_*": "allow",
        "github_publish_*": "deny"
      }
    },

    "github-publish": {
      "description": "Perform exactly one explicitly requested GitHub mutation. Default new pull requests to draft. Never merge, modify repository files, push commits, update branches, assign another coding agent, or perform follow-up actions. Stop after the approved action and report its URL.",
      "mode": "subagent",

      // A small deterministic model should be sufficient.
      // "model": "provider/cheap-model",

      "temperature": 0,
      "steps": 3,

      "permission": {
        "edit": "deny",
        "bash": "deny",
        "read": "deny",
        "glob": "deny",
        "grep": "deny",
        "lsp": "deny",
        "webfetch": "deny",
        "websearch": "deny",
        "task": "deny",

        // Read before publishing when necessary.
        "github_read_*": "allow",

        // Every advertised publishing operation requires approval.
        "github_publish_*": "ask"
      }
    },

    /*
     * Limit built-in agents as well. Tune these values from your test data.
     */
    "general": {
      "disable": true
    },
    "explore": {
      "steps": 6
      // Add a low-cost model here.
      // "model": "provider/low-cost-tool-model"
    },
    "scout": {
      "steps": 8
      // Add a low-cost model here.
      // "model": "provider/low-cost-tool-model"
    }
  },

  "command": {
    "gh-read": {
      "description": "Inspect GitHub metadata in an isolated read-only subtask",
      "agent": "github-read",
      "subtask": true,
      "template": "Answer this GitHub-only question using the minimum number of targeted calls: $ARGUMENTS"
    },

    "gh-publish": {
      "description": "Perform one explicitly requested GitHub mutation",
      "agent": "github-publish",
      "subtask": true,
      "template": "Perform only this explicitly requested GitHub mutation, then stop: $ARGUMENTS"
    }
  }
}
```

- [ ] **Step 2: Validate JSONC syntax**

Run:

```bash
node --check .opencode/opencode.jsonc
```

Expected: `node --check` succeeds without output. If Node rejects JSONC comments, validate by loading the file in OpenCode instead.

- [ ] **Step 3: Commit**

```bash
git add .opencode/opencode.jsonc
git commit -m "chore: add project-level OpenCode configuration"
```

---

### Task 3: Validate configuration loading and document the change

**Files:**
- Modify: `CHANGELOG.md` (append user-visible entry if file exists; otherwise create it)
- Test: load the config with OpenCode

**Interfaces:**
- Consumes: `.opencode/opencode.jsonc`
- Produces: validated config behavior and updated changelog

- [ ] **Step 1: Verify file layout**

Run:

```bash
ls -la .opencode/
ls -la .opencode/prompts/
```

Expected: `.opencode/opencode.jsonc`, `.opencode/prompts/github-read.md`, and `.opencode/prompts/github-publish.md` exist.

- [ ] **Step 2: Validate config loads**

Run:

```bash
opencode --version
```

Then start OpenCode in the project directory and confirm the default agent is `plan` and `/gh-read` and `/gh-publish` commands are listed. If OpenCode provides a config validation command, run it.

- [ ] **Step 3: Update changelog**

If `CHANGELOG.md` exists, append under an `## Unreleased` section:

```markdown
## Unreleased

### Added

- Project-level OpenCode configuration with separate GitHub read/publish MCP servers, exact tool allowlists, and manually approved publishing agent.
```

If `CHANGELOG.md` does not exist, create it with the same content plus a top-level `# Changelog` heading.

- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: document OpenCode configuration in changelog"
```

---

## Self-review

**Spec coverage:**
- Single project-level config → Task 2.
- Separate read/publish MCPs with exact tool lists → Task 2.
- Global deny + agent-specific re-enable → Task 2.
- `default_agent: plan`, `subagent_depth: 1` → Task 2.
- Agent prompts → Task 1.
- `/gh-read` and `/gh-publish` commands → Task 2.
- Disabled `general`, step limits for explore/scout → Task 2.
- Validation and changelog → Task 3.

**Placeholder scan:** No TBD/TODO/"implement later" found.

**Type consistency:** Not applicable; this is a JSONC configuration without code-level types.
