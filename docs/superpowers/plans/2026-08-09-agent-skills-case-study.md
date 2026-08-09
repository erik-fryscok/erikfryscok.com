# Agent Skills Case Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Feature the renamed Agent Skills repository as the leading website project and publish an evidence-first case study for its first skill.

**Architecture:** Reuse the existing `ProjectCard` data interface on `/projects`, add one static Astro case-study route, and verify the generated site through the existing Node test suite. Keep durable product context in the documentation index, design record, decision log, and changelog.

**Tech Stack:** Astro 7, TypeScript, Tailwind CSS 4, Markdown documentation, Node test runner.

## Global Constraints

- Keep `Agent Skills` first and `erikfryscok.com` second on `/projects`.
- Do not change `src/components/ProjectCard.astro` or its interface.
- Keep claims evidence-based: no adoption metrics, delivered-plugin claims, or mature-ecosystem language.
- Keep `github-public-readiness` as the only shipped skill featured at launch.
- Distinguish current evidence from future intent.
- Ensure command and prompt blocks do not overflow a 375px viewport.

### Task 1: Add the project card and case study using test-driven development

**Files:**
- Modify: `tests/projects-case-study.test.mjs`
- Modify: `src/pages/projects.astro`
- Create: `src/pages/projects/agent-skills.astro`

- [ ] **Step 1: Write failing output-focused tests**

Extend `tests/projects-case-study.test.mjs` to verify that the built `/projects` output features `Agent Skills` before `erikfryscok.com`, links internally to `/projects/agent-skills`, and links externally to `https://github.com/erik-fryscok/skills`. Verify the built case study contains the two CLI commands, the first skill slug, all three example prompts, expected report output, and links to the repository and first skill.

- [ ] **Step 2: Run the focused test and confirm RED**

Run `npm test -- --test-name-pattern='Agent Skills'` or the closest supported focused command. Confirm the new assertions fail because the card and route do not yet exist.

- [ ] **Step 3: Add Agent Skills first on `/projects`**

Add an `Agent Skills` project entry before the existing personal website entry. Use the existing `ProjectCard` interface unchanged, with an internal `Read case study` link and an external `Source` link.

Use this evidence-bounded card content:

- Description: `An open-source collection of reusable, evidence-backed agent skills that turn practical engineering judgment into dependable software-development workflows.`
- Technologies: `Agent Skills`, `Markdown`, `YAML`, `GitHub`
- Outcomes: an evidence-based GitHub public-readiness audit; separation of workflow guidance, evaluation criteria, and reporting structure; an MIT-licensed foundation for future agent tooling

- [ ] **Step 4: Build the case-study route**

Create `/projects/agent-skills` using `BaseLayout` and the established narrow case-study presentation. Include:

- Problem and purpose
- Anatomy of a skill package
- The `github-public-readiness` execution flow
- Safety and evidence design
- A reusable foundation for future skills and plugin packaging
- Installation and one-off CLI use
- Three example prompts
- Expected report output
- Repository and first-skill links

Use `overflow-x-auto` on code and prompt containers and preserve clear internal/external link behavior.

Use these three prompts:

```text
Use $github-public-readiness to audit this repository for safe public release and portfolio value.
```

```text
Audit this repository before I make it public. Prioritize disclosure risks and the smallest release checklist; do not modify files or visibility.
```

```text
Assess whether this repository is worth featuring in my portfolio, keeping public safety and showcase value as separate verdicts.
```

Describe the expected report as a readiness classification, a separate portfolio judgment, evidence-linked findings, an ordered release checklist, and the verification performed.

- [ ] **Step 5: Run the tests and confirm GREEN**

Run `npm test`; expect all tests and the production build to pass, with `dist/projects/agent-skills/index.html` generated.

### Task 2: Record the approved design and durable project context

**Files:**
- Create: `docs/superpowers/specs/2026-08-09-agent-skills-case-study-design.md`
- Modify: `docs/README.md`
- Modify: `docs/strategy/decisions.md`
- Modify: `CHANGELOG.md`
- Verify: `docs/superpowers/plans/2026-08-09-agent-skills-case-study.md`

- [ ] **Step 1: Write the design record**

Document the approved project positioning, content structure, evidence boundaries, CLI examples, responsive behavior, and repository-name rationale.

- [ ] **Step 2: Update the documentation index**

Link both the design record and this implementation plan from `docs/README.md` using the existing index structure.

- [ ] **Step 3: Add the decision-log entry**

Record the 2026-08-09 decision to use the generic `erik-fryscok/skills` collection name because the skills CLI and skills.sh foreground individual skill names while retaining `owner/repo` as source provenance. State that standalone MCP products or plugins can still receive separate repositories when appropriate.

- [ ] **Step 4: Update the Unreleased changelog**

Under `Unreleased` → `Added`, record the Agent Skills project card, case study, and CLI guidance, referencing website issue `#40`.

- [ ] **Step 5: Validate documentation**

Run `git diff --check`, inspect changed Markdown links, and run the relevant documentation/link tests if present.

### Task 3: Verify the completed website branch

**Files:**
- Verify: generated Astro output and all changed files

- [ ] **Step 1: Run diagnostics and tests**

Run `npm run check` and `npm test`; expect exit code 0 for both.

- [ ] **Step 2: Verify generated output**

Confirm `dist/projects/agent-skills/index.html` exists and contains `github-public-readiness`, both CLI commands, and the repository/skill links.

- [ ] **Step 3: Search for stale repository references**

Search the website and skills repositories for unintended `developer-skills` names or URLs. Historical planning context may be reported separately; user-visible or active links must use `erik-fryscok/skills`.

- [ ] **Step 4: Review responsive presentation**

Run the built site locally and inspect `/projects` and `/projects/agent-skills` at 375px and 1280px. Verify prompt overflow, readable hierarchy, and internal/external link behavior.
