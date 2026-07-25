# Implementation Plan: Writing Page (Issue #13)

**Issue:** [GitHub #13 — Implement the Writing page](https://github.com/erik-fryscok/erikfryscok.com/issues/13)
**Parent:** [GitHub #3 — Build the five-page site skeleton and navigation](https://github.com/erik-fryscok/erikfryscok.com/issues/3)
**Branch:** `erikf/issue-13-writing-page`
**Status:** complete

## Dependencies (all satisfied)

- [x] Issue #2 — Astro, TypeScript, Tailwind foundation (merged)
- [x] Issue #15 — BaseLayout component and Contact page (merged)

## Context

The BaseLayout component already exists with a "Writing" nav link pointing to `/writing`. The Contact page (`contact.astro`) establishes the pattern: import BaseLayout, use `max-w-2xl mx-auto` container, card-based sections with Tailwind utility classes.

## Tasks

### Batch 1: Create the Writing page

1. Create `src/pages/writing.astro` using BaseLayout.
2. Add an introductory heading and paragraph explaining what visitors will find in the Writing section (generalized engineering thinking, lessons, and patterns).
3. Add a placeholder article list section with a "coming soon" message, structured as a card similar to the Contact page's contact-method cards.
4. Ensure the page is responsive at 375px (mobile) and 1280px (desktop) — use the existing `max-w-2xl mx-auto` container pattern from Contact.

### Batch 2: Future-ready content structure

5. Create `src/content/writing/` directory with a `README.md` explaining the future Markdown-based article convention.
6. This directory signals where Markdown articles will live when content is ready, without committing to MDX or a full content collection yet.

### Batch 3: Validation

7. Run `npm run check` — must pass with no TypeScript or Astro diagnostics.
8. Run `npm run build` — must produce a valid static `dist/` output.
9. Verify the Writing page is accessible at `/writing` and reachable through the site navigation.

## Acceptance Criteria

- [ ] The Writing page is accessible at `/writing` and reachable through the site navigation.
- [ ] The page has a clear introductory message for the Writing section.
- [ ] A placeholder article list or "coming soon" indicator is present.
- [ ] The structure supports future Markdown-based articles without requiring MDX.
- [ ] The layout works at common mobile and desktop widths without horizontal overflow.
- [ ] `npm run check` passes with no TypeScript or Astro diagnostics.
- [ ] `npm run build` produces a valid static `dist/` output.

## Deviations from Issue

None planned. The implementation follows the issue's 7 implementation steps directly.
