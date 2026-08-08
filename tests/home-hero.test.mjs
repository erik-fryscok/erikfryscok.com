import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);
const expectedAlt =
  "Erik Fryscok smiling outdoors with a city street in the background.";

test("the built Home page serves Erik's optimized portrait", async () => {
  const html = await readFile(new URL("dist/index.html", projectRoot), "utf8");
  const imageTags = html.match(/<img\b[^>]*>/g) ?? [];
  const portrait = imageTags.find((tag) => tag.includes(`alt="${expectedAlt}"`));

  assert.ok(portrait, "expected the Home page to contain Erik's portrait");

  const source = portrait.match(/src="([^"]+)"/)?.[1];
  assert.match(source ?? "", /^\/_astro\/erik-fryscok-portrait\.[^/]+\.webp$/);
  await access(new URL(`dist${source}`, projectRoot));
});
