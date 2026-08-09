# GitHub Issue #7: Public Launch Readiness

Source: [GitHub issue #7](https://github.com/erik-fryscok/erikfryscok.com/issues/7)

## Outcome

Establish a lightweight, reusable launch gate for the public site by improving
accessibility and search metadata, generating a sitemap, correcting 404
behavior, and documenting preview and production verification.

## Implementation

1. Add built-site tests for the nine indexable routes, metadata, links,
   sitemap output, and the excluded noindex 404 page.
2. Extend `BaseLayout` with required descriptions, page type, and indexability;
   emit canonical, Open Graph, Twitter, and sitemap-discovery metadata.
3. Configure Astro with `site: "https://erikfryscok.com"` and the official
   sitemap integration while retaining Cloudflare-managed `robots.txt`.
4. Add the shared accessibility improvements: skip link, visible focus styles,
   ordinary navigation semantics, active-route state, and an accessible 404
   page that Cloudflare Pages serves with HTTP 404.
5. Record the durable launch-validation contract, sitemap decision, and
   user-visible release notes in project documentation.

## Metadata Contract

`BaseLayout` accepts `title`, `description`, optional `pageType` (`website` or
`article`), and optional `indexable` (default `true`). Indexable pages emit a
production canonical URL and Open Graph URL; non-indexable pages emit
`robots=noindex,follow` and omit both URL tags.

Every public page receives its approved unique description. The two writing
articles and the personal website case study use `pageType="article"`.

## Validation Gates

- `npm test`, `git diff --check`, and changed Markdown-link validation pass.
- Preview and production return 200 for every indexable route and 404 for an
  unknown route; HTTP redirects to HTTPS in production.
- The generated sitemap contains the nine indexable canonical URLs and excludes
  404; Cloudflare-managed robots allows search crawling.
- Lighthouse Accessibility and SEO score 100 for every public route plus 404.
- Keyboard, responsive, zoom, external-link, and production smoke checks are
  recorded on issue #7 before it is closed.
- After production passes, promote the launch notes to `1.0.0` with the actual
  release date while retaining an empty `Unreleased` heading.

## Boundaries

Analytics, RSS, search, social-preview artwork, content redesigns, DNS changes,
Git tagging, and GitHub Release publication remain out of scope.
