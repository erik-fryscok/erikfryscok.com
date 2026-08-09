import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);

async function readProjectFile(path) {
  return readFile(new URL(path, root), "utf8");
}

async function readBuiltProject(path) {
  return readFile(new URL(`dist/${path}/index.html`, root), "utf8");
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

test("Agent Skills leads the built projects page with case study and source links", async () => {
  const page = await readBuiltProject("projects");
  const agentSkillsHeading = page.indexOf(">Agent Skills</h2>");
  const websiteHeading = page.indexOf(">erikfryscok.com</h2>");

  assert.ok(agentSkillsHeading !== -1 && agentSkillsHeading < websiteHeading);
  assert.match(page, /href="\/projects\/agent-skills"/);
  assert.match(page, /href="https:\/\/github\.com\/erik-fryscok\/skills"/);
});

test("Agent Skills case study documents CLI use, prompts, output, and project links", async () => {
  const page = await readBuiltProject("projects/agent-skills");

  assert.match(page, /npx skills add erik-fryscok\/skills/);
  assert.match(page, /npx skills use erik-fryscok\/skills@github-public-readiness/);
  assert.match(page, /Use \$github-public-readiness to audit this repository for safe public release and portfolio value\./);
  assert.match(page, /Audit this repository before I make it public\. Prioritize disclosure risks and the smallest release checklist; do not modify files or visibility\./);
  assert.match(page, /Assess whether this repository is worth featuring in my portfolio, keeping public safety and showcase value as separate verdicts\./);
  assert.match(page, /readiness classification/);
  assert.match(page, /separate portfolio judgment/);
  assert.match(page, /evidence-linked findings/);
  assert.match(page, /ordered release checklist/);
  assert.match(page, /verification performed/);
  assert.match(page, /href="https:\/\/github\.com\/erik-fryscok\/skills"/);
  assert.match(page, /href="https:\/\/github\.com\/erik-fryscok\/skills\/tree\/main\/skills\/github-public-readiness"/);
});
