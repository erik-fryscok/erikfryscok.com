# Cloudflare Pages Preview Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure Cloudflare Pages preview deployment so the site can be reviewed before public launch.

**Architecture:** Use Cloudflare Pages GitHub integration for automatic preview deployments on every branch push. No local tooling required — dashboard configuration drives the delivery path. Document the setup so future tasks (#6 domain connection, #7 launch validation) know the build contract.

**Tech Stack:** Cloudflare Pages, Astro 7, Node 24, static output to `dist/`

## Global Constraints

- Node.js `24.18.0` pinned in `.node-version`; Cloudflare Pages build must use Node 24.
- Build command: `npm run build` (runs `check` + `astro build`).
- Build output directory: `dist`.
- No environment variables required (fully static site).
- Branch naming: `erikf/issue-N-short-description`.
- PR must use `Closes #5` to link to the issue.
- Content boundaries: do not publish employer/client confidential info, credentials, or internal project details.
- Documentation lives in `docs/`; deployment docs go in `docs/development/`.

---

### Task 1: Set up Cloudflare Pages Project

**Files:**
- Dashboard: Cloudflare Pages (no repo files)

**Prerequisites:** Cloudflare account with access. Repository owner (`erik-fryscok`) must perform this step manually.

- [ ] **Step 1: Navigate to Cloudflare Pages**

Go to https://dash.cloudflare.com and navigate to Pages > Create a project.

- [ ] **Step 2: Connect the GitHub repository**

Select "Connect to Git" flow. Authorize GitHub access if prompted. Select the `erik-fryscok/erikfryscok.com` repository.

- [ ] **Step 3: Configure build settings**

Use these exact values:

| Setting | Value |
| --- | --- |
| Project name | `erikfryscok` |
| Production branch | `main` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node.js version | `24` (select from dropdown) |

Do NOT enable any advanced settings:
- No environment variables needed (the site has no runtime config)
- No "Skip dependency detection" — let Cloudflare detect `package-lock.json`
- No "Build splitting" — single-page static site, not needed yet

- [ ] **Step 4: Create the project**

Click "Save and deploy". Cloudflare Pages will check out `main`, install dependencies from `package-lock.json`, run `npm run build`, and deploy the `dist/` output.

- [ ] **Step 5: Wait for first deployment**

Monitor the deployment in the Pages dashboard (1-3 minutes). Verify:
- Build log shows `npm run build` completed without errors
- Deployment status shows "Published"
- The deployment URL follows the pattern `erikfryscok.pages.dev`

- [ ] **Step 6: Verify the preview deployment**

Open the deployment URL in a browser. Confirm the page loads with HTTP 200, the heading is visible, and Tailwind CSS styling is applied. Record the deployment URL for the documentation task.

---

### Task 2: Document the Delivery Path

**Files:**
- Create: `docs/development/deployment.md`
- Modify: `docs/README.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: The deployment URL from Task 1 (placeholder used, updated after Task 1)
- Produces: Documentation that future implementers use for #6 (domain connection) and #7 (launch validation)

- [ ] **Step 1: Create the deployment documentation**

Create `docs/development/deployment.md` with the following content:

```markdown
# Deployment

## Cloudflare Pages

The site is deployed through Cloudflare Pages using the GitHub integration.

### Build configuration

| Setting | Value |
| --- | --- |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node.js version | `24` |
| Production branch | `main` |

### Deployment URLs

- **Preview:** Automatic preview deployments are created for every branch push and pull request.
- **Production:** Deployed automatically on merges to `main`.

### Local preview

Run `npm run preview` to serve the production build locally before deploying.

### Environment variables

None required. The site is fully static with no runtime configuration.

### Adding environment variables

If a future feature requires environment variables:

1. Add the variable in Cloudflare Pages > Project settings > Environment variables.
2. Add a corresponding `.env.example` entry (never commit actual values).
3. Reference via `import.meta.env.VARIABLE_NAME` in Astro code.

### Preview deployment workflow

1. Push a branch to GitHub.
2. Cloudflare Pages automatically creates a preview deployment.
3. The preview URL appears in the Pages dashboard and as a commit comment.
4. Review the preview at the generated `*.pages.dev` URL.
5. Merge to `main` for production deployment.
```

- [ ] **Step 2: Update the documentation index**

In `docs/README.md`, insert a new "Deployment" section between "Direction and history" and "Implementation plans":

```markdown
## Deployment

- [Deployment](development/deployment.md) — Cloudflare Pages delivery path and build configuration.
```

- [ ] **Step 3: Update the root README**

In `README.md`, add a "Deployment" section after the "Development" section:

```markdown
## Deployment

The site is deployed through Cloudflare Pages. See [the deployment documentation](docs/development/deployment.md) for build configuration, preview workflow, and local preview commands.
```

- [ ] **Step 4: Update CHANGELOG.md**

Under `## Unreleased`, add a new `### Added` section with:

```markdown
### Added

- Cloudflare Pages preview deployment for pre-launch review.
```

- [ ] **Step 5: Validate documentation links**

Confirm all new links resolve:
- `docs/development/deployment.md` exists and is readable
- `docs/README.md` links to it correctly
- `README.md` links to it correctly

- [ ] **Step 6: Run build to confirm nothing broke**

```bash
npm run build
npm run preview
```

Confirm the build still succeeds and the preview serves the root page.

- [ ] **Step 7: Commit**

```bash
git add docs/development/deployment.md docs/README.md README.md CHANGELOG.md
git commit -m "docs: document Cloudflare Pages preview deployment (issue #5)"
```

---

### Task 3: Push Branch and Create Pull Request

**Files:**
- Git operations only (branch creation, push, PR)

- [ ] **Step 1: Push the branch**

```bash
git push -u origin erikf/issue-5-cloudflare-pages-preview
```

This will trigger the first Cloudflare Pages preview deployment automatically.

- [ ] **Step 2: Verify the preview deployment**

Check the Cloudflare Pages dashboard for the new deployment from `erikf/issue-5-cloudflare-pages-preview`. Confirm it published successfully.

- [ ] **Step 3: Create the pull request**

Create a PR with title: "Configure Cloudflare Pages preview deployment"

Body:
```markdown
Closes #5

## Changes

- Connected repository to Cloudflare Pages with GitHub integration
- Configured build: `npm run build`, output `dist`, Node 24
- Documented the delivery path, build configuration, and preview workflow
- Added deployment section to root README

## Preview

The preview deployment is available at the Cloudflare Pages dashboard.

## Completion criteria

- [x] The repository is connected to Cloudflare Pages
- [x] A preview deployment is available for the site
- [x] The delivery path and any required environment configuration are documented
```

---

## Self-Review

**1. Spec coverage:**
- ✅ "Repository connected to Cloudflare Pages" → Task 1, Steps 2-4
- ✅ "Preview deployment available" → Task 1, Step 6 + Task 3, Step 2
- ✅ "Delivery path documented" → Task 2, Step 1 (deployment.md)
- ✅ "Environment configuration documented" → Task 2, Step 1 (env variables section)

**2. Placeholder scan:**
- No "TBD", "TODO", or "implement later"
- No vague "add validation" — each step has concrete actions
- No "write tests" without test code — N/A for infra task, but validation steps are explicit
- No "similar to Task N" — each step is self-contained

**3. Type/signature consistency:**
- N/A — no code interfaces; this is infrastructure + documentation

**4. Consistency with existing conventions:**
- Branch naming: `erikf/issue-5-cloudflare-pages-preview` matches `erikf/issue-N-short-description` convention
- Documentation in `docs/development/` — follows `docs/` hierarchy
- CHANGELOG entry under `## Unreleased` — matches existing pattern
- `Closes #5` in PR — matches delivery contract

**5. Boundary check:**
- Does NOT add Cloudflare adapter (that's for production domain in #6)
- Does NOT add custom domain (that's #6)
- Does NOT add analytics (deferred per product brief)
- Does NOT change Astro config (build already works with static output)
