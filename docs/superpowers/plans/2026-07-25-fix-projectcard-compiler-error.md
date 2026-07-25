# Fix ProjectCard CompilerError Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the invalid `@ts-expect-error` comment from `ProjectCard.astro` so the Projects page compiles and renders correctly.

**Architecture:** The bug is a single invalid comment on line 29 of `ProjectCard.astro`. The `key` prop on `<span>` inside a `.map()` is valid Astro template syntax and requires no TypeScript suppression. The fix is removing one line.

**Tech Stack:** Astro 7.1.3, TypeScript, Tailwind CSS

**Issue:** [GitHub #22 — Projects page CompilerError](https://github.com/erik-fryscok/erikfryscok.com/issues/22)
**Parent:** [GitHub #14 — Projects page](https://github.com/erik-fryscok/erikfryscok.com/issues/14)

## Global Constraints

- Astro version floor: `^7.0.0` (currently 7.1.3).
- Do not introduce new dependencies.
- All changes must pass `npm run check` (Astro type check + `tsc --noEmit`).
- Content boundaries from `docs/product/brief.md` apply: no employer, client, credential, proprietary, or non-public material.
- Follow existing code conventions: Tailwind utility classes, component prop interfaces, BaseLayout pattern.

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `src/components/ProjectCard.astro` | Modify (line 29) | Remove invalid `@ts-expect-error` comment |

Single-file change. No new files needed.

---

### Task 1: Remove the invalid @ts-expect-error comment

**Files:**
- Modify: `src/components/ProjectCard.astro:29`

**Interfaces:**
- Consumes: none (standalone fix)
- Produces: `ProjectCard.astro` compiles without `CompilerError`

- [ ] **Step 1: Confirm the failing state**

Run the dev server and verify the error reproduces:

```bash
npm run dev
```

Navigate to `http://localhost:4321/projects` in the browser.
Expected: `CompilerError: Unexpected token` at `ProjectCard.astro:29:11` in the terminal. Page fails to render.

- [ ] **Step 2: Remove the invalid comment**

In `src/components/ProjectCard.astro`, remove line 29 entirely. The diff should look like this:

```diff
   <div class="flex flex-wrap gap-2">
     {technologies.map((tech) => (
-      <!-- @ts-expect-error — Astro's key directive for map reconciliation; not in HTMLAttributes -->
       <span
         key={tech}
         class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
       >
         {tech}
       </span>
     ))}
   </div>
```

The `key` attribute on `<span>` is a recognized Astro template directive. It does not require a TypeScript suppression comment. The `@ts-expect-error` directive only works in `.ts`/`.tsx` files, not inside Astro template expressions.

- [ ] **Step 3: Run type check**

```bash
npm run check
```

Expected: PASS with zero diagnostics. If `@astrojs/check` reports errors on the `key` prop, the fix is incorrect — but based on Astro 7.x documentation, `key` is a valid template attribute.

- [ ] **Step 4: Run build**

```bash
npm run build
```

Expected: PASS — produces valid `dist/` output including `dist/projects/index.html`.

- [ ] **Step 5: Verify the page renders**

```bash
npm run preview
```

Navigate to `http://localhost:4321/projects` in the browser.
Expected: Three project cards render with titles, descriptions, technology tags, outcomes checkmarks, and links. No compiler errors in the terminal.

- [ ] **Step 6: Commit**

```bash
git add src/components/ProjectCard.astro
git commit -m "fix: remove invalid @ts-expect-error from ProjectCard template (issue #22)

The key prop is a valid Astro template directive and does not require a
TypeScript suppression comment. @ts-expect-error only works in .ts/.tsx
files, not inside Astro template expressions."
```

## Deliverables

- `src/components/ProjectCard.astro` — line 29 removed; `key` prop works without suppression.
- `CHANGELOG.md` — entry under next release for this bug fix.

## Verification

- `npm run check` passes with zero diagnostics.
- `npm run build` produces valid output including `/projects/`.
- `npm run preview` renders the Projects page at `/projects` with three cards.
- No `CompilerError` in dev server logs.

## Notes

- This fix was introduced in commit `67cf33b` (issue #13). The `@ts-expect-error` comment was a mistaken attempt to suppress a non-existent TypeScript warning.
- The `technologies.map()` loop on lines 28-36 was the only location using `@ts-expect-error` in the codebase. The `outcomes.map()` (line 47) and `links.map()` (line 59) loops never had this comment and work correctly.
- No CHANGELOG update needed for this internal build fix — the Projects page was never accessible to users, so there is no user-visible behavior change. The changelog entry for the Projects page feature will cover this when the page launches.
