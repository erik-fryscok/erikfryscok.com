# Changelog

All notable user-visible changes to the website are documented here.

The site may deploy continuously. This changelog records meaningful product releases rather than every deployment.

## Unreleased

### Fixed

- Mobile navigation overflow — added hamburger menu for screens below 1024px (issue #25).
- Corrected LinkedIn profile URL slug on Contact page (`erik-fryscok`).

### Added

- Home page with hero section, introduction, selected work grid, and contact CTA (issue #11).
- Placeholder pages for About, Writing, and Projects with shared BaseLayout.
- Cloudflare Pages preview deployment for pre-launch review.
- About page with professional narrative, engineering philosophy, leadership approach, and interests (issue #12).
- Projects page with curated case study cards (issue #14).
- Type declaration for `key` prop in Astro templates to support `.map()` reconciliation.
- Project-level OpenCode configuration with separate GitHub read/publish MCP servers, exact tool allowlists, and manually approved publishing agent.
- Full OpenCode agent roster: customized Plan, Build, Chat, and Review primaries; re-enabled General, Explore, and Scout subagents; new documentation, security, and code-review specialists orchestrated by Review; per-agent model assignments from OpenCode Zen.
- Favicon with SVG, PNG, and Apple Touch Icon for cross-platform browser support (issue #24).
- Web App Manifest for Android Chrome home-screen installation (issue #24).
- Site logo in navigation header replacing plain-text brand (issue #24).
- Writing article: "OpenCode Configuration Guide" covering agent architecture, permission controls, and practical AI delivery ROI.

### Changed

- Established the documentation and project-lifecycle foundation for the site.
- Added Astro, TypeScript, and Tailwind CSS foundation (issue #2).
