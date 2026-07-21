# Personal Website

Status: active planning

## Repository setup decision

The initial GitHub repository settings are:

- Owner: `erik-fryscok`
- Repository: `erikfryscok.com`
- Visibility: Public
- README: Enabled
- `.gitignore`: GitHub’s Node template
- License: None

The repository is public for discoverability and portfolio value. No license was added because the repository may contain personal content, branding, images, and employer-informed ideas. Revisit licensing once the code/content boundary is clearer.

## Purpose

Create a professional home base that explains who Erik is, demonstrates useful thinking and selected work, and makes contact easy. The site should support future consulting, writing, digital products, speaking, and selected public projects without requiring any of those to launch.

## Initial message

**Headline**

> Building better software teams with AI, automation, and modern engineering practices.

**Supporting copy**

> I’m a software development team lead focused on engineering leadership, AI-enabled development, cloud infrastructure, documentation, and practical systems that help teams work more effectively.

## First release scope

- Home — message, short introduction, selected writing/projects, and a contact path.
- About — story, interests, engineering philosophy, and leadership approach; not a résumé dump.
- Writing — initially a simple landing page, later Markdown-based articles.
- Projects — a small set of meaningful case studies rather than every repository.
- Contact — a clear way to get in touch.

## Technical direction

| Area | Decision |
| --- | --- |
| Framework | Astro |
| Language | TypeScript, strict mode |
| Styling | Tailwind CSS |
| Content | Markdown initially; MDX only when needed |
| Hosting | Cloudflare Pages |
| Analytics | Cloudflare Web Analytics, after launch |
| Source control | Public GitHub repository |

## Content boundaries

Internal experience can inform projects and articles, but content must be rewritten as generalized patterns, lessons, and architectures. Do not publish employer or client confidential information, proprietary source code, credentials, non-public designs, or internal project details.

## Next actions

1. Confirm domain availability and purchase the preferred personal-name domain.
2. Create a public repository (suggested: `erikfryscok.com` or `personal-website`).
3. Scaffold an Astro minimal project with strict TypeScript and Git.
4. Add Tailwind CSS.
5. Build the five-page skeleton and publish a simple first version.
6. Connect the repository to Cloudflare Pages and set up automatic deployment from `main`.

## Deferred until there is a need

- MDX
- Sitemap and RSS
- Syntax highlighting
- Site search (useful after a substantial writing archive)
- Newsletter
- Comments
- Courses, paid products, and a SaaS surface
