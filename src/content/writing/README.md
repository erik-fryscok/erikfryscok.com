# Writing Content Directory

This directory will hold Markdown-based articles for the Writing page.

## Future Convention

When articles are ready to publish, each will be a `.md` file in this directory with front matter:

```markdown
---
title: "Article Title"
date: 2025-01-15
summary: "A brief description of the article."
---

Article content here...
```

The Writing page (`src/pages/writing.astro`) will be updated to list and render these articles using Astro's content collection or file-based listing pattern. MDX is deferred until there is a demonstrated need.

## Content Boundaries

See `docs/product/brief.md` — internal experience can inform articles, but content must be rewritten as generalized patterns, lessons, and architectures. Do not publish employer or client confidential information.
