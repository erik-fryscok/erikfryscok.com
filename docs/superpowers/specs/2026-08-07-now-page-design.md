# Focused Now Page Design

**Issue:** [GitHub #35 — Add a focused /now page](https://github.com/erik-fryscok/erikfryscok.com/issues/35)

## Purpose

Add a standalone `/now` page that answers what Erik is focused on at this point in time. It is a concise personal snapshot, not a social-media feed or replacement for the Writing archive.

## Experience

- Keep `/writing` and its existing article unchanged.
- Add **Now** to the main navigation between About and Writing. The existing responsive navigation makes it available on both desktop and mobile.
- Render the page with the shared `BaseLayout` and the established narrow, readable content column.
- Start with an `h1` of “Now,” followed by a short explanation that this is a current snapshot and a visible “Last updated: August 7, 2026” line.

## Initial Content

Use three short sections, each expressed as concise prose rather than timeline updates:

1. **Building better engineering systems** — current focus on practical AI-enabled development, cloud infrastructure, documentation, and the engineering practices that help teams work more effectively. Do not identify employers, clients, internal systems, or non-public work.
2. **Playing guitar again** — regularly playing guitar, with an emphasis on Drop C-tuned songs by System of a Down and August Burns Red.
3. **Riding new routes** — biking frequently and finding or creating routes around the neighbourhood.

The professional focus and the two personal pursuits receive equal visual treatment. Keep the copy matter-of-fact and human; avoid calls to action, status-feed language, and speculative future commitments.

## Quality Requirements

- Use semantic heading order (`h1`, followed by `h2` sections) and readable body copy with the existing Tailwind design language.
- Do not add client-side JavaScript, dependencies, CMS/content-collection machinery, or images.
- Preserve existing mobile menu behavior; adding the nav item must not cause horizontal overflow at small viewports.
- Add a concise Unreleased changelog entry and a decision-log entry documenting that `/now` complements, rather than repurposes, `/writing`.
- Verify Astro/TypeScript diagnostics, production build output, the `/now` route, and navigation links.
