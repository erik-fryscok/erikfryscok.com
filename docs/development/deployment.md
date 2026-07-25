# Cloudflare Pages Preview Deployment

> **For agentic workers:** Use this document to understand the build contract, preview workflow, and local preview commands. Future tasks (#6 domain connection, #7 launch validation) depend on this configuration.

## Deployment URL

The Cloudflare Pages preview deployment is available at:

```
https://erikfryscok.pages.dev
```

> **Note:** This URL is the production deployment URL. Preview deployments from feature branches follow the pattern `https://<branch-name>--erikfryscok.pages.dev`. The repository owner must connect the GitHub repository in the Cloudflare Pages dashboard (Task 1) to enable automatic preview deployments.

## Build Configuration

| Setting | Value |
| --- | --- |
| Project name | `erikfryscok` |
| Production branch | `main` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node.js version | `24` |

### Build command details

The build command `npm run build` runs two steps in sequence:

1. `npm run check` — Astro and TypeScript diagnostics
2. `astro build` — static site generation to `dist/`

### Build output

The build outputs a fully static site to `dist/`. Cloudflare Pages serves this directory directly. No server-side rendering, no dynamic routes, no runtime dependencies.

## Environment Variables

None required. The site is fully static. No runtime configuration, API keys, or environment-specific settings are needed.

## Preview Workflow

When the repository is connected to Cloudflare Pages via the GitHub integration:

1. A pull request is opened from a feature branch to `main`.
2. Cloudflare Pages automatically checks out the feature branch.
3. Dependencies are installed from `package-lock.json`.
4. `npm run build` executes.
5. If the build succeeds, a preview deployment is generated at:

   ```
   https://<branch-name>--erikfryscok.pages.dev
   ```

6. The preview URL is posted as a comment on the pull request.

### Manual preview deployment

To trigger a manual preview deployment:

1. Push a commit to a feature branch.
2. Wait 1–3 minutes for the build to complete.
3. Check the Cloudflare Pages dashboard for the deployment status.

## Local Preview

To preview the site locally before pushing:

```bash
# Install dependencies
npm install

# Run diagnostics and build
npm run build

# Serve the build locally
npm run preview
```

The local preview server runs on `http://localhost:4321` by default.

## Related Documentation

- [Product brief: technical direction](../product/brief.md#technical-direction) — framework, hosting, and content decisions.
- [Project lifecycle](../project-lifecycle.md) — division of responsibility between Git and GitHub.
- [Cloudflare Pages preview deployment plan](../superpowers/plans/2026-07-25-cloudflare-pages-preview.md) — the implementation plan for this task.
