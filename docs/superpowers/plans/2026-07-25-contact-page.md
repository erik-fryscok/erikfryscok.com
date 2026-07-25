# Contact Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the Contact page with a shared layout component so visitors have a clear, low-friction way to get in touch.

**Architecture:** Two tasks — first build the shared `BaseLayout` component (header, navigation, footer) that all five first-release pages will consume, then create the Contact page using that layout. No backend, no form processing; just direct links to email, GitHub, and professional profiles.

**Tech Stack:** Astro 7, TypeScript (strict mode via `astro/tsconfigs/strict`), Tailwind CSS 4 (via `@tailwindcss/vite`), Node 24.

## Global Constraints

- Node.js `24.18.0` pinned in `.node-version`; engine range `>=24 <25` in `package.json`.
- Build command: `npm run build` (runs `check` + `astro build`).
- Check command: `npm run check` (runs `astro check && tsc --noEmit`).
- Branch naming: `erikf/issue-N-short-description`.
- PR must use `Closes #15` to link to the issue.
- Content boundaries: do not publish employer/client confidential info, credentials, or internal project details.
- Responsive breakpoints: mobile at `375px`, desktop at `1280px` — no horizontal overflow at either width.
- Astro default static output (no SSR adapter).
- Tailwind CSS 4 via `@tailwindcss/vite` plugin in `astro.config.mjs`; global styles in `src/styles/global.css` with `@import "tailwindcss"`.
- Every Astro file must import `src/styles/global.css` in its frontmatter to receive Tailwind utilities.

---

### Task 1: Create the shared BaseLayout component

**Files:**
- Create: `src/components/BaseLayout.astro`

**Interfaces:**
- Consumes: nothing from other tasks (this is the first task)
- Produces: `BaseLayout` component accepting `title: string` prop and a default slot; later tasks import it from `../components/BaseLayout.astro`

The `BaseLayout` component is the single shared layout for all five first-release pages. Every page imports it, passes a page-specific title, and places content in the default slot. This ensures consistent header, navigation, and footer across the entire site.

- [ ] **Step 1: Create the BaseLayout component file**

Create `src/components/BaseLayout.astro` with the following content:

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
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title}</title>
  </head>
  <body class="min-h-screen bg-white text-gray-900 flex flex-col">
    <header class="border-b border-gray-200">
      <nav class="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between" aria-label="Main navigation">
        <a href="/" class="text-lg font-semibold text-gray-900 hover:text-gray-600 transition-colors">
          erikfryscok
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
    <main class="flex-1 max-w-3xl w-full mx-auto px-4 py-12">
      <slot />
    </main>
    <footer class="border-t border-gray-200">
      <div class="max-w-3xl mx-auto px-4 py-6 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} Erik Fryscok
      </div>
    </footer>
  </body>
</html>
```

Key design decisions embedded in this component:
- `html lang="en"` for accessibility and SEO.
- Viewport meta tag for responsive behavior.
- Static description meta tag — page-specific descriptions can be added later.
- `favicon.svg` reference — a placeholder; the actual favicon will be added in a future task.
- `body` uses `flex flex-col` with `main` using `flex-1` so the footer always sticks to the bottom.
- `max-w-3xl mx-auto px-4` on nav, main, and footer for consistent horizontal centering.
- Navigation links for all five pages so the structure is ready regardless of which page is implemented first.
- `slot` element for page-specific content injection.

- [ ] **Step 2: Verify the component compiles**

Run the type check to confirm the Astro file has no diagnostics:

```bash
npm run check
```

Expected: completes with zero errors. The `Astro.props` access and slot usage are valid Astro patterns.

- [ ] **Step 3: Verify the build succeeds**

```bash
npm run build
```

Expected: produces a valid `dist/` directory. The layout component itself won't appear in `dist/` until a page uses it, but the build must not fail.

- [ ] **Step 4: Commit**

```bash
git add src/components/BaseLayout.astro
git commit -m "feat: add shared BaseLayout component with header, nav, and footer (issue #15)"
```

---
### Task 2: Create the Contact page

**Files:**
- Create: `src/pages/contact.astro`

**Interfaces:**
- Consumes: `BaseLayout` from `../components/BaseLayout.astro` (accepts `title: string` prop, provides default slot)
- Produces: the Contact page at route `/contact`

The Contact page presents a brief introduction and direct links to available contact channels. No form, no backend — just mailto, GitHub, and LinkedIn links styled as accessible, responsive cards.

- [ ] **Step 1: Create the Contact page**

Create `src/pages/contact.astro`. The full file content follows — copy it as one complete file.

```astro
---
import BaseLayout from "../components/BaseLayout.astro";
---

<BaseLayout title="Contact — Erik Fryscok">
  <section aria-labelledby="contact-heading">
    <h1 id="contact-heading" class="text-3xl font-bold text-gray-900">
      Get in touch
    </h1>
    <p class="mt-4 text-lg text-gray-600 max-w-2xl">
      I'm always interested in connecting with people working on engineering
      leadership, AI-enabled development, automation, and modern software
      practices. Here are the best ways to reach me.
    </p>

    <div class="mt-10 grid gap-6 sm:grid-cols-2">
      <a
        href="mailto:erik@erikfryscok.com"
        class="group flex items-start gap-4 p-6 rounded-lg border border-gray-200 hover:border-gray-400 hover:shadow-sm transition-all"
      >
        <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-lg bg-gray-100 text-gray-600 group-hover:bg-gray-200 transition-colors" aria-hidden="true">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2" /><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" /></svg>
        </span>
        <div>
          <h2 class="font-semibold text-gray-900">Email</h2>
          <p class="mt-1 text-sm text-gray-600">erik@erikfryscok.com</p>
          <p class="mt-1 text-sm text-gray-500">For general inquiries, collaboration, and consulting.</p>
        </div>
      </a>
      <a
        href="https://github.com/erik-fryscok"
        target="_blank"
        rel="noopener noreferrer"
        class="group flex items-start gap-4 p-6 rounded-lg border border-gray-200 hover:border-gray-400 hover:shadow-sm transition-all"
      >
        <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-lg bg-gray-100 text-gray-600 group-hover:bg-gray-200 transition-colors" aria-hidden="true">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.206 11.387.6.113.826-.258.826-.577 0-.286-.013-1.19-.013-2.166-3.338.721-4.035-1.614-4.035-1.614-.546-1.387-1.333-1.758-1.333-1.758-1.09-.745.083-.73.083-.73 1.205.085 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.304 3.495.998.108-.776.42-1.305.763-1.605-2.665-.305-5.466-1.334-5.466-5.931 0-1.313.469-2.386 1.234-3.227-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.52 11.52 0 0 1 12 5.204c.95.004 1.903.127 2.823.377 2.293-1.552 3.301-1.23 3.301-1.23.654 1.653.243 2.874.118 3.176.77.841 1.235 1.914 1.235 3.227 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222 0 1.606-.011 2.898-.011 3.293 0 .322.221.695.828.578C20.565 21.795 24 17.31 24 12c0-6.63-5.37-12-12-12z" /></svg>
        </span>
        <div>
          <h2 class="font-semibold text-gray-900">GitHub</h2>
          <p class="mt-1 text-sm text-gray-600">@erik-fryscok</p>
          <p class="mt-1 text-sm text-gray-500">Open source projects, code, and technical writing.</p>
        </div>
      </a>
      <a
        href="https://www.linkedin.com/in/erikfryscok"
        target="_blank"
        rel="noopener noreferrer"
        class="group flex items-start gap-4 p-6 rounded-lg border border-gray-200 hover:border-gray-400 hover:shadow-sm transition-all"
      >
        <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-lg bg-gray-100 text-gray-600 group-hover:bg-gray-200 transition-colors" aria-hidden="true">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.378-1.85 3.601 0 4.27 2.358 4.27 5.44v6.301zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" /></svg>
        </span>
        <div>
          <h2 class="font-semibold text-gray-900">LinkedIn</h2>
          <p class="mt-1 text-sm text-gray-600">Erik Fryscok</p>
          <p class="mt-1 text-sm text-gray-500">Professional network and industry connections.</p>
        </div>
      </a>
    </div>
  </section>
</BaseLayout>
```

Key design decisions:
- `BaseLayout` wraps all content with `title` prop for the `<title>` tag.
- `section` with `aria-labelledby` pointing to the `<h1>` id for screen reader accessibility.
- Three contact cards in a responsive grid: `grid gap-6 sm:grid-cols-2` stacks on mobile, two columns on desktop.
- Each card is an `<a>` element because it navigates — correct semantic choice.
- `mailto:` for email opens the user's email client.
- `target="_blank" rel="noopener noreferrer"` for external links — security best practice.
- Inline SVG icons (Heroicons email, GitHub, LinkedIn) — no external icon library.
- `aria-hidden="true"` on decorative icon containers.
- Email `erik@erikfryscok.com` matches the personal domain.
- LinkedIn URL uses GitHub username pattern — update if the actual URL differs.

- [ ] **Step 2: Run the type check**

```bash
npm run check
```

Expected: completes with zero errors. The `BaseLayout` import uses `.astro` extension, the `title` prop matches the component's interface, and the slot content is valid HTML.

- [ ] **Step 3: Build and verify the output**

```bash
npm run build
```

Expected: produces a valid `dist/` directory containing `dist/contact/index.html`. Verify:

```bash
ls dist/contact/index.html
```

- [ ] **Step 4: Preview and verify visually**

```bash
npm run preview
```

Open `http://localhost:4321/contact` in a browser and verify:
- The page loads with the BaseLayout header, navigation, and footer.
- The "Get in touch" heading is visible.
- The introductory paragraph is displayed.
- Three contact cards (Email, GitHub, LinkedIn) are shown in a grid.
- On desktop (1280px): two-column grid layout.
- On mobile (375px): single-column stacked layout.
- No horizontal overflow at either width.
- The email link opens the email client (`mailto:`).
- The GitHub and LinkedIn links open in new tabs.
- Navigation links in the header are present for all five pages.

- [ ] **Step 5: Verify accessibility attributes**

In the browser dev tools or an accessibility checker, confirm:
- The `<nav>` element has `aria-label="Main navigation"`.
- The `<section>` has `aria-labelledby="contact-heading"` matching the `<h1>` id.
- Decorative SVG icons have `aria-hidden="true"`.
- External links have `rel="noopener noreferrer"`.

- [ ] **Step 6: Commit**

```bash
git add src/pages/contact.astro
git commit -m "feat: add Contact page with email, GitHub, and LinkedIn links (issue #15)"
```

---

## Self-Review

**1. Spec coverage:**
- Contact introduction — brief message inviting visitors to reach out: Task 2, Step 1 (intro paragraph under h1).
- Contact methods — email link, GitHub profile, LinkedIn: Task 2, Step 1 (three contact cards).
- Simple, accessible layout — no complex forms: Task 2, Step 1 (link-based cards, no form elements).
- Shared layout and navigation from the site skeleton: Task 1 (BaseLayout with header/nav/footer); Task 2 consumes it.
- Accessible at `/contact`: Task 2 — `src/pages/contact.astro` creates the `/contact` route via Astro file-based routing.
- Reachable through site navigation: Task 1 — nav includes `/contact` link.
- All links functional, properly formatted, accessible: Task 2, Step 5 (explicit accessibility verification).
- Responsive at 375px and 1280px without horizontal overflow: Task 2, Step 4 (visual verification at both widths).
- `npm run check` passes: Task 1, Step 2 and Task 2, Step 2.
- `npm run build` produces valid `dist/`: Task 1, Step 3 and Task 2, Step 3.
- No credentials, private identifiers, or sensitive information: only public email, public GitHub profile, and public LinkedIn URL.

**2. Placeholder scan:**
- No "TBD", "TODO", or "implement later".
- No vague "add validation" — each validation step is explicit with commands and expected output.
- No "write tests" without test code — N/A for static Astro pages; visual and build validation serves as the test cycle.
- No "similar to Task N" — each step is fully self-contained with complete code.
- All types and function signatures are defined inline.

**3. Type/signature consistency:**
- `BaseLayout` interface: `{ title: string }` defined in Task 1, consumed identically in Task 2.
- Import path `../components/BaseLayout.astro` is correct from `src/pages/contact.astro`.
- Tailwind classes use Tailwind CSS 4 syntax (no `@apply` or custom config needed).

**4. Consistency with existing conventions:**
- Branch naming: `erikf/issue-15-contact-page` matches `erikf/issue-N-short-description`.
- Component in `src/components/` — standard Astro convention.
- Page in `src/pages/` — standard Astro file-based routing.
- Tailwind utilities for styling — matches existing `index.astro` pattern.
- `Closes #15` in PR — matches delivery contract.

**5. Boundary check:**
- Does NOT add a contact form (deferred per spec: "no complex forms in the first release").
- Does NOT add backend or form processing (per spec: "No backend or form-processing dependency").
- Does NOT add MDX, content collections, or syntax highlighting (deferred per product brief).
- Does NOT modify `astro.config.mjs` (no new integrations needed).
- Does NOT add analytics (deferred per product brief: "after launch").
- The `favicon.svg` reference in BaseLayout is a placeholder — the actual favicon asset will be added in a future task. The build will still succeed; browsers will show a missing icon until the file exists.

---

## Execution Recommendation

**Subagent-Driven (recommended)** — dispatch a fresh subagent per task using `superpowers:subagent-driven-development`. Task 1 (BaseLayout) must complete before Task 2 (Contact page) begins. Two-stage review between tasks catches interface mismatches early.

**Inline Execution** — execute tasks sequentially in this session using `superpowers:executing-plans` with checkpoints for review.

