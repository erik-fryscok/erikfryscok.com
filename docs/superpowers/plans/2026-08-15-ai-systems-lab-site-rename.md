# AI Systems Lab Site Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the website's current Local AI Lab references to AI Systems Lab and update Home, Writing, Projects, and supporting current-positioning content to describe local and cloud-hosted model/provider scope accurately.

**Architecture:** Keep the existing static Astro page structure and build-output regression-test approach. Rename the project case-study source file and canonical route, preserve the former route as a noindex migration redirect, and update active site copy and durable strategy while leaving historical plans/specifications intact as history.

**Tech Stack:** Astro 7, TypeScript, Tailwind CSS, Node.js 24 built-in test runner, `@astrojs/sitemap`

## Global Constraints

- Use `ai-systems-lab` for the repository slug and **AI Systems Lab** for the project/display name.
- Use `/projects/ai-systems-lab` as the canonical internal case-study route.
- Retain `/projects/local-ai-lab` only as an intentional migration redirect to `/projects/ai-systems-lab`; do not leave internal navigation pointing to the former route.
- Explain that local llama.cpp and cloud-hosted OpenAI-compatible providers are both within scope.
- Preserve local-model support as a first-class use case.
- Keep provider-specific concerns conceptually isolated from provider-agnostic routing and evaluation.
- Continue to describe AI Systems Lab as an experimental learning and evaluation testbed, not production infrastructure.
- ERI-19 provider support is verified in `ai-systems-lab` `origin/main` at `bb060300`: local llama.cpp remains the default first-class backend; opt-in cloud-hosted OpenAI-compatible providers participate in provider-agnostic `chat`, `bench-server`, and candidate `bench-quality` paths. Preserve these distinctions in public copy.
- Do not add dependencies or restructure unrelated pages/components.
- Preserve former-name references only in explicit historical or migration context.
- Do not publish credentials, private machine details, private repository metadata, employer/client material, or proprietary implementation details.

---

## File Structure

- `docs/superpowers/plans/2026-08-15-ai-systems-lab-site-rename.md` — this task-by-task execution contract.
- `src/pages/index.astro` — Home positioning and the leading AI Systems Lab proof card.
- `src/pages/writing.astro` — Writing metadata and introduction broadened from local-only experimentation to local/cloud model systems.
- `src/pages/projects.astro` — Project-card name, summary, internal case-study link, source link, metadata, and introduction.
- `src/pages/projects/ai-systems-lab.astro` — renamed canonical case study with provider-neutral project messaging and preserved local-model evidence.
- `astro.config.mjs` — former-route migration redirect only.
- `src/pages/now.astro` — current-focus reference aligned with the new name and broader scope.
- `tests/ai-developer-positioning.test.mjs` — Home and Writing copy/ordering regression coverage.
- `tests/ai-systems-lab-case-study.test.mjs` — renamed Projects and case-study content/claim guards.
- `tests/launch-readiness.test.mjs` — canonical metadata, route, sitemap, internal-link, and redirect regression coverage.
- `README.md` and `docs/product/brief.md` — current top-level/product wording.
- `docs/strategy/positioning.md` and `docs/strategy/decisions.md` — durable current positioning and the superseding rename decision.
- `docs/README.md` — historical entries clarified as referring to the former project name.
- `CHANGELOG.md` — unreleased user-visible rename and scope change.

### Task 1: Rename and broaden Home and Writing positioning

**Files:**
- Modify: `tests/ai-developer-positioning.test.mjs`
- Modify: `tests/launch-readiness.test.mjs`
- Modify: `src/pages/index.astro`
- Modify: `src/pages/writing.astro`
- Modify: `docs/product/brief.md`

**Interfaces:**
- Consumes: ERI-19 naming decision and the existing built-file test helpers in `tests/ai-developer-positioning.test.mjs` and `tests/launch-readiness.test.mjs`.
- Produces: Home and Writing HTML that consistently uses **AI Systems Lab** and describes local/cloud-hosted model scope; later route tests rely on the Home card linking to `/projects/ai-systems-lab`.

- [ ] **Step 1: Update the build-output expectations before changing page source**

In `tests/ai-developer-positioning.test.mjs`, replace the Home supporting-copy and first proof-description fixtures with:

```js
const supportingCopy =
  "I’m a software development team lead and hands-on engineer working with coding agents, local and cloud-hosted models, developer tooling, evaluations, cloud infrastructure, and the systems that help engineering teams ship better software.";

const proofDescriptions = [
  "An experimental learning and evaluation environment for AI model systems, exploring local llama.cpp and cloud-hosted OpenAI-compatible providers, routing, compatibility, benchmarks, and capability boundaries.",
  "Reusable, evidence-backed workflows that turn practical engineering judgment into dependable instructions for AI coding agents.",
  "What customizing coding agents, building evaluations, weighing usage costs, and testing workflow continuity taught me.",
];
```

Rename `localLabPosition` to `systemsLabPosition`, expect `>AI Systems Lab</h3>`, and replace the project-card assertions with:

```js
assert.ok(systemsLabPosition >= 0, "expected AI Systems Lab proof on Home");
assert.ok(systemsLabPosition < agentSkillsPosition, "expected AI Systems Lab before Agent Skills");
assert.match(
  html,
  /<a href="\/projects\/ai-systems-lab" class="[^"]*sm:col-span-2[^"]*"><p[^>]*>EXPERIMENTAL<\/p><h3[^>]*>AI Systems Lab<\/h3>/,
);
assert.match(html, /href="\/projects\/ai-systems-lab"/);
assert.doesNotMatch(html, /Local AI Lab|\/projects\/local-ai-lab/);
```

Add a focused Writing regression test to the same file:

```js
test("Writing describes model-system work across local and cloud environments", async () => {
  const html = await readFile(new URL("dist/writing/index.html", root), "utf8");
  const visibleText = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");

  assert.ok(
    visibleText.includes(
      "I write about AI-assisted software engineering, evaluations and reliability, local and cloud model systems, developer tooling, and the leadership practices that help teams adopt AI with appropriate judgment.",
    ),
  );
  assert.doesNotMatch(html, /local and open-weight model experiments/i);
});
```

In the `/writing` entry in `tests/launch-readiness.test.mjs`, change the expected description to:

```js
"Articles by Erik Fryscok on AI-assisted software engineering, agent evaluations, local and cloud model systems, developer tooling, and engineering leadership."
```

- [ ] **Step 2: Run the changed tests to verify they fail for the old name and copy**

Run:

```bash
npm test
```

Expected: FAIL because Home still renders `Local AI Lab` and `/projects/local-ai-lab`, and Writing still renders `local and open-weight model experiments`.

- [ ] **Step 3: Implement the minimal Home and Writing copy changes**

In `src/pages/index.astro`:

- Change the supporting paragraph to the exact `supportingCopy` fixture above.
- Rename the comment to `<!-- AI Systems Lab Card -->`.
- Change the card link to `/projects/ai-systems-lab`.
- Change the card heading to `AI Systems Lab`.
- Replace the card description with the exact first `proofDescriptions` fixture above.
- Keep the `EXPERIMENTAL` label, proof ordering, card classes, and “Explore the lab” CTA unchanged.

In `src/pages/writing.astro`, use these exact strings:

```astro
<BaseLayout
  title="Writing — Erik Fryscok"
  description="Articles by Erik Fryscok on AI-assisted software engineering, agent evaluations, local and cloud model systems, developer tooling, and engineering leadership."
>
```

```astro
<p class="text-gray-700 mb-8 leading-relaxed">
  I write about AI-assisted software engineering, evaluations and reliability,
  local and cloud model systems, developer tooling, and the leadership practices
  that help teams adopt AI with appropriate judgment.
</p>
```

In `docs/product/brief.md`, replace the supporting-copy quotation with the exact Home supporting copy from this task so durable product intent and rendered content remain synchronized.

- [ ] **Step 4: Build and run the focused tests to verify the changes pass**

Run:

```bash
npm run build
node --test --test-name-pattern='Home|Writing|metadata' tests/ai-developer-positioning.test.mjs tests/launch-readiness.test.mjs
```

Expected: PASS for the selected tests; the build generates Home and Writing with the new scope language.

- [ ] **Step 5: Commit the Home and Writing positioning change**

```bash
git add src/pages/index.astro src/pages/writing.astro docs/product/brief.md tests/ai-developer-positioning.test.mjs tests/launch-readiness.test.mjs
git commit -m "refactor: align home and writing with AI Systems Lab"
```

### Task 2: Rename the Projects card, canonical case study, and public route

**Files:**
- Rename: `tests/local-ai-lab-case-study.test.mjs` → `tests/ai-systems-lab-case-study.test.mjs`
- Modify: `tests/ai-systems-lab-case-study.test.mjs`
- Modify: `tests/launch-readiness.test.mjs`
- Modify: `src/pages/projects.astro`
- Rename: `src/pages/projects/local-ai-lab.astro` → `src/pages/projects/ai-systems-lab.astro`
- Modify: `src/pages/projects/ai-systems-lab.astro`
- Modify: `astro.config.mjs`

**Interfaces:**
- Consumes: `/projects/ai-systems-lab` links introduced on Home in Task 1; ERI-19's new GitHub slug `erik-fryscok/ai-systems-lab`.
- Produces: canonical `/projects/ai-systems-lab` case-study HTML, `/projects/local-ai-lab` migration HTML, and source links to `https://github.com/erik-fryscok/ai-systems-lab`.

- [ ] **Step 1: Rename and update the case-study regression test before changing implementation**

Run:

```bash
git mv tests/local-ai-lab-case-study.test.mjs tests/ai-systems-lab-case-study.test.mjs
```

In the renamed file:

- Set `sourceRepository` to `https://github.com/erik-fryscok/ai-systems-lab`.
- Rename `localLabPosition` to `systemsLabPosition`.
- Replace display-name expectations with `AI Systems Lab`.
- Replace case-study route/build paths with `/projects/ai-systems-lab` and `dist/projects/ai-systems-lab/index.html`.
- Rename the two project-specific test titles to start with `AI Systems Lab`.
- Keep the existing prohibited-claim patterns and local-model compatibility/evaluation evidence assertions, except replace `One endpoint with workload-specific model aliases and managed model lifecycle` with `Workload-specific model aliases across local llama.cpp and cloud-hosted OpenAI-compatible provider backends` to match the renamed Projects card.
- Change `projectsIntroduction` to:

```js
const projectsIntroduction =
  "Selected projects showing how I build, test, and reason about AI developer systems. AI Systems Lab is an experimental learning environment; Agent Skills is the more directly reusable developer workflow project.";
```

- Change `projectDescription` to:

```js
const projectDescription =
  "An experimental learning and evaluation environment for AI model systems, exploring provider-neutral routing, model lifecycle, compatibility, benchmarks, and local llama.cpp and cloud-hosted OpenAI-compatible capability boundaries.";
```

- Add these provider-scope assertions to the case-study test:

```js
for (const evidence of [
  "local llama.cpp remains a first-class backend",
  "cloud-hosted OpenAI-compatible providers participate in the same chat and evaluation paths",
  "provider-neutral request path",
  "provider-specific request construction",
  "credentials are opt-in environment variables",
]) {
  assert.match(html, new RegExp(evidence, "i"));
}
```

- Replace the boundary fixtures with the new display name:

```js
const prohibitedClaims = [
  "AI Systems Lab is a replacement for frontier cloud models.",
  "AI Systems Lab is ready for production.",
];
```

```js
for (const boundary of [
  "AI Systems Lab is not production infrastructure.",
  "AI Systems Lab is not a replacement for frontier cloud models.",
]) {
  // Keep the existing assertion body.
}
```

In `tests/launch-readiness.test.mjs`, replace the Projects metadata description with:

```js
"Selected AI and software engineering projects from Erik Fryscok, including the experimental AI Systems Lab, Agent Skills, and evidence-based developer tooling."
```

Replace the case-study `pages` entry with:

```js
{
  path: "/projects/ai-systems-lab",
  file: "dist/projects/ai-systems-lab/index.html",
  title: "AI Systems Lab — Experimental AI Project",
  heading: "AI Systems Lab",
  description:
    "How Erik Fryscok uses AI Systems Lab to explore provider-neutral model routing, lifecycle, compatibility, evaluation, and local and cloud AI boundaries.",
  pageType: "article",
},
```

Add this redirect regression test:

```js
test("the former AI lab route redirects to the renamed canonical case study", async () => {
  const html = await readBuiltFile("dist/projects/local-ai-lab/index.html");

  assert.match(
    html,
    /<meta http-equiv="refresh" content="0;url=\/projects\/ai-systems-lab">/,
  );
  assert.match(html, /<meta name="robots" content="noindex">/);
  assert.match(
    html,
    /<link rel="canonical" href="https:\/\/erikfryscok\.com\/projects\/ai-systems-lab\/?">/,
  );
});
```

Extend the sitemap test after its existing page loop:

```js
assert.doesNotMatch(sitemap, /<loc>https:\/\/erikfryscok\.com\/projects\/local-ai-lab\/?<\/loc>/);
```

- [ ] **Step 2: Run the renamed route and case-study tests to verify they fail**

Run:

```bash
npm test
```

Expected: FAIL because `/projects/ai-systems-lab` and its source file do not exist yet, Projects still contains the former name/links, and no migration redirect is configured.

- [ ] **Step 3: Rename the case-study source file and configure the migration redirect**

Run:

```bash
git mv src/pages/projects/local-ai-lab.astro src/pages/projects/ai-systems-lab.astro
```

Add the redirect beside `site` in `astro.config.mjs`:

```js
export default defineConfig({
  site: 'https://erikfryscok.com',
  redirects: {
    '/projects/local-ai-lab': '/projects/ai-systems-lab',
  },
```

This former slug is an intentional migration reference. Astro's static build emits a noindex HTML redirect with the new canonical URL.

- [ ] **Step 4: Update the Projects listing with the canonical name and links**

In the first object in `src/pages/projects.astro`, use:

```ts
{
  title: "AI Systems Lab",
  supportingLabel: "EXPERIMENTAL",
  description:
    "An experimental learning and evaluation environment for AI model systems, exploring provider-neutral routing, model lifecycle, compatibility, benchmarks, and local llama.cpp and cloud-hosted OpenAI-compatible capability boundaries.",
  technologies: ["Python", "llama.cpp", "OpenAI-compatible APIs", "Hugging Face", "JSONL"],
  outcomes: [
    "Workload-specific model aliases across local llama.cpp and cloud-hosted OpenAI-compatible provider backends",
    "Compatibility gates for visible completions and structured tool calls",
    "Layered throughput, server-path, and quality evaluation workflows",
  ],
  links: [
    { label: "Read case study", href: "/projects/ai-systems-lab", external: false },
    { label: "Source", href: "https://github.com/erik-fryscok/ai-systems-lab", external: true },
  ],
},
```

Use the exact Projects metadata description from the updated launch-readiness fixture. Replace the introduction with:

```astro
<p class="text-gray-700 mb-10 max-w-2xl">
  Selected projects showing how I build, test, and reason about AI developer
  systems. AI Systems Lab is an experimental learning environment; Agent
  Skills is the more directly reusable developer workflow project.
</p>
```

- [ ] **Step 5: Update the renamed case study without erasing local-model evidence**

In `src/pages/projects/ai-systems-lab.astro`:

- Set `sourceRepository` to `https://github.com/erik-fryscok/ai-systems-lab`.
- Use the exact title and description from the new `pages` fixture.
- Change the H1 and source-link label to **AI Systems Lab**.
- Replace the header summary with:

```astro
<p class="text-lg text-gray-700 max-w-2xl">
  A learning playground and evaluation testbed for understanding how local
  llama.cpp and cloud-hosted OpenAI-compatible models fit software-development
  workloads—and where their demonstrated capability ends.
</p>
```

- Replace the opening section body and boundary callout with:

```astro
<p class="text-gray-700 mb-4">
  AI Systems Lab makes provider abstraction, model routing, lifecycle management,
  compatibility checks, and repeatable evaluation concrete enough to study. Local
  llama.cpp remains a first-class backend and default workflow, while cloud-hosted
  OpenAI-compatible providers participate in the same chat and evaluation paths
  through shared model interfaces. Cloud provider credentials are opt-in
  environment variables and never committed configuration.
</p>
<aside class="rounded-lg border border-amber-300 bg-amber-50 p-5 text-amber-950">
  <p>
    <strong>Production limit:</strong> AI Systems Lab is not production
    infrastructure, a production architecture, a team-wide solution, or a
    replacement for frontier cloud models. It is an experimental learning and
    evaluation environment.
  </p>
</aside>
```

- Replace the “What the lab explores” paragraph with:

```astro
<p class="text-gray-700">
  The lab uses workload-specific model aliases behind a provider-neutral request
  path. Provider-specific request construction handles local runtime lifecycle or
  cloud API transport without coupling routing and evaluation workflows to one vendor. A
  curated catalog records each model’s provider, capabilities, intended role, and
  lifecycle so candidates can be tested before promotion.
</p>
```

- Keep the local usefulness, limitation, compatibility, evaluation, evidence-boundary, and benchmark-command sections. Update phrases that assume every candidate is locally managed: apply residency/unload requirements only to local runtimes, and require cloud-provider requests to satisfy the same observable completion/tool-call contract.
- Change the first “What this demonstrates” list item to:

```astro
<li>Designing provider-neutral routing around stable workload aliases while isolating provider-specific request construction and local lifecycle state.</li>
```

- Keep the production-limit and prohibited-claim language enforced by the tests.

- [ ] **Step 6: Build and run the Projects, route, metadata, and sitemap tests**

Run:

```bash
npm run build
node --test --test-name-pattern='AI Systems Lab|former AI lab route|metadata|sitemap|internal links' tests/ai-systems-lab-case-study.test.mjs tests/launch-readiness.test.mjs
```

Expected: PASS. `dist/projects/ai-systems-lab/index.html` is canonical, `dist/projects/local-ai-lab/index.html` is a noindex redirect, internal links resolve, and only the new route appears in the sitemap.

- [ ] **Step 7: Commit the Projects and route rename**

```bash
git add astro.config.mjs src/pages/projects.astro src/pages/projects/ai-systems-lab.astro tests/ai-systems-lab-case-study.test.mjs tests/launch-readiness.test.mjs
git commit -m "feat: rename project case study to AI Systems Lab"
```

### Task 3: Align current Now, repository, strategy, and release references

**Files:**
- Modify: `src/pages/now.astro`
- Modify: `tests/launch-readiness.test.mjs`
- Modify: `README.md`
- Modify: `docs/README.md`
- Modify: `docs/strategy/positioning.md`
- Modify: `docs/strategy/decisions.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: canonical name, scope language, and route established in Tasks 1–2.
- Produces: current non-historical website/documentation references that agree with ERI-19; former names remain only in the redirect, superseded decision, explicit rename changelog text, and dated historical plans/specifications.

- [ ] **Step 1: Add a failing current-content and stale-name regression check**

In `tests/launch-readiness.test.mjs`, update the `/now` expected metadata description to:

```js
"What Erik Fryscok is focused on now: AI developer systems, AI Systems Lab, agent workflows, guitar, and local cycling."
```

Add this test near the route metadata coverage:

```js
test("current public pages do not expose the former project name or route", async () => {
  const currentPages = pages.map(({ file }) => file);

  for (const file of currentPages) {
    const html = await readBuiltFile(file);
    assert.doesNotMatch(html, /Local AI Lab|\/projects\/local-ai-lab/i, file);
  }
});
```

Do not add the generated redirect page to `pages`; it is deliberately excluded from the canonical public-page set.

- [ ] **Step 2: Run the new current-content check to verify it fails**

Run:

```bash
npm test
```

Expected: FAIL because `/now` and its metadata still contain current former-name/local-only wording.

- [ ] **Step 3: Update the current Now and repository-level scope wording**

In `src/pages/now.astro`, use the exact metadata description from the updated test and replace the professional-focus paragraph with:

```astro
<p class="text-gray-700 leading-relaxed">
  I’m focused on coding-agent workflows, developer tooling, evaluations, and AI
  Systems Lab. The lab is a learning and evaluation environment for testing local
  and cloud-hosted models, provider boundaries, and workload fit—not production
  infrastructure or a claim that one model works for every task.
</p>
```

Update the first sentence in `README.md` to:

```markdown
Personal website and technical portfolio focused on AI systems for software development, including coding agents, evaluations, local and cloud model systems, developer tooling, and engineering leadership.
```

- [ ] **Step 4: Update active strategy and record the superseding decision**

In `docs/strategy/positioning.md`:

- Update `Last updated` to `2026-08-15`.
- Change theme 3 to:

```markdown
3. **Model-system experimentation** — provider-neutral routing and evaluation across local, open-weight, and cloud-hosted models, with explicit workload and capability boundaries.
```

- Replace the proof-role paragraph with:

```markdown
AI Systems Lab and Agent Skills play different proof roles. AI Systems Lab is an experimental learning and evaluation environment for model systems across local and cloud-hosted providers, not a production solution or a claim of model superiority. Local execution remains a first-class use case, while provider-neutral routing and evaluation keep core workflows independent of any one runtime or vendor. Agent Skills is the more directly reusable developer-workflow project. When a task exceeds a model's demonstrated capability, reliability, or risk boundary, the appropriate path is routing or escalation to a better-supported model/provider.
```

In `docs/strategy/decisions.md`, change the 2026-08-12 row status from `Active` to `Superseded`, preserving its former name as historical context. Append:

```markdown
| 2026-08-15 | Rename Local AI Lab to AI Systems Lab and broaden its identity from local-only execution to model systems across local and cloud-hosted providers. | The systems-oriented name preserves the experimental lab while removing deployment location as an architectural constraint. Local support remains first-class; shared routing/evaluation concepts should not couple core workflows to one provider or imply production readiness. | Active |
```

In `docs/README.md`, qualify the two dated AI-developer-repositioning entries as historical records by changing `Local AI Lab` to `the then-named Local AI Lab`. Do not rewrite the linked 2026-08-12 plan/spec; those are dated historical artifacts.

Add the new implementation plan to the top of the “Implementation plans” section:

```markdown
- [ERI-19: AI Systems Lab site rename](superpowers/plans/2026-08-15-ai-systems-lab-site-rename.md) — canonical naming, route migration, local/cloud provider scope, and stale-reference validation for Home, Writing, Projects, and current positioning.
```

- [ ] **Step 5: Record the user-visible rename in the unreleased changelog**

In `CHANGELOG.md`:

- Change current Unreleased feature/proof entries from `Local AI Lab` to `AI Systems Lab`.
- Add this first bullet under `### Changed`:

```markdown
- Renamed Local AI Lab to AI Systems Lab across Home, Writing, Projects, and current positioning; broadened its stated scope to include local and cloud-hosted providers while preserving its experimental, non-production boundaries (ERI-19).
```

This bullet is an intentional migration-context use of the former name.

- [ ] **Step 6: Rebuild and verify the current-content regression passes**

Run:

```bash
npm run build
node --test --test-name-pattern='current public pages|metadata' tests/launch-readiness.test.mjs
```

Expected: PASS. Every canonical public page is free of the former display name and route, while the generated migration redirect remains separate.

- [ ] **Step 7: Audit old-name occurrences and classify every allowed result**

Run:

```bash
rg -n -i 'local ai lab|local-ai-lab' src tests astro.config.mjs README.md CHANGELOG.md docs
```

Expected current-code results are limited to:

- `astro.config.mjs` — redirect source.
- `tests/launch-readiness.test.mjs` — redirect and stale-reference assertions.
- `CHANGELOG.md` — explicit rename/migration entry.
- `docs/strategy/decisions.md` — superseded decision and new rename decision.
- `docs/README.md`, `docs/superpowers/plans/`, and `docs/superpowers/specs/` — explicitly dated historical context.

Any occurrence in `src/`, canonical fixture data, `README.md`, or active positioning prose is a failure and must be replaced before committing.

- [ ] **Step 8: Commit the current-positioning and documentation alignment**

```bash
git add src/pages/now.astro tests/launch-readiness.test.mjs README.md docs/README.md docs/strategy/positioning.md docs/strategy/decisions.md CHANGELOG.md docs/superpowers/plans/2026-08-15-ai-systems-lab-site-rename.md
git commit -m "docs: align current positioning with AI Systems Lab"
```

### Task 4: Run the complete rename and release validation

**Files:**
- Verify: `src/pages/index.astro`
- Verify: `src/pages/writing.astro`
- Verify: `src/pages/projects.astro`
- Verify: `src/pages/projects/ai-systems-lab.astro`
- Verify: `src/pages/now.astro`
- Verify: `astro.config.mjs`
- Verify: `tests/*.test.mjs`
- Verify: current documentation and `CHANGELOG.md`

**Interfaces:**
- Consumes: all rendered pages, route migration, fixtures, and documentation from Tasks 1–3.
- Produces: evidence that ERI-19's website-reference scope is complete without stale canonical naming, broken links, sitemap duplication, or weakened experimental/local-model boundaries.

- [ ] **Step 1: Run static diagnostics**

Run:

```bash
npm run check
```

Expected: PASS with no Astro or TypeScript diagnostics.

- [ ] **Step 2: Run the full build-output regression suite**

Run:

```bash
npm test
```

Expected: PASS for every test in `tests/*.test.mjs`, including canonical metadata, internal links, sitemap coverage, redirect behavior, claim guards, Home proof order, Writing scope, and Projects case-study evidence.

- [ ] **Step 3: Run whitespace and stale-reference audits**

Run:

```bash
git diff --check
rg -n -i 'local ai lab|local-ai-lab' src README.md docs/product docs/strategy/positioning.md
```

Expected: `git diff --check` exits 0. The `rg` command returns no matches in rendered source or current product/positioning documents; historical/migration references were classified separately in Task 3.

- [ ] **Step 4: Inspect the generated canonical and migration artifacts**

Run:

```bash
rg -n 'AI Systems Lab|ai-systems-lab|Local AI Lab|local-ai-lab|canonical|noindex' dist/index.html dist/writing/index.html dist/projects/index.html dist/projects/ai-systems-lab/index.html dist/projects/local-ai-lab/index.html dist/sitemap-*.xml
```

Expected:

- Home and Projects link only to `/projects/ai-systems-lab`.
- Writing uses local/cloud model-system scope wording.
- The canonical case study uses **AI Systems Lab** and the new GitHub URL.
- The former route contains only a noindex redirect and canonical link to the new route.
- The sitemap contains `/projects/ai-systems-lab/` and omits `/projects/local-ai-lab/`.

- [ ] **Step 5: Perform responsive and link-behavior review**

Run:

```bash
npm run dev
```

Inspect `/`, `/writing`, `/projects`, `/projects/ai-systems-lab`, and `/now` at 375px and 1280px. Verify the renamed heading does not wrap awkwardly, the Home proof hierarchy and `EXPERIMENTAL` label remain clear, the case-study command block still scrolls horizontally, focus states remain visible, the new internal/source links work, and `/projects/local-ai-lab` redirects to the canonical case study.

- [ ] **Step 6: Review final scope and history preservation**

Run:

```bash
git status --short
git diff --stat
git log -3 --oneline
```

Expected: only the files named in this plan are changed; historical 2026-08-12 plans/specifications retain their dated terminology; the new plan itself is present; and the implementation is split into the three focused commits described above.

---

## Self-Review Results

- **Spec coverage:** Home, Writing, Projects, the case study, source/canonical links, local/cloud scope, local-first support, provider-neutral wording, experimental boundaries, active current references, tests, sitemap, redirect, and stale-name verification are all assigned to tasks.
- **Scope boundary:** This plan updates `erikfryscok.com` references only. Renaming the external GitHub repository and implementing provider adapters in `ai-systems-lab` remain ERI-19 work in that repository.
- **Historical references:** Dated plans/specifications and the superseded decision remain unchanged or explicitly qualified; canonical rendered pages cannot use the former name or route.
- **Placeholder scan:** No deferred implementation markers or unspecified code steps remain.
- **Consistency check:** Every canonical link, source URL, fixture path, output path, metadata title, and display name uses `ai-systems-lab` / **AI Systems Lab**; the sole old route is the tested redirect.
