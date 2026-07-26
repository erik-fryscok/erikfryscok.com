# Mobile Navigation Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the navigation bar's mobile experience so links no longer overlap the site name or run off-screen, and provide a clean, accessible hamburger menu for narrow viewports.

**Architecture:** Refactor the nav in `BaseLayout.astro` to use a hamburger toggle button on mobile (hidden on desktop) that reveals a vertical menu, while keeping the existing horizontal row on desktop. Uses Astro's `is:inline` script with Tailwind responsive utilities (`hidden`, `lg:flex`, `lg:hidden`) for minimal client-side interactivity.

**Tech Stack:** Astro 7, TypeScript (strict mode), Tailwind CSS 4 (via `@tailwindcss/vite`), Node 24.

## Global Constraints

- Node.js `24.18.0` pinned in `.node-version`; engine range `>=24 <25` in `package.json`.
- Build command: `npm run build` (runs `check` + `astro build`).
- Check command: `npm run check` (runs `astro check && tsc --noEmit`).
- Branch naming: `erikf/issue-N-short-description`.
- PR must use `Closes #25` to link to the issue.
- Content boundaries: do not publish employer/client confidential info, credentials, or internal project details.
- Responsive breakpoints: mobile at `375px`, desktop at `1280px` — no horizontal overflow at either width.
- Astro default static output (no SSR adapter).
- Tailwind CSS 4 via `@tailwindcss/vite` plugin in `astro.config.mjs`; global styles in `src/styles/global.css` with `@import "tailwindcss"`.
- Every Astro file must import `src/styles/global.css` in its frontmatter to receive Tailwind utilities.
- Client-side interactivity uses Astro `is:inline` scripts (no client component hydration).

---

### Task 1: Add hamburger menu toggle button

**Files:**
- Modify: `src/components/BaseLayout.astro` (nav section, lines 21-32)

**Interfaces:**
- Consumes: existing `BaseLayout` component structure
- Produces: hamburger button with `id="mobile-menu-toggle"`, `aria-expanded`, `aria-controls`, and inline SVG icons for open/close states

The hamburger button replaces the visible nav links on mobile. It uses Tailwind responsive utilities to be visible only below `lg:` (1024px).

- [ ] **Step 1: Add the hamburger toggle button to the nav**

Edit `src/components/BaseLayout.astro`. Replace the entire `<nav>` element (lines 21-32) with:

```astro
<nav class="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between" aria-label="Main navigation">
  <a href="/" class="text-lg font-semibold text-gray-900 hover:text-gray-600 transition-colors">
    erikfryscok
  </a>
  <button
    id="mobile-menu-toggle"
    class="lg:hidden p-2 text-gray-600 hover:text-gray-900 transition-colors"
    aria-expanded="false"
    aria-controls="mobile-menu"
    aria-label="Toggle navigation menu"
  >
    <!-- Open icon (hamburger) -->
    <svg id="menu-icon-open" class="h-6 w-6 block" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
    <!-- Close icon (X) -->
    <svg id="menu-icon-close" class="h-6 w-6 hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  </button>
  <ul class="hidden lg:flex gap-6 list-none" id="mobile-menu">
    <li><a href="/" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Home</a></li>
    <li><a href="/about" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">About</a></li>
    <li><a href="/writing" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Writing</a></li>
    <li><a href="/projects" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Projects</a></li>
    <li><a href="/contact" class="text-sm text-gray-600 hover:text-gray-900 transition-colors">Contact</a></li>
  </ul>
</nav>
```

Key changes:
- The `<button>` has `lg:hidden` so it only appears below 1024px.
- The `<ul>` has `hidden lg:flex` so it's hidden on mobile and horizontal on desktop.
- The `<ul>` has `id="mobile-menu"` for `aria-controls` targeting.
- Two SVG icons inside the button: hamburger (default visible) and X (default hidden), toggled by the inline script.

- [ ] **Step 2: Run the dev server and verify mobile appearance**

Run: `npm run dev`
Open the dev server URL in a browser at 375px width (Chrome DevTools device emulation).
Expected: Hamburger button is visible; nav links are hidden.
Open at 1280px width.
Expected: Hamburger button is hidden; nav links are visible in a horizontal row (unchanged from before).

- [ ] **Step 3: Run type check**

Run: `npm run check`
Expected: PASS with no TypeScript or Astro errors.

- [ ] **Step 4: Commit**

```bash
git add src/components/BaseLayout.astro
git commit -m "feat: add hamburger menu toggle button to BaseLayout nav (issue #25)"
```

---

### Task 2: Add toggle script and overlay behavior

**Files:**
- Modify: `src/components/BaseLayout.astro` (add inline script and overlay)

**Interfaces:**
- Consumes: hamburger button from Task 1 (`#mobile-menu-toggle`, `#mobile-menu`, `#menu-icon-open`, `#menu-icon-close`)
- Produces: working toggle behavior with overlay that closes on click

- [ ] **Step 1: Add the inline toggle script**

Add the following `<script is:inline>` block at the end of the `<body>` in `src/components/BaseLayout.astro`, just before the closing `</body>` tag (after the `</footer>`):

```astro
<script is:inline>
  (() => {
    const toggle = document.getElementById('mobile-menu-toggle');
    const menu = document.getElementById('mobile-menu');
    const iconOpen = document.getElementById('menu-icon-open');
    const iconClose = document.getElementById('menu-icon-close');

    if (!toggle || !menu || !iconOpen || !iconClose) return;

    function openMenu() {
      menu.classList.remove('hidden');
      menu.classList.add('flex', 'flex-col');
      iconOpen.classList.add('hidden');
      iconOpen.classList.remove('block');
      iconClose.classList.remove('hidden');
      iconClose.classList.add('block');
      toggle.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
      menu.classList.add('hidden');
      menu.classList.remove('flex', 'flex-col');
      iconOpen.classList.remove('hidden');
      iconOpen.classList.add('block');
      iconClose.classList.add('hidden');
      iconClose.classList.remove('block');
      toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', () => {
      const isOpen = toggle.getAttribute('aria-expanded') === 'true';
      isOpen ? closeMenu() : openMenu();
    });

    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('click', (e) => {
      if (toggle.getAttribute('aria-expanded') === 'true' &&
          !toggle.contains(e.target) && !menu.contains(e.target)) {
        closeMenu();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        toggle.focus();
      }
    });
  })();
</script>
```

- [ ] **Step 2: Style the mobile menu for vertical layout**

Update the `<ul>` in the nav to include mobile-friendly positioning and spacing:

```astro
  <ul class="hidden lg:flex gap-6 list-none lg:static absolute top-full left-0 right-0 bg-white border-b border-gray-200 lg:border-none lg:bg-transparent lg:border-0 lg:top-auto lg:left-auto lg:right-auto p-4 lg:p-0 flex-col lg:flex-row lg:gap-6 lg:mt-0 mt-2" id="mobile-menu">
    <li><a href="/" class="text-sm text-gray-600 hover:text-gray-900 transition-colors block py-2 lg:py-0">Home</a></li>
    <li><a href="/about" class="text-sm text-gray-600 hover:text-gray-900 transition-colors block py-2 lg:py-0">About</a></li>
    <li><a href="/writing" class="text-sm text-gray-600 hover:text-gray-900 transition-colors block py-2 lg:py-0">Writing</a></li>
    <li><a href="/projects" class="text-sm text-gray-600 hover:text-gray-900 transition-colors block py-2 lg:py-0">Projects</a></li>
    <li><a href="/contact" class="text-sm text-gray-600 hover:text-gray-900 transition-colors block py-2 lg:py-0">Contact</a></li>
  </ul>
```

Mobile menu styling breakdown:
- `absolute top-full left-0 right-0` — drops down below nav, full width
- `bg-white border-b border-gray-200` — white bg with border on mobile
- `lg:static lg:border-none lg:bg-transparent` — reverts to normal flow on desktop
- `flex-col lg:flex-row` — vertical on mobile, horizontal on desktop
- `p-4 lg:p-0` — padding on mobile, none on desktop
- `block py-2 lg:py-0` — clickable padding on mobile links

- [ ] **Step 3: Run the dev server and verify full behavior**

Run: `npm run dev`

At 375px: hamburger visible, links hidden. Click hamburger: menu drops down vertically, icon changes to X. Click a link: menu closes. Click outside: menu closes. Press Escape: menu closes, focus returns to button.

At 1280px: hamburger hidden, horizontal nav links visible (unchanged). No visual regression.

- [ ] **Step 4: Run type check**

Run: `npm run check`
Expected: PASS with no TypeScript or Astro errors.

- [ ] **Step 5: Run production build**

Run: `npm run build`
Expected: PASS, produces valid `dist/` directory.

- [ ] **Step 6: Update CHANGELOG.md**

Add to `CHANGELOG.md` under `## Unreleased` → `### Fixed`:

```markdown
- Mobile navigation overflow — added hamburger menu for screens below 1024px (issue #25).
```

- [ ] **Step 7: Update decision log**

Add to `docs/strategy/decisions.md`:

```markdown
| 2026-07-25 | Use a hamburger menu with `is:inline` script for mobile navigation in BaseLayout. | Minimal client-side interactivity avoids Astro client component hydration overhead; Tailwind responsive utilities handle show/hide; inline script toggles CSS classes and ARIA attributes. | Chosen |
```

- [ ] **Step 8: Update docs/README.md**

Add to the "Implementation plans" section in `docs/README.md`:

```markdown
- [GitHub issue #25: Mobile navigation fix](superpowers/plans/2026-07-25-mobile-navigation.md) — hamburger menu toggle, overlay behavior, and responsive nav layout.
```

- [ ] **Step 9: Commit**

```bash
git add src/components/BaseLayout.astro CHANGELOG.md docs/strategy/decisions.md docs/README.md
git commit -m "feat: complete mobile navigation with toggle, overlay, and keyboard support (issue #25)"
```

---

## Self-Review

**1. Spec coverage:**
- Hamburger button visible on mobile, hidden on desktop: Task 1, Step 1 (`lg:hidden` on button).
- Nav links hidden on mobile, horizontal on desktop: Task 1, Step 1 (`hidden lg:flex` on ul).
- Toggle reveals vertical menu: Task 2, Step 1 (`openMenu()` adds `flex flex-col`).
- Icon switches between hamburger and X: Task 1, Step 1 (two SVGs) + Task 2, Step 1 (`openMenu`/`closeMenu` toggle `hidden`/`block`).
- Clicking outside closes menu: Task 2, Step 1 (`document.addEventListener('click', ...)`).
- Clicking a nav link closes menu: Task 2, Step 1 (`menu.querySelectorAll('a').forEach(...)`).
- `aria-expanded`, `aria-controls`, `aria-label` on toggle: Task 1, Step 1.
- Escape key closes menu: Task 2, Step 1 (`keydown` listener).
- Visual verification at 375px and 1280px: Task 1, Step 2 and Task 2, Step 3.
- `npm run check` passes: Task 1, Step 3 and Task 2, Step 4.
- `npm run build` succeeds: Task 2, Step 5.
- CHANGELOG.md updated: Task 2, Step 6.
- Decision log entry: Task 2, Step 7.
- docs/README.md updated: Task 2, Step 8.

**2. Placeholder scan:**
- No "TBD", "TODO", or "implement later".
- No vague "add validation" — each verification step is explicit with commands and expected output.
- No "write tests" without test code — N/A for static Astro; visual and build validation serves as the test cycle.
- No "similar to Task N" — each step is fully self-contained with complete code.
- All element IDs referenced in the script are defined in the HTML.

**3. Type/signature consistency:**
- `BaseLayout` interface unchanged: `{ title: string }` — no new props added.
- No new TypeScript types needed; inline script uses DOM APIs only.
- Tailwind classes use Tailwind CSS 4 syntax (responsive prefix utilities, no custom config).
- Element IDs (`mobile-menu-toggle`, `mobile-menu`, `menu-icon-open`, `menu-icon-close`) are consistent between HTML and script.

**4. Consistency with existing conventions:**
- Branch naming: `erikf/issue-25-mobile-navigation` matches `erikf/issue-N-short-description`.
- Component stays in `src/components/BaseLayout.astro` — existing location.
- Tailwind utilities for styling — matches existing pattern.
- `is:inline` script — Astro convention for minimal client-side JS without hydration.
- `Closes #25` in PR — matches delivery contract.

**5. Boundary check:**
- Does NOT add a new component file — keeps changes within existing `BaseLayout.astro`.
- Does NOT use Astro client-side directives (`client:visible`, `client:load`) — uses `is:inline` instead.
- Does NOT modify `astro.config.mjs`, `tailwind.config.cjs`, or `package.json`.
- Does NOT add external dependencies or JavaScript libraries.
- Does NOT change the nav link list or order.
- Does NOT modify page content or routing.

---

## Execution Recommendation

**Subagent-Driven (recommended)** — dispatch a fresh subagent per task using `superpowers:subagent-driven-development`. Task 1 (hamburger button) must complete before Task 2 (toggle script) begins. Two-stage review between tasks catches interface mismatches early.

**Inline Execution** — execute tasks sequentially in this session using `superpowers:executing-plans` with checkpoints for review.
