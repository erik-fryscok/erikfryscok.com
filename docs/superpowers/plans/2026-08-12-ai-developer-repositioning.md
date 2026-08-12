# AI Developer Website Repositioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition erikfryscok.com around hands-on AI systems for software development while presenting Local AI Lab honestly as a prominent experimental learning and evaluation environment—not a production solution or frontier-model replacement.

**Architecture:** Preserve the static Astro architecture and portrait-led design. Align sitewide copy, metadata, and durable strategy; rebuild the homepage around concrete evidence; and add an evidence-based Local AI Lab case study with explicit capability and escalation boundaries.

**Tech Stack:** Astro 7, TypeScript strict mode, Tailwind CSS 4, Node.js 24, Node built-in test runner.

## Global Constraints

- Work from the latest `origin/main`, including the merged Agent Skills case study, on `codex/ai-developer-repositioning`.
- Related work: [GitHub issue #42](https://github.com/erik-fryscok/erikfryscok.com/issues/42), a sub-issue of #1.
- Present Local AI Lab as an **experimental AI lab**, learning playground, and evaluation testbed.
- Never describe Local AI Lab as production-ready, a production architecture, a team solution, or a replacement for frontier cloud models.
- State that local models are useful for bounded experiments, small targeted changes, and fixes, but fall short on higher-stakes, ambiguous, complex, large-context, or reliability-critical work.
- State that frontier/flagship cloud models are the escalation path when task risk or complexity exceeds demonstrated local capability.
- Preserve the existing portrait, navigation, articles, Agent Skills case study, personal-website case study, and `/now` personal sections.
- Do not claim external adoption, benchmark superiority, ML-research credentials, guaranteed privacy/safety, or outcomes not established by public evidence.
- Do not publish raw benchmark data, model answers, local paths, machine details, credentials, or employer/client information.
- Defer RSS, structured data, social images, GitHub/LinkedIn profile changes, and Local AI Lab licensing/topics.

---

### Task 1: Record the approved direction

**Files:**
- Create: `docs/superpowers/specs/2026-08-12-ai-developer-repositioning-design.md`
- Modify: `docs/README.md`

- [ ] Write a design spec that records the identity (hands-on engineering leader building and evaluating AI developer systems), audience (engineering peers, technical leaders, hiring teams), themes (AI-assisted engineering; evaluations and reliability; local/open-weight experimentation; AI engineering leadership), proof order (Local AI Lab, Agent Skills, Codex writing), Local AI Lab's experimental status and escalation boundaries, route `/projects/local-ai-lab`, and automated/responsive acceptance criteria.
- [ ] Index the design and this plan in `docs/README.md`.
- [ ] Run `git diff --check` and commit with `docs: define AI developer repositioning`.

---

### Task 2: Add the calibrated Local AI Lab case study

**Files:**
- Create: `src/pages/projects/local-ai-lab.astro`
- Create: `tests/local-ai-lab-case-study.test.mjs`
- Modify: `src/pages/projects.astro`
- Modify: `tests/launch-readiness.test.mjs`

- [ ] First add build-output tests proving Local AI Lab is before Agent Skills and erikfryscok.com; marked "Experimental AI lab"; has the correct internal and source links; and its case study contains OpenAI-compatible aliases, structured tool calls, `bench-llama`, `bench-server`, `bench-quality`, production limits, bounded-work strengths, higher-stakes limitations, frontier-cloud escalation, and the source URL. Tests must reject claims that it is a production solution, frontier replacement, or viable for every workload. Run and observe the expected failure.
- [ ] Add Local AI Lab first on Projects with this description: "An experimental learning and evaluation environment for local and open-weight models, exploring routing, model lifecycle, compatibility, benchmarks, and the boundary between useful local work and tasks that still require frontier cloud models." Include the specified technologies, outcomes, case-study link, source link, and visible "Experimental AI lab" supporting label.
- [ ] Replace the Projects intro with: "Selected projects showing how I build, test, and reason about AI developer systems. Local AI Lab is an experimental learning environment; Agent Skills is the more directly reusable developer workflow project."
- [ ] Add `/projects/local-ai-lab` with sections: An experimental AI lab; What the lab explores; Where local models are useful; Where they fall short; When to escalate; Compatibility before promotion; Layered evaluation; Evidence boundaries; What this demonstrates; Explore the project. Include the approved production-limit callout and the documented command block.
- [ ] Register metadata: title `Local AI Lab — Experimental AI Project`; description `How Erik Fryscok uses Local AI Lab to learn about local-model routing, lifecycle, compatibility, evaluation, and the boundary between local and frontier AI.`; page type article.
- [ ] Run `npm run check`, `npm test`, `git diff --check`, and commit with `feat: add experimental Local AI Lab case study`.

---

### Task 3: Reposition Home around calibrated evidence

**Files:**
- Create: `tests/ai-developer-positioning.test.mjs`
- Modify: `src/pages/index.astro`
- Modify: `tests/launch-readiness.test.mjs`

- [ ] First add a build-output test for the exact new headline and proof order: Local AI Lab, Agent Skills, Why I Keep Coming Back to Codex. It must verify experimental/lab language and links to their routes. Observe failure.
- [ ] Use the hero headline: `Building practical AI systems for software development.`
- [ ] Use this supporting copy: `I’m a software development team lead and hands-on engineer working with coding agents, local and open-weight models, developer tooling, evaluations, cloud infrastructure, and the systems that help engineering teams ship better software.`
- [ ] Use this introduction: `I build and evaluate the systems around AI-assisted software development: agent workflows, developer tooling, model experiments, and the guardrails that make them useful in real teams. My leadership experience shapes the work—clear evidence, honest capability boundaries, maintainable systems, and better engineering outcomes over novelty.`
- [ ] Replace generic cards with a two-column proof grid: dominant, span-two-column Local AI Lab card labelled "Experimental AI lab"; Agent Skills and Why I Keep Coming Back to Codex on the second row. Use the approved descriptions and internal links.
- [ ] Update Home metadata to title `Erik Fryscok — Practical AI Systems for Software Development` and description `Erik Fryscok builds and evaluates AI systems for software development, including coding-agent workflows, local-model experiments, evaluations, and developer tooling.`
- [ ] Use the approved opportunities/collaboration CTA and preserve portrait behavior.
- [ ] Run `npm run check`, `npm test`, `git diff --check`, and commit with `feat: reposition Home around calibrated AI engineering`.

---

### Task 4: Align supporting pages and durable strategy

**Files:**
- Modify: `src/pages/about.astro`, `src/pages/now.astro`, `src/pages/writing.astro`, `src/pages/contact.astro`
- Modify: `tests/launch-readiness.test.mjs`, `README.md`, `docs/product/brief.md`, `docs/strategy/positioning.md`, `docs/strategy/decisions.md`, `docs/ideas/content-backlog.md`, `CHANGELOG.md`

- [ ] Align About, Now, Writing, and Contact to hands-on AI/software engineering with leadership context. About must use "Evidence over AI novelty" and explain bounded local/open-weight experimentation. Now must use "Building and evaluating AI developer systems" and preserve guitar/cycling content. Writing must use the approved AI-assisted engineering sentence. Contact must invite relevant opportunities without a response-time claim.
- [ ] Update page metadata exactly as approved in the plan and corresponding launch-readiness expectations.
- [ ] Set durable positioning to: `I build and evaluate practical AI systems for software development—agents, developer tools, model experiments, and team workflows—combining hands-on engineering with leadership experience and explicit capability boundaries.` Record all four themes, Lab versus Agent Skills roles, and frontier cloud escalation.
- [ ] Update the product brief headline/supporting copy, README summary, content-backlog introduction, decision log (supersede the 2026-07-20 leadership/enterprise-AI decision and add the approved 2026-08-12 decision), and Unreleased changelog entries specified in the approved plan.
- [ ] Run `npm run check`, `npm test`, `git diff --check`, and commit with `docs: align AI positioning and model boundaries`.

---

### Task 5: Verify, review, and publish

- [ ] Run `npm run check`, `npm test`, `git diff --check`, and review Local AI Lab language with `rg` for production, solution, replacement, frontier, flagship, parity, and experimental.
- [ ] Inspect `/`, `/projects`, and `/projects/local-ai-lab` at 375px and 1280px for hierarchy, overflow, portrait balance, command-block overflow behavior, focus states, and link behavior.
- [ ] Validate documentation links and public claims against the Local AI Lab README.
- [ ] Use SSH, push `codex/ai-developer-repositioning`, and open a draft PR containing `Closes #42`, the change summary, boundary framing, and verification evidence.
