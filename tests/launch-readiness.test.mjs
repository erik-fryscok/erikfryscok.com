import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const site = "https://erikfryscok.com";

const pages = [
  {
    path: "/",
    file: "dist/index.html",
    title: "Erik Fryscok — Software Engineering Leadership",
    description:
      "Erik Fryscok on software engineering leadership, AI-enabled development, cloud infrastructure, and practical systems for better teams.",
    pageType: "website",
  },
  {
    path: "/about",
    file: "dist/about/index.html",
    title: "About — Erik Fryscok",
    description:
      "Learn how Erik Fryscok approaches engineering leadership, AI-enabled development, documentation, developer experience, and sustainable software delivery.",
    pageType: "website",
  },
  {
    path: "/now",
    file: "dist/now/index.html",
    title: "Now — Erik Fryscok",
    description:
      "What Erik Fryscok is focused on now: better engineering systems, practical AI-enabled development, guitar, and local cycling.",
    pageType: "website",
  },
  {
    path: "/writing",
    file: "dist/writing/index.html",
    title: "Writing — Erik Fryscok",
    description:
      "Articles by Erik Fryscok on engineering leadership, AI-enabled development, cloud infrastructure, documentation, and practical software systems.",
    pageType: "website",
  },
  {
    path: "/writing/opencode-configuration-guide",
    file: "dist/writing/opencode-configuration-guide/index.html",
    title: "OpenCode Configuration Guide — Erik Fryscok",
    description:
      "A practical guide to configuring OpenCode agents with role separation, permissions, approval gates, and measurable delivery outcomes.",
    pageType: "article",
  },
  {
    path: "/writing/why-i-keep-coming-back-to-codex",
    file: "dist/writing/why-i-keep-coming-back-to-codex/index.html",
    title: "Why I Keep Coming Back to Codex — Erik Fryscok",
    description:
      "Why Erik Fryscok chose Codex as a daily coding agent after evaluating configuration, workflow continuity, and usage costs.",
    pageType: "article",
  },
  {
    path: "/projects",
    file: "dist/projects/index.html",
    title: "Projects — Erik Fryscok",
    description:
      "Selected projects and case studies from Erik Fryscok on practical engineering, delivery systems, AI-enabled development, and modern infrastructure.",
    pageType: "website",
  },
  {
    path: "/projects/personal-website",
    file: "dist/projects/personal-website/index.html",
    title: "erikfryscok.com — Project Case Study",
    description:
      "How erikfryscok.com combines Astro, Cloudflare Pages, GitHub, an owned domain, and documented delivery practices.",
    pageType: "article",
  },
  {
    path: "/contact",
    file: "dist/contact/index.html",
    title: "Contact — Erik Fryscok",
    description:
      "Contact Erik Fryscok about software engineering leadership, AI-enabled development, collaboration, and new opportunities.",
    pageType: "website",
  },
];

function canonicalURL(path) {
  return new URL(path === "/" ? path : `${path}/`, site).href;
}

async function readBuiltFile(path) {
  return readFile(new URL(path, root), "utf8");
}

async function fileExists(path) {
  try {
    await access(new URL(path, root));
    return true;
  } catch {
    return false;
  }
}

function builtPathFor(href) {
  const pathname = new URL(href, site).pathname;
  if (pathname === "/") return "dist/index.html";
  if (/\.[a-z0-9]+$/i.test(pathname)) return `dist${pathname}`;
  return `dist${pathname}/index.html`;
}

test("each public route emits unique, production-ready metadata", async () => {
  const titles = new Set();
  const descriptions = new Set();

  for (const page of pages) {
    const html = await readBuiltFile(page.file);
    const canonical = canonicalURL(page.path);

    assert.match(html, new RegExp(`<title>${page.title}</title>`));
    assert.match(html, new RegExp(`<meta name="description" content="${page.description}">`));
    assert.match(html, new RegExp(`<link rel="canonical" href="${canonical}">`));
    assert.match(html, new RegExp(`<meta property="og:title" content="${page.title}">`));
    assert.match(html, new RegExp(`<meta property="og:description" content="${page.description}">`));
    assert.match(html, new RegExp(`<meta property="og:type" content="${page.pageType}">`));
    assert.match(html, new RegExp(`<meta property="og:url" content="${canonical}">`));
    assert.match(html, /<meta property="og:site_name" content="Erik Fryscok">/);
    assert.match(html, /<meta name="twitter:card" content="summary">/);
    assert.match(html, new RegExp(`<meta name="twitter:title" content="${page.title}">`));
    assert.match(html, new RegExp(`<meta name="twitter:description" content="${page.description}">`));
    assert.match(html, /<link rel="sitemap" href="\/sitemap-index\.xml">/);
    assert.equal((html.match(/<h1\b/g) ?? []).length, 1, `${page.path} needs one h1`);

    for (const image of html.match(/<img\b[^>]*>/g) ?? []) {
      assert.match(image, /\balt="[^"]*"/, `${page.path} has an image without alt text`);
    }

    titles.add(page.title);
    descriptions.add(page.description);
  }

  assert.equal(titles.size, pages.length, "page titles must be unique");
  assert.equal(descriptions.size, pages.length, "page descriptions must be unique");
});

test("built internal links resolve to generated pages or assets", async () => {
  for (const page of pages) {
    const html = await readBuiltFile(page.file);
    const links = html.match(/\bhref="[^"]+"/g) ?? [];

    for (const attribute of links) {
      const href = attribute.slice(6, -1);
      if (!href.startsWith("/") || href.startsWith("//")) continue;

      assert.equal(
        await fileExists(builtPathFor(href)),
        true,
        `${page.path} links to a missing built target: ${href}`,
      );
    }
  }
});

test("the generated sitemap contains every indexable public URL and excludes 404", async () => {
  assert.equal(await fileExists("dist/sitemap-index.xml"), true, "expected sitemap index");

  const index = await readBuiltFile("dist/sitemap-index.xml");
  const sitemapPath = index.match(/<loc>https:\/\/erikfryscok\.com\/([^<]+)<\/loc>/)?.[1];

  assert.ok(sitemapPath, "expected sitemap index to reference a sitemap file");

  const sitemap = await readBuiltFile(`dist/${sitemapPath}`);
  for (const page of pages) {
    assert.match(sitemap, new RegExp(`<loc>${canonicalURL(page.path)}</loc>`));
  }
  assert.doesNotMatch(sitemap, /<loc>https:\/\/erikfryscok\.com\/404\/?<\/loc>/);
});

test("the generated 404 page is discoverable to visitors but excluded from indexing", async () => {
  assert.equal(await fileExists("dist/404.html"), true, "expected a generated 404 page");

  const html = await readBuiltFile("dist/404.html");

  assert.match(html, /<meta name="robots" content="noindex,follow">/);
  assert.doesNotMatch(html, /<link rel="canonical"/);
  assert.doesNotMatch(html, /<meta property="og:url"/);
  assert.match(html, /href="\/"[^>]*>Home/);
  assert.match(html, /href="\/contact"[^>]*>Contact/);
});

test("the shared shell provides standard navigation and a keyboard skip link", async () => {
  const html = await readBuiltFile("dist/index.html");

  assert.match(html, /href="#main-content"[^>]*>Skip to main content/);
  assert.match(html, /<main id="main-content"/);
  assert.doesNotMatch(html, /role="menu"/);
  assert.doesNotMatch(html, /role="menuitem"/);
  assert.match(html, /href="\/"[^>]*aria-current="page"[^>]*>Home/);

  const article = await readBuiltFile("dist/writing/opencode-configuration-guide/index.html");
  assert.match(article, /href="\/writing"[^>]*aria-current="page"[^>]*>Writing/);

  const caseStudy = await readBuiltFile("dist/projects/personal-website/index.html");
  assert.match(caseStudy, /href="\/projects"[^>]*aria-current="page"[^>]*>Projects/);
});
