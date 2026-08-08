import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

async function readProjectFile(path) {
  return readFile(new URL(path, root), "utf8");
}

test("Projects page features the personal website case study", async () => {
  const page = await readProjectFile("src/pages/projects.astro");

  assert.match(page, /erikfryscok\.com/);
  assert.match(page, /\/projects\/personal-website/);
  assert.doesNotMatch(page, /Local AI Infrastructure for Software Teams/);
});

test("personal website case study links the live site, source, and project board", async () => {
  const page = await readProjectFile("src/pages/projects/personal-website.astro");

  assert.match(page, /https:\/\/erikfryscok\.com/);
  assert.match(page, /https:\/\/github\.com\/erik-fryscok\/erikfryscok\.com/);
  assert.match(page, /https:\/\/github\.com\/users\/erik-fryscok\/projects\/73/);
  assert.match(page, /Proton Mail/);
  assert.match(page, /Cloudflare Pages/);
});

test("project links distinguish internal and external destinations", async () => {
  const card = await readProjectFile("src/components/ProjectCard.astro");

  assert.match(card, /external: boolean/);
  assert.match(card, /link\.external/);
});
