# Favicon and Site Logo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete, cross-platform favicon implementation and integrate the site logo into the navigation header, preserving the existing mobile navigation.

**Architecture:** Three tasks — first move the existing image assets from `src/public/` to `public/` (Astro's default static directory) so they are served correctly, then create the Web App Manifest for PWA/home-screen support, then make targeted modifications to `BaseLayout.astro` (replacing only the placeholder favicon link and the plain-text nav label — NOT replacing the entire file, to preserve the mobile navigation from issue #25). Documentation updates are folded into the final task.

**Tech Stack:** Astro 7, TypeScript (strict mode via `astro/tsconfigs/strict`), Tailwind CSS 4 (via `@tailwindcss/vite`), Node 24.

## Global Constraints

- Node.js `24.18.0` pinned in `.node-version`; engine range `>=24 <25` in `package.json`.
- Build command: `npm run build` (runs `npm run check` + `astro build`).
- Check command: `npm run check` (runs `astro check && tsc --noEmit`).
- Preview command: `npm run preview` (serves `dist/` on `http://localhost:4321`).
- Branch naming: `erikf/issue-N-short-description`.
- PR must use `Closes #24` to link to the issue.
- Content boundaries: do not publish employer/client confidential info, credentials, or internal project details.
- Responsive breakpoints: mobile at `375px`, desktop at `1280px` — no horizontal overflow at either width.
- Astro default static output (no SSR adapter); default `publicDir` is `public/` at project root (no custom config in `astro.config.mjs`).
- Tailwind CSS 4 via `@tailwindcss/vite` plugin in `astro.config.mjs`; global styles in `src/styles/global.css` with `@import "tailwindcss"`.
- Every Astro file must import `src/styles/global.css` in its frontmatter to receive Tailwind utilities.
- No automated test framework exists; validation is via `npm run check`, `npm run build`, visual inspection, and `npm run preview`.
- The `public/` directory is Astro's static assets directory — files placed here are copied as-is to `dist/` during build.
- **CRITICAL:** `BaseLayout.astro` contains mobile navigation (hamburger menu, inline toggle script, overlay behavior) from issue #25. Modifications must be targeted line replacements — do NOT replace the entire file.

## File Structure

| File | Action | Responsibility |
| --- | --- | --- |
| `public/` | Create directory | Astro static assets directory — contents copied verbatim to `dist/` |
| `public/favicon.svg` | Move from `src/public/` | Primary favicon for modern browsers (vector) |
| `public/favicon-16x16.png` | Move from `src/public/` | 16×16 tab icon for legacy browsers |
| `public/favicon-32x32.png` | Move from `src/public/` | 32×32 tab/bookmark icon for legacy browsers |
| `public/apple-touch-icon.png` | Move from `src/public/` | 180×180 iOS home screen / Safari pinned tab icon |
| `public/logo.svg` | Move from `src/public/` | Vector logo for navigation header |
| `public/manifest.json` | Create | Web App Manifest for Android Chrome home-screen installation |
| `src/components/BaseLayout.astro` | Modify (targeted) | Add favicon/link tags to `<head>` (line 16); replace nav text with logo `<img>` (lines 22–24) |
| `CHANGELOG.md` | Modify | Add entries under Unreleased → Added |
| `docs/strategy/decisions.md` | Modify | Add decision-log entry for favicon and logo approach |
| `docs/superpowers/plans/2026-07-31-favicon-and-logo.md` | Create | This plan document |
| `docs/README.md` | Modify | Update plan link from 2026-07-25 to 2026-07-31 |
| `docs/superpowers/plans/2026-07-25-favicon-and-logo.md` | Delete | Superseded by this plan — remove to avoid duplicate |

---

### Task 1: Move assets to `public/` and verify build

**Files:**
- Create: `public/` (directory)
- Move: `src/public/favicon.svg` → `public/favicon.svg`
- Move: `src/public/favicon-16x16.png` → `public/favicon-16x16.png`
- Move: `src/public/favicon-32x32.png` → `public/favicon-32x32.png`
- Move: `src/public/apple-touch-icon.png` → `public/apple-touch-icon.png`
- Move: `src/public/logo.svg` → `public/logo.svg`

**Interfaces:**
- Consumes: nothing from other tasks (this is the first task)
- Produces: static asset files in `public/` that Astro will copy to `dist/` during build; consumed by Tasks 2 and 3

The 5 image assets already exist in `src/public/` (exported from the Illustrator source file in a prior session). Astro's default `publicDir` is `public/` at the project root — files in `src/public/` are NOT served as static assets. This task moves them to the correct location.

- [ ] **Step 1: Create `public/` directory and move assets with `git mv`**

```bash
mkdir -p public
git mv src/public/favicon.svg public/favicon.svg
git mv src/public/favicon-16x16.png public/favicon-16x16.png
git mv src/public/favicon-32x32.png public/favicon-32x32.png
git mv src/public/apple-touch-icon.png public/apple-touch-icon.png
git mv src/public/logo.svg public/logo.svg
```

- [ ] **Step 2: Remove the now-empty `src/public/` directory**

```bash
rmdir src/public
```

If `rmdir` fails (directory not empty), check for hidden files:
```bash
ls -la src/public/
```
Remove any remaining files (e.g., `.DS_Store`) and retry `rmdir`.

- [ ] **Step 3: Verify assets exist in `public/` and are valid**

```bash
ls -la public/
file public/favicon.svg
file public/favicon-16x16.png
file public/favicon-32x32.png
file public/apple-touch-icon.png
file public/logo.svg
```

Expected: All five files present in `public/`. SVG files show as XML/text. PNG files show as PNG image data with correct dimensions (16×16, 32×32, 180×180).

- [ ] **Step 4: Run build to verify assets are copied to `dist/`**

```bash
npm run build
```

Expected: Build succeeds (check + astro build). No errors.

- [ ] **Step 5: Verify build output contains all assets**

```bash
ls -la dist/favicon.svg dist/favicon-16x16.png dist/favicon-32x32.png dist/apple-touch-icon.png dist/logo.svg
```

Expected: All five files present in `dist/` with non-zero sizes.

- [ ] **Step 6: Commit**

```bash
git add public/
git commit -m "feat: move favicon and logo assets to public/ directory (issue #24)"
```

---

### Task 2: Create Web App Manifest for PWA and home-screen support

**Files:**
- Create: `public/manifest.json`

**Interfaces:**
- Consumes: PNG assets from Task 1 (`favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png` referenced in manifest `icons` array)
- Produces: `manifest.json` at root of `public/` that browsers discover via `<link rel="manifest">` (added in Task 3)

The Web App Manifest enables Android Chrome home-screen installation and provides metadata for bookmarking, sharing, and browser display. It references the PNG icons from Task 1.

- [ ] **Step 1: Create the manifest file**

Create `public/manifest.json` with the following content:

```json
{
  "name": "Erik Fryscok — Software Engineering Leadership",
  "short_name": "Erik Fryscok",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2563eb",
  "icons": [
    {
      "src": "/favicon-16x16.png",
      "sizes": "16x16",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/favicon-32x32.png",
      "sizes": "32x32",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/apple-touch-icon.png",
      "sizes": "180x180",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

Notes on the values:
- `name` — full site name, matches the `<title>` in `index.astro`: `"Erik Fryscok — Software Engineering Leadership"`
- `short_name` — abbreviated name for space-constrained contexts (home screen icons)
- `start_url` — root path; where the app opens from home screen
- `display` — `standalone` removes browser chrome for home-screen launches
- `background_color` — white, matching the site's `bg-white` base in `BaseLayout.astro`
- `theme_color` — `#2563eb` is Tailwind's `blue-600`, the site's primary accent color used in buttons (`bg-blue-600`) and links (`text-blue-600`) across all pages
- `icons` — references the PNG assets from Task 1; `maskable` on the 180px icon enables adaptive icons on Android

- [ ] **Step 2: Validate the manifest JSON**

```bash
python3 -m json.tool public/manifest.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

Expected: `Valid JSON`

- [ ] **Step 3: Run build to verify manifest is copied to `dist/`**

```bash
npm run build
```

Expected: Build succeeds. `dist/manifest.json` exists.

- [ ] **Step 4: Verify manifest in build output**

```bash
python3 -m json.tool dist/manifest.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

Expected: `Valid JSON`

- [ ] **Step 5: Commit**

```bash
git add public/manifest.json
git commit -m "feat: add Web App Manifest for PWA and home-screen support (issue #24)"
```

---

### Task 3: Update BaseLayout with favicon links, nav logo, and documentation

**Files:**
- Modify: `src/components/BaseLayout.astro` (line 16 — head favicon link; lines 22–24 — nav label)
- Modify: `CHANGELOG.md`
- Modify: `docs/strategy/decisions.md`
- Modify: `docs/README.md` (line 37 — plan link)
- Delete: `docs/superpowers/plans/2026-07-25-favicon-and-logo.md` (superseded)
- Create: `docs/superpowers/plans/2026-07-31-favicon-and-logo.md` (this plan)

**Interfaces:**
- Consumes: assets from Task 1 (`favicon.svg`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `logo.svg`) and Task 2 (`manifest.json`)
- Produces: updated `BaseLayout.astro` with all favicon `<link>` tags and logo in nav; consumed by all pages via `BaseLayout` import

This task makes two targeted modifications to `BaseLayout.astro`. It does NOT replace the entire file — the mobile navigation (hamburger button, dropdown menu, inline toggle script, keyboard/overlay handlers) from issue #25 must be preserved.

**Current `BaseLayout.astro` structure (112 lines):**
- Lines 1–9: Frontmatter (imports, Props interface)
- Lines 11–18: `<head>` with placeholder favicon link on line 16
- Lines 20–49: `<header>` with nav (plain-text label on lines 22–24, hamburger button, mobile menu)
- Lines 50–52: `<main>` with slot
- Lines 53–57: `<footer>`
- Lines 58–110: `<script is:inline>` for mobile menu toggle
- Lines 111–112: closing tags

- [ ] **Step 1: Replace the placeholder favicon link in the `<head>`**

In `src/components/BaseLayout.astro`, find this block (lines 15–17):

```astro
    <meta name="description" content="Erik Fryscok — software engineering leadership, AI-enabled development, and modern practices." />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title}</title>
```

Replace it with:

```astro
    <meta name="description" content="Erik Fryscok — software engineering leadership, AI-enabled development, and modern practices." />

    <!-- Primary favicon (modern browsers) -->
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />

    <!-- Legacy browser favicons -->
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />

    <!-- Apple Touch Icon (iOS home screen, Safari pinned tab) -->
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

    <!-- Web App Manifest (Android Chrome home screen) -->
    <link rel="manifest" href="/manifest.json" />

    <!-- Theme color for browser chrome -->
    <meta name="theme-color" content="#2563eb" />

    <title>{title}</title>
```

Key changes:
- Single placeholder `<link>` replaced with full set: SVG favicon, two PNG favicons, Apple Touch Icon, manifest link, and `theme-color` meta tag
- `theme-color` value `#2563eb` matches Tailwind `blue-600` used in buttons and links across all pages
- All `href` paths use absolute URLs (`/favicon.svg`, etc.) matching Astro's `public/` convention

- [ ] **Step 2: Replace the plain-text nav label with the logo image**

In `src/components/BaseLayout.astro`, find this block (lines 22–24):

```astro
        <a href="/" class="text-lg font-semibold text-gray-900 hover:text-gray-600 transition-colors">
          erikfryscok
        </a>
```

Replace it with:

```astro
        <a href="/" class="flex items-center gap-2 text-lg font-semibold text-gray-900 hover:text-gray-600 transition-colors">
          <img src="/logo.svg" alt="Erik Fryscok" class="h-8 w-auto" />
        </a>
```

Key changes:
- Added `flex items-center gap-2` to the `<a>` class to center the image vertically
- Replaced text `erikfryscok` with `<img>` tag: `src="/logo.svg"`, `alt="Erik Fryscok"`, `class="h-8 w-auto"`
- `h-8` sets logo height to 32px, consistent with the existing `text-lg` (18px) nav sizing with visual breathing room
- `w-auto` preserves the SVG's aspect ratio
- `alt="Erik Fryscok"` provides accessible text for screen readers
- Existing `text-lg font-semibold text-gray-900 hover:text-gray-600 transition-colors` classes preserved on the `<a>` tag
- **Do NOT modify any other part of the file** — the hamburger button, mobile menu `<ul>`, inline script, and all other elements must remain unchanged

- [ ] **Step 3: Run type and lint checks**

```bash
npm run check
```

Expected: PASS with no TypeScript or Astro errors.

- [ ] **Step 4: Run build**

```bash
npm run build
```

Expected: PASS. `dist/` contains all HTML pages with the new `<link>` tags in `<head>`.

- [ ] **Step 5: Verify the built HTML contains all expected head tags**

```bash
grep -A 20 '<head>' dist/index.html
```

Expected output includes all these tags:
```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#2563eb" />
```

- [ ] **Step 6: Verify the logo appears in the nav and mobile nav is preserved**

```bash
grep 'logo.svg' dist/index.html
```

Expected: `<img src="/logo.svg" alt="Erik Fryscok" class="h-8 w-auto" />` present in the nav section.

```bash
grep 'mobile-menu-toggle' dist/index.html
```

Expected: `id="mobile-menu-toggle"` present — confirms the mobile navigation was NOT removed.

```bash
grep 'menu-icon-close' dist/index.html
```

Expected: `id="menu-icon-close"` present — confirms the hamburger close icon was preserved.

- [ ] **Step 7: Start local preview and visual verification**

```bash
npm run preview
```

Open `http://localhost:4321` in a browser and verify:

**Favicon:**
- Browser tab shows the favicon (SVG in modern browsers, PNG fallback in others)

**Navigation logo:**
- Navigation header shows the logo image instead of plain text "erikfryscok"
- Logo is properly sized (~32px height) and aligned with nav links
- Logo hover inherits the `hover:text-gray-600` color transition from the parent `<a>`

**Mobile navigation (must still work — issue #25 regression check):**
- At 375px viewport width (use browser dev tools device emulation):
  - Hamburger button is visible, logo is visible
  - Click hamburger: menu drops down vertically, icon changes to X
  - Click a nav link: menu closes
  - Click outside menu: menu closes
  - Press Escape: menu closes, focus returns to button
  - No horizontal layout overflow
- At 1280px viewport width:
  - Hamburger button is hidden, horizontal nav links visible
  - Logo and links are properly aligned
  - No horizontal layout overflow

- [ ] **Step 8: Update CHANGELOG.md**

Add the following entries under `## Unreleased` → `### Added` in `CHANGELOG.md`, after the last existing entry in that section (after the OpenCode configuration entry):

```markdown
- Favicon with SVG, PNG, and Apple Touch Icon for cross-platform browser support (issue #24).
- Web App Manifest for Android Chrome home-screen installation (issue #24).
- Site logo in navigation header replacing plain-text brand (issue #24).
```

- [ ] **Step 9: Add decision-log entry**

Append the following row to the decision log table in `docs/strategy/decisions.md` (after the last row):

```markdown
| 2026-07-31 | Use SVG as primary favicon with PNG fallbacks (16×16, 32×32), Apple Touch Icon (180×180), and Web App Manifest for cross-platform coverage. Logo SVG in nav header replaces plain-text brand. Assets served from Astro's default `public/` directory. | SVG provides crisp rendering at any resolution; PNG fallbacks cover legacy browsers; Apple Touch Icon and manifest enable home-screen installation on iOS and Android. `public/` is Astro's convention for static assets, copied verbatim to `dist/` during build. | Chosen |
```

- [ ] **Step 10: Update `docs/README.md` plan link**

In `docs/README.md`, find this line (line 37):

```markdown
- [GitHub issue #24: Favicon and site logo](superpowers/plans/2026-07-25-favicon-and-logo.md) — cross-platform favicon implementation and navigation logo integration.
```

Replace it with:

```markdown
- [GitHub issue #24: Favicon and site logo](superpowers/plans/2026-07-31-favicon-and-logo.md) — cross-platform favicon implementation and navigation logo integration.
```

- [ ] **Step 11: Remove the superseded plan file**

```bash
git rm docs/superpowers/plans/2026-07-25-favicon-and-logo.md
```

This removes the outdated plan that would have overwritten the mobile navigation. The new plan at `2026-07-31-favicon-and-logo.md` supersedes it.

- [ ] **Step 12: Final build verification**

```bash
npm run build
```

Expected: PASS with no errors. All pages in `dist/` contain the updated head tags, logo, and preserved mobile navigation.

- [ ] **Step 13: Commit**

```bash
git add src/components/BaseLayout.astro CHANGELOG.md docs/strategy/decisions.md docs/README.md docs/superpowers/plans/2026-07-31-favicon-and-logo.md
git commit -m "feat: wire up favicon links and nav logo in BaseLayout (issue #24)"
```

---

## Self-Review

**1. Spec coverage (issue #24 acceptance criteria):**
- SVG favicon in `public/favicon.svg`: Task 1 (moved from `src/public/`), Task 3 (linked in BaseLayout)
- PNG favicons at 16×16 and 32×32: Task 1 (moved), Task 3 (linked with `sizes` attributes)
- Apple Touch Icon 180×180: Task 1 (moved), Task 3 (`<link rel="apple-touch-icon">`)
- Web App Manifest `manifest.json`: Task 2 (created), Task 3 (`<link rel="manifest">`)
- All favicon and manifest tags in `BaseLayout.astro`: Task 3, Step 1
- Logo SVG in nav header replacing plain-text "erikfryscok": Task 1 (moved `logo.svg`), Task 3, Step 2
- `npm run build` produces valid `dist/`: Task 1 Step 4, Task 2 Step 3, Task 3 Steps 4 and 12
- `npm run check` passes: Task 3 Step 3
- Visual verification at 375px and 1280px: Task 3 Step 7
- CHANGELOG.md updated under Unreleased → Added: Task 3 Step 8
- Decision log entry: Task 3 Step 9
- Implementation plan saved to `docs/superpowers/plans/`: this document (Task 3 commits it)
- `docs/README.md` updated with plan link: Task 3 Step 10

**2. Placeholder scan:**
- No "TBD", "TODO", or "implement later"
- No vague "add validation" — each verification step has explicit commands and expected output
- No "write tests" without test code — N/A for static Astro; build, check, grep verification, and visual inspection serve as the test cycle
- No "similar to Task N" — each step is fully self-contained with complete code
- All file paths are explicit within the repo
- All code blocks contain complete, copyable content

**3. Type/signature consistency:**
- `BaseLayout` Props interface unchanged (`{ title: string }`) — no breaking change for consuming pages
- Nav `<a>` tag adds `flex items-center gap-2` to existing class string — all other classes preserved
- Logo `h-8` (32px) is consistent with existing `text-lg` (18px) nav sizing
- All `<link>` `href` paths use absolute URLs (`/favicon.svg`, etc.) matching Astro's `public/` convention
- Manifest `theme_color` (`#2563eb`) matches Tailwind `blue-600` used in `bg-blue-600` and `text-blue-600` across all pages
- Manifest `name` matches `<title>` in `index.astro`: `"Erik Fryscok — Software Engineering Leadership"`
- Element IDs (`mobile-menu-toggle`, `mobile-menu`, `menu-icon-open`, `menu-icon-close`) are NOT modified — inline script continues to work unchanged

**4. Consistency with existing conventions:**
- Branch naming: `erikf/issue-24-favicon-and-logo` matches `erikf/issue-N-short-description`
- Assets in `public/` — standard Astro convention for static files
- `BaseLayout.astro` targeted modification — preserves existing file structure and mobile navigation
- Tailwind utilities for styling — matches existing pattern
- `Closes #24` in PR — matches delivery contract
- Plan saved to `docs/superpowers/plans/` — matches existing plan naming convention
- Old plan removed to avoid duplicate (AGENTS.md: "Do not create duplicate Markdown roadmaps")

**5. Boundary check:**
- Does NOT modify `astro.config.mjs` (no new integrations or config needed)
- Does NOT add new npm dependencies (manifest and favicons are pure static assets)
- Does NOT add analytics, MDX, or other deferred features
- Does NOT modify page content — only layout head and nav label
- Does NOT add server-side functionality — fully static
- Does NOT modify the mobile navigation — only head and nav `<a>` tag are touched
- Does NOT create a `favicon.ico` for IE — not in issue scope; potential follow-up

**6. Regression risk — mobile navigation (issue #25):**
- The existing plan (2026-07-25) would have replaced the entire `BaseLayout.astro`, deleting the hamburger menu, inline script, and overlay behavior. This plan makes only two targeted replacements (head link, nav label) and explicitly verifies the mobile nav survives the build (Step 6 grep checks for `mobile-menu-toggle` and `menu-icon-close`).

---

## Execution Recommendation

**Model and reasoning level:** A local open-weight model at medium reasoning level is sufficient. The task is straightforward — file moves, JSON creation, and two targeted HTML modifications. The primary risk (preserving mobile navigation) is mitigated by the plan's explicit grep verification steps. Per the decision log (2026-07-24), local inference is the coding baseline; no paid inference is required.

**Subagent-Driven (recommended)** — dispatch a fresh subagent per task using `superpowers:subagent-driven-development`. Tasks must execute in order (1 → 2 → 3) due to dependencies. Two-stage review between tasks catches interface mismatches early. Task 3 requires the most careful review — verify the mobile navigation is preserved.

**Inline Execution** — execute tasks sequentially in this session using `superpowers:executing-plans` with checkpoints for review.
