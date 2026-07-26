# Favicon and Site Logo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete, cross-platform favicon implementation and integrate the site logo into the navigation header.

**Architecture:** Three tasks — first create the `public/` directory and populate it with exported assets from the Illustrator source file, then add the Web App Manifest for PWA/home-screen support, then update `BaseLayout.astro` with all favicon `<link>` tags and replace the plain-text nav label with the SVG logo. All assets live in `public/` so Astro copies them to `dist/` during build.

**Tech Stack:** Astro 7, TypeScript (strict mode via `astro/tsconfigs/strict`), Tailwind CSS 4 (via `@tailwindcss/vite`), Node 24.

## File Structure

| File | Action | Responsibility |
| --- | --- | --- |
| `public/` | Create directory | Astro static assets directory — contents copied verbatim to `dist/` |
| `public/favicon.svg` | Create | Primary favicon for modern browsers (vector) |
| `public/favicon-16x16.png` | Create | 16×16 tab icon for legacy browsers |
| `public/favicon-32x32.png` | Create | 32×32 tab/bookmark icon for legacy browsers |
| `public/apple-touch-icon.png` | Create | 180×180 iOS home screen / Safari pinned tab icon |
| `public/logo.svg` | Create | Vector logo for navigation header |
| `public/manifest.json` | Create | Web App Manifest for Android Chrome home-screen installation |
| `src/components/BaseLayout.astro` | Modify | Add all favicon/link tags to `<head>`; replace nav text with logo SVG |
| `CHANGELOG.md` | Modify | Add entry under Unreleased → Added |
| `docs/strategy/decisions.md` | Modify | Add decision-log entry for favicon and logo approach |
| `docs/superpowers/plans/2026-07-25-favicon-and-logo.md` | Create | This plan document |
| `docs/README.md` | Modify | Add plan link to implementation plans section |

## Global Constraints

- Node.js `24.18.0` pinned in `.node-version`; engine range `>=24 <25` in `package.json`.
- Build command: `npm run build` (runs `check` + `astro build`).
- Check command: `npm run check` (runs `astro check && tsc --noEmit`).
- Branch naming: `erikf/issue-N-short-description`.
- PR must use `Closes #24` to link to the issue.
- Content boundaries: do not publish employer/client confidential info, credentials, or internal project details.
- Responsive breakpoints: mobile at `375px`, desktop at `1280px` — no horizontal overflow at either width.
- Astro default static output (no SSR adapter).
- Tailwind CSS 4 via `@tailwindcss/vite` plugin in `astro.config.mjs`; global styles in `src/styles/global.css` with `@import "tailwindcss"`.
- Every Astro file must import `src/styles/global.css` in its frontmatter to receive Tailwind utilities.
- No automated test framework exists; validation is via `npm run check`, `npm run build`, visual inspection, and `npm run preview`.
- The `public/` directory is Astro's static assets directory — files placed here are copied as-is to `dist/` during build.

---
### Task 1: Create public directory and add favicon assets

**Files:**
- Create: `public/` (directory)
- Create: `public/favicon.svg`
- Create: `public/favicon-16x16.png`
- Create: `public/favicon-32x32.png`
- Create: `public/apple-touch-icon.png`
- Create: `public/logo.svg`

**Interfaces:**
- Consumes: nothing from other tasks (this is the first task)
- Produces: static asset files in `public/` that Astro will copy to `dist/` during build

**Asset export instructions:**

Export the following from the Adobe Illustrator source file. The SVG should use a simple, clean design suitable for small sizes (16–32px). The PNG exports should have transparent backgrounds.

| File | Format | Dimensions | Export settings |
| --- | --- | --- | --- |
| `favicon.svg` | SVG | Vector | Export as SVG, preserve RGB colors, minimal code |
| `favicon-16x16.png` | PNG | 16×16 | Transparent background, high quality |
| `favicon-32x32.png` | PNG | 32×32 | Transparent background, high quality |
| `apple-touch-icon.png` | PNG | 180×180 | Transparent background, high quality |
| `logo.svg` | SVG | Vector (~48px viewBox height) | Clean vector, suitable for nav display at ~32–48px height |

- [ ] **Step 1: Export assets from Illustrator**

Open the Illustrator source file and export:

1. **`favicon.svg`** — File → Export → Export As → SVG. Use "SVG Options…" to set:
   - Styling: Presentation Attributes
   - Font: Convert to Outlines (if text-based logo)
   - Decimal Places: 3
   - Object IDs: Layer Names

2. **`favicon-16x16.png`** — File → Export → Export As → PNG. Set width to 16px (height auto-scales to 16px if square). Transparent background.

3. **`favicon-32x32.png`** — File → Export → Export As → PNG. Set width to 32px. Transparent background.

4. **`apple-touch-icon.png`** — File → Export → Export As → PNG. Set width to 180px. Transparent background.

5. **`logo.svg`** — File → Export → Export As → SVG. Same settings as favicon.svg. This is the same logo but may be optimized for larger display (nav header).

- [ ] **Step 2: Create the public directory and place assets**

```bash
mkdir -p public
# Copy exported files into public/:
# public/favicon.svg
# public/favicon-16x16.png
# public/favicon-32x32.png
# public/apple-touch-icon.png
# public/logo.svg
```

- [ ] **Step 3: Verify assets exist and are valid**

```bash
ls -la public/
file public/favicon.svg
file public/favicon-16x16.png
file public/favicon-32x32.png
file public/apple-touch-icon.png
file public/logo.svg
```

Expected: All five files present. SVG files show as XML/text. PNG files show as PNG image data with correct dimensions.

- [ ] **Step 4: Run build to verify assets are copied to dist/**

```bash
npm run build
```

Expected: Build succeeds. `dist/favicon.svg`, `dist/favicon-16x16.png`, `dist/favicon-32x32.png`, `dist/apple-touch-icon.png`, `dist/logo.svg` all exist in the output directory.

- [ ] **Step 5: Verify build output**

```bash
ls -la dist/favicon.svg dist/favicon-16x16.png dist/favicon-32x32.png dist/apple-touch-icon.png dist/logo.svg
```

Expected: All five files present in `dist/` with non-zero sizes.

- [ ] **Step 6: Commit**

```bash
git add public/
git commit -m "feat: add favicon and logo assets from Illustrator source (issue #24)"
```

---

### Task 2: Create Web App Manifest for PWA and home-screen support

**Files:**
- Create: `public/manifest.json`

**Interfaces:**
- Consumes: assets from Task 1 (`favicon-32x32.png`, `apple-touch-icon.png` referenced in manifest)
- Produces: `manifest.json` at root of `public/` that browsers discover via `<link rel="manifest">`

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
- `name` — full site name shown on home screens and in app drawers
- `short_name` — abbreviated name for space-constrained contexts
- `start_url` — root path; where the app opens from home screen
- `display` — `standalone` removes browser chrome for home-screen launches
- `background_color` — white, matching the site's `bg-white` base
- `theme_color` — `#2563eb` is Tailwind's `blue-600`, matching the site's primary accent color used in buttons and links
- `icons` — references the PNG assets from Task 1; `maskable` on the 180px icon enables adaptive icons on Android

- [ ] **Step 2: Validate the manifest JSON**

```bash
cat public/manifest.json | python3 -m json.tool > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

Expected: "Valid JSON"

- [ ] **Step 3: Run build to verify manifest is copied**

```bash
npm run build
```

Expected: Build succeeds. `dist/manifest.json` exists.

- [ ] **Step 4: Verify manifest in build output**

```bash
cat dist/manifest.json | python3 -m json.tool > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

Expected: "Valid JSON"

- [ ] **Step 5: Commit**

```bash
git add public/manifest.json
git commit -m "feat: add Web App Manifest for PWA and home-screen support (issue #24)"
```

---

### Task 3: Update BaseLayout with favicon links and logo in navigation

**Files:**
- Modify: `src/components/BaseLayout.astro` (lines 11-24)
- Modify: `CHANGELOG.md`
- Modify: `docs/strategy/decisions.md`
- Modify: `docs/README.md`

**Interfaces:**
- Consumes: assets from Task 1 (`favicon.svg`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `logo.svg`) and Task 2 (`manifest.json`)
- Produces: updated `BaseLayout.astro` with all favicon `<link>` tags and logo in nav; consumed by all pages via `BaseLayout` import

This task replaces the existing placeholder favicon link in `BaseLayout.astro` with a complete set of `<link>` tags, and replaces the plain-text nav label with the SVG logo.

- [ ] **Step 1: Update BaseLayout.astro with complete favicon links and logo**

Replace the entire file content of `src/components/BaseLayout.astro`:

```astro
---
import "../styles/global.css";

interface Props {
  title: string;
}

const { title } = Astro.props;
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
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
  </head>
  <body class="min-h-screen bg-white text-gray-900 flex flex-col">
    <header class="border-b border-gray-200">
      <nav class="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between" aria-label="Main navigation">
        <a href="/" class="flex items-center gap-2 text-lg font-semibold text-gray-900 hover:text-gray-600 transition-colors">
          <img src="/logo.svg" alt="Erik Fryscok" class="h-8 w-auto" />
        </a>
        <ul class="flex gap-6 list-none">
          <li><a href="/" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Home</a></li>
          <li><a href="/about" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">About</a></li>
          <li><a href="/writing" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Writing</a></li>
          <li><a href="/projects" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Projects</a></li>
          <li><a href="/contact" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Contact</a></li>
        </ul>
      </nav>
    </header>
    <main class="flex-1 max-w-3xl mx-auto px-4 py-8 w-full">
      <slot />
    </main>
    <footer class="border-t border-gray-200">
      <div class="max-w-3xl mx-auto px-4 py-4 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} Erik Fryscok. All rights reserved.
      </div>
    </footer>
  </body>
</html>
```

Key changes from the current file:
- **Lines 16-28:** Replaced single `<link rel="icon">` with full set: SVG favicon, two PNG favicons, Apple Touch Icon, manifest link, and theme-color meta tag
- **Lines 33-35:** Replaced plain-text `erikfryscok` with `<img>` tag referencing `/logo.svg`, wrapped in a `flex items-center gap-2` container. The `h-8` class sets the logo to 32px height, matching the existing `text-lg` sizing. `w-auto` preserves aspect ratio. `alt="Erik Fryscok"` provides accessible text.

- [ ] **Step 2: Run type and lint checks**

```bash
npm run check
```

Expected: PASS with no errors or warnings.

- [ ] **Step 3: Run build**

```bash
npm run build
```

Expected: PASS. `dist/` contains all HTML pages with the new `<link>` tags in `<head>`.

- [ ] **Step 4: Verify the built HTML contains all expected tags**

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

- [ ] **Step 5: Verify the logo appears in the nav**

```bash
grep 'logo.svg' dist/index.html
```

Expected: `<img src="/logo.svg" alt="Erik Fryscok" class="h-8 w-auto" />` present in the nav section.

- [ ] **Step 6: Start local preview and visual verification**

```bash
npm run preview
```

Open `http://localhost:4321` in a browser and verify:
- Browser tab shows the favicon (SVG in modern browsers, PNG fallback in others)
- Navigation header shows the logo image instead of plain text
- Logo is properly sized (~32px height) and aligned with nav links
- No layout overflow at 375px viewport width (use browser dev tools device emulation)
- No layout overflow at 1280px viewport width
- All nav links still functional and styled correctly
- Logo hover inherits the `hover:text-gray-600` color transition from the parent `<a>`

- [ ] **Step 7: Update CHANGELOG.md**

Add the following entries under the `## Unreleased` → `### Added` section in `CHANGELOG.md`, after the existing entries:

```
- Favicon with SVG, PNG, and Apple Touch Icon for cross-platform browser support (issue #24).
- Web App Manifest for Android Chrome home-screen installation (issue #24).
- Site logo in navigation header replacing plain-text brand (issue #24).
```

- [ ] **Step 8: Add decision-log entry**

Append the following row to the decision log table in `docs/strategy/decisions.md`:

```markdown
| 2026-07-25 | Use SVG as primary favicon with PNG fallbacks (16×16, 32×32), Apple Touch Icon (180×180), and Web App Manifest for complete cross-platform coverage. Logo SVG in nav header replaces plain-text brand. | SVG provides crisp rendering at any resolution; PNG fallbacks cover legacy browsers; Apple Touch Icon and manifest enable home-screen installation on iOS and Android. All assets exported from a single Illustrator source. | Chosen |
```

- [ ] **Step 9: Update docs/README.md**

Add the plan link to the "Implementation plans" section in `docs/README.md`. Insert this line after the existing plans entries (after the issue #22 entry on line 35) to maintain chronological order:

```markdown
  - [GitHub issue #24: Favicon and site logo](superpowers/plans/2026-07-25-favicon-and-logo.md) — cross-platform favicon implementation and navigation logo integration.
```

- [ ] **Step 10: Final build verification**

```bash
npm run build
```

Expected: PASS with no errors. All pages in `dist/` contain the updated head tags and logo.

- [ ] **Step 11: Commit**

```bash
git add src/components/BaseLayout.astro CHANGELOG.md docs/strategy/decisions.md docs/README.md docs/superpowers/plans/2026-07-25-favicon-and-logo.md
git commit -m "feat: wire up favicon links and nav logo in BaseLayout (issue #24)"
```

---

## Self-Review

**1. Spec coverage:**
- Scalable SVG favicon: Task 1 (`favicon.svg`), Task 3 (linked in BaseLayout)
- Multiple sizes for all scenarios: Task 1 (16×16 PNG, 32×32 PNG, 180×180 Apple Touch Icon), Task 2 (manifest with icon array)
- Logo added to site: Task 1 (`logo.svg`), Task 3 (nav `<img>` tag replacing plain text)
- iOS home-screen support: Task 1 (`apple-touch-icon.png`), Task 3 (`<link rel="apple-touch-icon">`)
- Android Chrome home-screen: Task 2 (`manifest.json`), Task 3 (`<link rel="manifest">`)
- Safari pinned tab: Task 1 (SVG favicon + `apple-touch-icon.png`)
- Legacy browser support: Task 1 (PNG favicons), Task 3 (`<link rel="icon" type="image/png">`)
- Visual verification at 375px and 1280px: Task 3, Step 6
- `npm run build` produces valid `dist/`: Task 1 Step 4, Task 2 Step 3, Task 3 Step 3 and 10
- `npm run check` passes: Task 3 Step 2
- CHANGELOG.md updated: Task 3 Step 7
- Decision log updated: Task 3 Step 8
- docs/README.md updated: Task 3 Step 9
- Implementation plan saved: this document

**2. Placeholder scan:**
- No "TBD", "TODO", or "implement later"
- No vague "add validation" — each validation step has explicit commands and expected output
- No "write tests" without test code — N/A for static Astro; build, check, and visual verification serve as the test cycle
- No "similar to Task N" — each step is fully self-contained
- All file paths are explicit and absolute within the repo
- All code blocks contain complete, copyable content

**3. Type/signature consistency:**
- `BaseLayout` props interface unchanged (`{ title: string }`) — no breaking change for consuming pages
- Nav `<a>` tag now uses `flex items-center gap-2` class — existing `text-lg font-semibold text-gray-900 hover:text-gray-600 transition-colors` classes preserved
- Logo `h-8` (32px) matches existing nav text sizing at `text-lg` (18px) with visual breathing room
- All `<link>` `href` paths use absolute URLs (`/favicon.svg`, etc.) matching Astro's `public/` convention
- Manifest `theme_color` (`#2563eb`) matches Tailwind `blue-600` used in buttons and links across the site

**4. Consistency with existing conventions:**
- Branch naming: `erikf/issue-24-favicon-and-logo` matches `erikf/issue-N-short-description`
- Assets in `public/` — standard Astro convention for static files
- `BaseLayout.astro` modification — existing file, follows established patterns
- Tailwind utilities for styling — matches existing pattern
- `Closes #24` in PR — matches delivery contract
- Plan saved to `docs/superpowers/plans/` — matches existing plan naming convention

**5. Boundary check:**
- Does NOT modify `astro.config.mjs` (no new integrations needed)
- Does NOT add new npm dependencies (manifest and favicons are pure static assets)
- Does NOT add analytics, MDX, or other deferred features
- Does NOT modify page content — only layout and assets
- Does NOT add server-side functionality — fully static

---

## Execution Recommendation

**Subagent-Driven (recommended)** — dispatch a fresh subagent per task using `superpowers:subagent-driven-development`. Tasks must execute in order (1 → 2 → 3) due to dependencies. Two-stage review between tasks catches interface mismatches early.

**Inline Execution** — execute tasks sequentially in this session using `superpowers:executing-plans` with checkpoints for review.

