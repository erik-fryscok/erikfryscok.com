# Home Hero Portrait Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Erik's supplied portrait to the Home page hero in a responsive, optimized, and accessible treatment.

**Architecture:** Import the source JPEG through Astro's asset pipeline and render it with the `Image` component so the production build emits an optimized WebP. Convert only the existing hero section to a responsive two-column grid; all other Home page content remains unchanged. Add a Node integration test that validates the real built output rather than source text.

**Tech Stack:** Astro 7, TypeScript strict mode, Tailwind CSS 4, Node.js built-in test runner, Node 24.

## Global Constraints

- Related work: [GitHub issue #33](https://github.com/erik-fryscok/erikfryscok.com/issues/33).
- Approved design: `docs/superpowers/specs/2026-08-07-home-hero-portrait-design.md`.
- Node.js `24.18.0` is pinned in `.node-version`; `package.json` allows `>=24 <25`.
- Preserve the existing Home hero headline and supporting copy verbatim.
- Do not modify the Home page introduction, selected work, contact CTA, shared layout, or other routes.
- Use the supplied image without retouching or generative edits.
- Content must not expose employer/client confidential information, credentials, or internal project details.
- Validate at 375px and 1280px widths with no horizontal overflow.
- The pull request must include `Closes #33`.

---

### Task 1: Add the tested responsive portrait treatment

**Files:**
- Modify: `package.json`
- Create: `tests/home-hero.test.mjs`
- Create: `src/assets/erik-fryscok-portrait.jpg`
- Modify: `src/pages/index.astro`

**Interfaces:**
- Consumes: `/Users/erik/Documents/profile-pic-2026-ai-zoomed-1024x1024.jpg` as the approved source image.
- Produces: an optimized Home hero portrait in the built `/index.html` and a repeatable `npm test` command.

- [ ] **Step 1: Add the failing integration test and test command**

Add this script to `package.json`:

```json
"test": "npm run build && node --test tests/*.test.mjs"
```

Create `tests/home-hero.test.mjs`:

```js
import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);
const expectedAlt =
  "Erik Fryscok smiling outdoors with a city street in the background.";

test("the built Home page serves Erik's optimized portrait", async () => {
  const html = await readFile(new URL("dist/index.html", projectRoot), "utf8");
  const imageTags = html.match(/<img\b[^>]*>/g) ?? [];
  const portrait = imageTags.find((tag) => tag.includes(`alt="${expectedAlt}"`));

  assert.ok(portrait, "expected the Home page to contain Erik's portrait");

  const source = portrait.match(/src="([^"]+)"/)?.[1];
  assert.match(source ?? "", /^\/_astro\/erik-fryscok-portrait\.[^/]+\.webp$/);
  await access(new URL(`dist${source}`, projectRoot));
});
```

- [ ] **Step 2: Run the test and confirm the expected failure**

Run:

```bash
npm test
```

Expected: the build succeeds, then the test fails with `expected the Home page to contain Erik's portrait` because the Home page does not render the image yet.

- [ ] **Step 3: Copy the approved source image into Astro's managed assets**

```bash
mkdir -p src/assets
cp /Users/erik/Documents/profile-pic-2026-ai-zoomed-1024x1024.jpg src/assets/erik-fryscok-portrait.jpg
```

Verify it remains a 1024×1024 JPEG:

```bash
file src/assets/erik-fryscok-portrait.jpg
```

- [ ] **Step 4: Implement the minimal Home hero change**

Add these imports to `src/pages/index.astro` frontmatter:

```astro
import { Image } from "astro:assets";
import portrait from "../assets/erik-fryscok-portrait.jpg";
```

Replace only the existing Hero Section with:

```astro
<!-- Hero Section -->
<section class="mb-16 grid gap-8 md:grid-cols-[minmax(0,1fr)_16rem] md:items-center md:gap-10">
  <div>
    <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
      Building better software teams with AI, automation, and modern engineering practices.
    </h1>
    <p class="mt-4 text-lg leading-relaxed text-gray-600 max-w-3xl">
      I'm a software development team lead focused on engineering leadership,
      AI-enabled development, cloud infrastructure, documentation, and practical
      systems that help teams work more effectively.
    </p>
  </div>
  <Image
    src={portrait}
    alt="Erik Fryscok smiling outdoors with a city street in the background."
    width={512}
    height={512}
    format="webp"
    quality={80}
    loading="eager"
    fetchpriority="high"
    class="mx-auto aspect-square w-full max-w-64 rounded-2xl object-cover shadow-sm md:mx-0"
  />
</section>
```

- [ ] **Step 5: Run the integration test and confirm it passes**

```bash
npm test
```

Expected: Astro checks and build pass; the Node test reports 1 passing test and the emitted WebP exists under `dist/_astro/`.

- [ ] **Step 6: Commit the tested feature**

```bash
git add package.json tests/home-hero.test.mjs src/assets/erik-fryscok-portrait.jpg src/pages/index.astro
git commit -m "feat: add portrait to home hero (issue #33)"
```

---

### Task 2: Document and visually verify the placement decision

**Files:**
- Modify: `docs/strategy/decisions.md`
- Modify: `docs/README.md`
- Modify: `CHANGELOG.md`
- Create: `docs/superpowers/plans/2026-08-07-home-hero-portrait.md`

**Interfaces:**
- Consumes: the completed Home hero from Task 1 and the approved design spec.
- Produces: durable rationale, release notes, indexed implementation documentation, and browser evidence at both acceptance widths.

- [ ] **Step 1: Record the durable placement decision**

Append this row to `docs/strategy/decisions.md`:

```markdown
| 2026-08-07 | Place Erik's portrait in the Home hero rather than the Contact page, using Astro's managed image pipeline. | The Home placement humanizes the first impression and balances the text-heavy hero; the Contact page remains focused on outreach methods. Astro-managed WebP output reduces image transfer size while retaining the source asset in Git. | Chosen |
```

- [ ] **Step 2: Index the implementation plan**

Add this entry under “Implementation plans” in `docs/README.md`:

```markdown
- [GitHub issue #33: Home hero portrait](superpowers/plans/2026-08-07-home-hero-portrait.md) — responsive, optimized portrait placement in the Home page hero.
```

- [ ] **Step 3: Update the changelog**

Add this entry under `Unreleased` → `Added` in `CHANGELOG.md`:

```markdown
- Responsive, optimized portrait in the Home page hero (issue #33).
```

- [ ] **Step 4: Run final automated verification on Node 24**

Run the test command with the configured Node 24 runtime, then check formatting and repository state:

```bash
npm test
git diff --check
git status --short
```

Expected: 1 passing test, 0 Astro/TypeScript diagnostics, 7 static pages built, no whitespace errors, and only the intended documentation files remain uncommitted.

- [ ] **Step 5: Verify the responsive design in a local browser**

Run the production preview and inspect `/` at 375×812 and 1280×800.

At 375px verify:

- hero copy appears before the centered portrait;
- portrait width is at most 256px;
- there is no horizontal overflow;
- the existing mobile navigation remains usable.

At 1280px verify:

- portrait appears to the right of the hero copy;
- portrait renders as a 256px square with rounded corners;
- headline and copy remain legible without overlap;
- About begins below the hero with the existing spacing.

- [ ] **Step 6: Commit the documentation**

```bash
git add CHANGELOG.md docs/README.md docs/strategy/decisions.md docs/superpowers/plans/2026-08-07-home-hero-portrait.md
git commit -m "docs: record home hero portrait change (issue #33)"
```

- [ ] **Step 7: Publish for review**

Run the full test command once more, push `codex/issue-33-home-hero`, and open a draft pull request to `main` with `Closes #33`, a concise change summary, and the validation evidence.
