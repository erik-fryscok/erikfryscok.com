# Launch Readiness

This document defines the repeatable validation contract for a public website
release. GitHub issue #7 holds live evidence, current status, and release
discussion; this document intentionally does not duplicate them.

## Automated gate

Run the complete built-site gate before requesting a preview:

```bash
npm test
git diff --check
```

`npm test` runs Astro and TypeScript diagnostics, generates the static site,
and verifies the public pages, metadata, internal links, sitemap, and 404
output. Review changed Markdown links and the public diff for confidential or
non-public material before publishing.

## Preview and production gate

For the Cloudflare Pages preview and again on the canonical production domain:

1. Confirm the nine indexable routes return HTTP 200 and an unknown route
   returns HTTP 404.
2. Confirm HTTP redirects to HTTPS in production.
3. Confirm canonical URLs use `https://erikfryscok.com`, the sitemap index and
   its child sitemap return XML, and the sitemap contains each indexable route
   but not the 404 page.
4. Confirm Cloudflare-managed `robots.txt` permits search crawling and does
   not contain a site-wide `Disallow: /`. Do not replace its managed crawler
   policy with a repository-owned file.
5. Run Lighthouse Accessibility and SEO audits for each public route and the
   404 page; require scores of 100.
6. Check keyboard order, skip-link behavior, focus treatment, mobile-menu
   open/close/Escape behavior, landmarks, headings, accessible names, and
   layouts at 320, 768, 1024, and 1440 pixels plus 200% zoom.
7. Open external links and verify the email link. If an automated probe is
   blocked by the destination, record a manual confirmation instead.

Record the preview URL, production URL, commit SHA, automated results, manual
audit matrix, and resolved findings in the source GitHub issue.

## Release notes

Keep launch changes under `Unreleased` while production checks are pending.
After the production gate passes, create a release-finalization commit that
adds an empty `Unreleased` heading and promotes the accumulated notes to
`1.0.0` using that day's actual release date. GitHub release publication and
tagging remain separate release-management work.
