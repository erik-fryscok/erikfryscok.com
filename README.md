# erikfryscok.com
Personal website and technical portfolio focused on AI systems for software development, including coding agents, evaluations, local and cloud model systems, developer tooling, and engineering leadership.

## Current focus

- Establish a professional home base for future writing, consulting, products, and selected projects.

## Project tracking

Current work, release scope, and delivery status are maintained in the [public GitHub Project](https://github.com/users/erik-fryscok/projects/73) and repository issues. Durable context lives in [the documentation](docs/README.md).

## Documentation

Read [the documentation index](docs/README.md) for product intent, strategy, decisions, ideas, journal entries, and the project lifecycle.

## Development

The following npm scripts are available for local development:

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Astro development server. |
| `npm run check` | Run Astro and TypeScript diagnostics. |
| `npm test` | Create a production build and run repository regression tests. |
| `npm run build` | Run diagnostics then create a production build. |
| `npm run preview` | Serve the production build locally for verification. |

## Releases

User-visible changes are recorded in [CHANGELOG.md](CHANGELOG.md). Formal product checkpoints are published as [GitHub Releases](https://github.com/erik-fryscok/erikfryscok.com/releases); ordinary merges may deploy continuously without becoming a formal release.

## Deployment

This site is hosted on [Cloudflare Pages](https://pages.cloudflare.com/). The canonical production URL is:

```
https://erikfryscok.com
```

Cloudflare Pages also provides `https://erikfryscok.pages.dev` as the platform endpoint. Preview deployments from feature branches are available through the Cloudflare Pages dashboard. See [the deployment documentation](docs/development/deployment.md) for build configuration and the preview workflow.
