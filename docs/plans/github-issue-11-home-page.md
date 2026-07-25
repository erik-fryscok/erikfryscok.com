# GitHub Issue #11: Implement the Home Page

Source: [GitHub issue #11](https://github.com/erik-fryscok/erikfryscok.com/issues/11)

Repository path: `docs/plans/github-issue-11-home-page.md`

Implementation branch: `erikf/issue-11-home-page`

## Outcome

Create the Home page as the primary entry point for visitors. It communicates
the working positioning, provides a short introduction, surfaces selected writing
and projects, and offers a clear contact path.

## Boundaries

This change implements the Home page structure and creates minimal placeholder
pages for About, Writing, and Projects so that all navigation links are
functional. Content for About, Writing, and Projects will be finalized in their
own issues (issue #4 for initial copy, with dedicated issues for each page).

This change does not add MDX, content collections, animations, or interactive
JavaScript components.

## Dependencies

- Issue #2 (Astro, TypeScript, Tailwind foundation) — merged.
- Issue #15 (Contact page with BaseLayout) — merged. The shared BaseLayout
  component provides header, navigation, main content area, and footer.

## Implementation approach

### Batch 1: Foundation and placeholder pages

1. Create `src/pages/about.astro` — minimal placeholder with BaseLayout.
2. Create `src/pages/writing.astro` — minimal placeholder with BaseLayout.
3. Create `src/pages/projects.astro` — minimal placeholder with BaseLayout.
4. Add `/projects` to the BaseLayout navigation (was missing from the Contact
   page implementation in issue #15).
5. Verify `npm run check` and `npm run build` pass with all pages.

### Batch 2: Home page implementation

1. Rewrite `src/pages/index.astro` (replacing the Tailwind placeholder) with:
   - **Hero section** — headline from the product brief and supporting copy.
   - **Introduction section** — short bio with link to `/about`.
   - **Selected Work section** — two-card grid linking to `/writing` and
     `/projects` with placeholder descriptions.
   - **Contact CTA section** — styled call-to-action box with button linking
     to `/contact`.
2. Use BaseLayout for consistent header/navigation/footer.
3. Use Tailwind utilities for all styling.
4. Ensure responsive behavior:
   - Hero headline uses `sm:text-5xl` breakpoint.
   - Selected Work grid uses `sm:grid-cols-2` for two-column layout on
     tablets and wider.
   - Navigation wraps naturally on mobile via flex layout.
5. Verify `npm run check` and `npm run build` pass.

### Batch 3: Documentation and validation

1. Create this implementation plan file.
2. Update `docs/README.md` to reference the new plan.
3. Update `CHANGELOG.md` under Unreleased.
4. Run final validation: `npm run check`, `npm run build`, `git diff --check`.
5. Verify content follows documented content boundaries (no employer or client
   confidential information).
6. Commit and create pull request linked to issue #11.

## Content boundaries compliance

All content on this page uses generalized positioning language from the product
brief. No employer names, client details, proprietary information, credentials,
or internal project details are included.

## Validation

Implementation is complete when all of the following evidence is available:

- `npm run check` completes without Astro or TypeScript diagnostics.
- `npm run build` creates the static `dist/` output with 5 pages.
- The Home page is accessible at `/` and reachable through the site navigation.
- The hero section displays the working positioning headline and supporting copy.
- Links to About, Writing, Projects, and Contact pages are present and functional.
- The layout works at common mobile and desktop widths without horizontal overflow.
- `git diff --check` reports no whitespace errors.
- Documentation links pass the repository Markdown link check.

## Deviations from the issue

The issue references a "Selected work carousel or grid." A simple two-card grid
was implemented rather than a carousel, since carousels require JavaScript and
the issue's dependencies only include the static Astro foundation. A JavaScript
carousel can be added in a future issue if needed.

The issue mentions 2–3 featured items. Two cards (Writing and Projects) were
implemented, matching the two content areas with dedicated pages.

## Documentation and release impact

- Add the Home page under `CHANGELOG.md` in Unreleased.
- Add this plan to `docs/README.md` in the Implementation plans section.
- No decision log entries required (no new architectural choices).
