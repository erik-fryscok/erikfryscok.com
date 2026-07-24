# GitHub Issue #2: Astro, TypeScript, and Tailwind Foundation

Source: [GitHub issue #2](https://github.com/erik-fryscok/erikfryscok.com/issues/2)

Repository path: `docs/plans/github-issue-2-astro-foundation.md`

Implementation branch: `erikf/issue-2-astro-typescript-tailwind-foundation`

## Outcome

Establish a minimal, reproducible Astro foundation with strict TypeScript and
Tailwind CSS. The result will provide documented development and validation
commands without taking on the five-page site structure tracked by
[GitHub issue #3](https://github.com/erik-fryscok/erikfryscok.com/issues/3).

## Boundaries

This change will establish the buildable project foundation and a minimal root
page that proves Astro and Tailwind work together.

It will not add the Cloudflare adapter, a UI framework, content collections,
MDX, a testing framework, a linting stack, or the first-release page and
navigation structure. Astro will retain its default static output.

## Technical baseline

- Use npm and commit `package-lock.json`.
- Pin Node.js `24.18.0` LTS in `.node-version` and declare a compatible Node 24
  engine range in `package.json`.
- Use the current Astro 7 release line with `astro/tsconfigs/strict`.
- Install `@astrojs/check` and TypeScript so `.astro` and TypeScript files are
  checked explicitly.
- Use Tailwind CSS 4 through `@tailwindcss/vite`; do not use the deprecated
  `@astrojs/tailwind` integration.
- Ignore Astro's generated `.astro/` directory.

The Node baseline is compatible with Cloudflare Pages' configurable build
environment. The framework choices follow the current
[Astro installation](https://docs.astro.build/en/install-and-setup/),
[TypeScript](https://docs.astro.build/en/guides/typescript/), and
[Tailwind styling](https://docs.astro.build/en/guides/styling/) guidance.

## Codex model and reasoning recommendation

Use `gpt-5.6-sol` with `high` reasoning effort for the initial implementation.
This work is bounded, but it establishes the shared application foundation,
merges generated framework files into an existing repository, depends on
version-sensitive integrations, and requires validation across code,
configuration, documentation, and public-repository safety.

`gpt-5.6-sol` is the current frontier-capability model for complex reasoning
and coding. `high` gives the implementation enough room to inspect generated
output, reconcile it with repository conventions, and diagnose integration or
validation failures without defaulting to the highest-cost effort.

Do not default to `max`; reserve it for a specific unresolved, quality-first
problem after `high` proves insufficient. Use `medium` for later routine,
well-understood maintenance or deterministic validation reruns where deeper
reasoning is unlikely to change the outcome.

This recommendation was verified against the official
[GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model)
and [GPT-5.6 Sol model reference](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
on 2026-07-23. Recheck the available Codex model lineup before execution if
these names or effort levels are no longer available.

## Implementation approach

1. Generate Astro's current minimal scaffold in a temporary directory rather
   than running the generator over this existing repository.
2. Merge only the required scaffold files into the repository, preserving the
   existing Git configuration, documentation, issue templates, and ignore
   rules.
3. Configure `astro.config.mjs` with the Tailwind Vite plugin.
4. Add `src/styles/global.css` with `@import "tailwindcss"` and import it from
   the root Astro page.
5. Keep the root page intentionally small, but use a Tailwind utility so the
   integration is exercised by the production build and preview.
6. Add the documented developer commands and install only the dependencies
   required for this foundation.

## Developer interface

The project will expose these npm commands:

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Astro development server. |
| `npm run check` | Run Astro and TypeScript diagnostics. |
| `npm run build` | Run diagnostics and then create the production build. |
| `npm run preview` | Serve the production build locally for verification. |

`npm run build` will fail before producing a deployable build when
`npm run check` reports an error.

There are no runtime APIs, schemas, migrations, environment variables, or
external service contracts in this change.

## Documentation and release impact

- Add prerequisites, installation, development, checking, building, and
  preview commands to the root `README.md`.
- Change the existing Astro, TypeScript, and Tailwind decision in
  `docs/strategy/decisions.md` from `Proposed` to `Chosen` after the foundation
  is implemented successfully.
- Record the new development foundation under `CHANGELOG.md` in `Unreleased`.
- Keep active delivery status and completion evidence in GitHub issue #2 rather
  than duplicating them in Markdown.

## Validation

Implementation is complete when all of the following evidence is available:

- `npm ci` succeeds from the committed lockfile under Node.js `24.18.0`.
- `npm run check` completes without Astro or TypeScript diagnostics.
- `npm run build` creates the static `dist/` output.
- `npm run preview` serves `/` with HTTP 200.
- The root page renders the Tailwind-styled placeholder, proving the stylesheet
  is included in the production output.
- Documentation links pass the repository Markdown link check.
- `git diff --check` reports no whitespace errors.
- The public-repository privacy review finds no credentials, confidential
  employer or client information, private identifiers, local paths, or
  unintended generated files.

## Delivery notes

The implementation should remain within GitHub issue #2. Work that introduces
the Home, About, Writing, Projects, or Contact structure belongs to issue #3.
Cloudflare Pages project configuration and deployment should remain with the
separately tracked hosting work.
