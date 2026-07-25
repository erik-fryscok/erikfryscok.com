# Implementation Plan: Projects Page (Issue #14)

**Issue:** [GitHub #14 — Implement the Projects page](https://github.com/erik-fryscok/erikfryscok.com/issues/14)
**Parent:** [GitHub #3 — Build the five-page site skeleton and navigation](https://github.com/erik-fryscok/erikfryscok.com/issues/3)
**Branch:** `issue-14-projects-page`

## Context

The Projects page showcases a small set of meaningful case studies rather than every repository. This is part of the first release scope (five-page site skeleton).

## Dependencies

- Issue #2 (Astro, TypeScript, Tailwind foundation) — **merged**.
- BaseLayout component — **exists** at `src/components/BaseLayout.astro`.
- Content for specific case studies will be finalized in issue #4; placeholder content is acceptable.

## Content Boundaries

Per [docs/product/brief.md](../product/brief.md): do not publish employer or client confidential information, proprietary source code, credentials, non-public designs, or internal project details. Placeholder content must use generalized, public-facing examples.

## Tasks

### Task 1: Create the ProjectCard component

1. Create `src/components/ProjectCard.astro`.
2. Accept props: `title` (string), `description` (string), `technologies` (string[]), `outcomes` (string[]), `links` (array of `{ label, href }`).
3. Render a card with: title (h2), description paragraph, technology tags (small pills), outcomes list, and link buttons.
4. Use Tailwind CSS utility classes consistent with the existing codebase (e.g., `border border-gray-200 rounded-lg p-6`).
5. Ensure the card is self-contained and responsive.

**Verification:** Visual inspection; `npm run check` passes.

### Task 2: Create the Projects page

1. Create `src/pages/projects.astro`.
2. Import and use `BaseLayout` for consistent header/navigation/footer.
3. Add an introductory section (h1 + paragraph) explaining the Projects area.
4. Import `ProjectCard` and place 2–3 placeholder cards demonstrating the layout.
5. Use a CSS grid layout (`grid grid-cols-1 md:grid-cols-2 gap-6`) for responsive reflow.
6. Placeholder content must respect content boundaries (generalized examples, no confidential info).

**Verification:** Page renders at `/projects`; `npm run check` passes.

### Task 3: Update BaseLayout navigation

1. Add a `<li><a href="/projects">Projects</a></li>` entry to the nav `<ul>` in `BaseLayout.astro`.
2. Place it between "Writing" and "Contact" to match the site skeleton order (Home, About, Writing, Projects, Contact).

**Verification:** Navigation link appears and points to `/projects`.

### Task 4: Final validation

1. Run `npm run check` — must pass with zero diagnostics.
2. Run `npm run build` — must produce a valid `dist/` output including `/projects/`.
3. Verify `dist/projects/index.html` exists and contains the expected content.

**Verification:** Both commands succeed; output is valid.

## Deliverables

- `src/components/ProjectCard.astro` — new reusable component.
- `src/pages/projects.astro` — new page.
- `src/components/BaseLayout.astro` — updated with Projects nav link.
- `docs/plans/github-issue-14-projects-page.md` — this plan.
- `CHANGELOG.md` — entry for user-visible change.
- `docs/README.md` — updated with plan reference.
