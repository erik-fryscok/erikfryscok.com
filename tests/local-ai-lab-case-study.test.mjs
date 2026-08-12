import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const sourceRepository = "https://github.com/erik-fryscok/local-ai-lab";
const projectDescription =
  "An experimental learning and evaluation environment for local and open-weight models, exploring routing, model lifecycle, compatibility, benchmarks, and the boundary between useful local work and tasks that still require frontier cloud models.";
const projectsIntroduction =
  "Selected projects showing how I build, test, and reason about AI developer systems. Local AI Lab is an experimental learning environment; Agent Skills is the more directly reusable developer workflow project.";
const prohibitedClaimPatterns = [
  /\b(?:is|appears|offers|provides|serves as)\s+(?!not\b)(?:(?:an?\s+)?production(?:-ready)?(?:\s+(?:solution|architecture|infrastructure|system))?|ready\s+for\s+production)\b/i,
  /\b(?:(?:can\s+)?replaces?|(?:is|serves as)\s+(?!not\b)(?:a\s+)?replacement for)\s+(?:flagship\s+)?frontier(?:\s+cloud)?\s+models\b/i,
  /\b(?:viable|suitable|effective|ready|works)\s+for\s+(?:every|all)\s+workloads?\b/i,
];

async function readBuiltFile(path) {
  return readFile(new URL(path, root), "utf8");
}

test("Local AI Lab leads Projects with calibrated framing and working project links", async () => {
  const html = await readBuiltFile("dist/projects/index.html");
  const visibleText = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
  const localLabPosition = html.indexOf(">Local AI Lab</h2>");
  const agentSkillsPosition = html.indexOf(">Agent Skills</h2>");
  const websitePosition = html.indexOf(">erikfryscok.com</h2>");

  assert.ok(localLabPosition >= 0, "expected Local AI Lab on Projects");
  assert.ok(localLabPosition < agentSkillsPosition, "expected Local AI Lab before Agent Skills");
  assert.ok(agentSkillsPosition < websitePosition, "expected Agent Skills before erikfryscok.com");
  assert.match(
    html,
    /<article[^>]*><p[^>]*>EXPERIMENTAL<\/p><h2[^>]*>Local AI Lab<\/h2>/,
  );
  assert.ok(visibleText.includes(projectsIntroduction));
  assert.ok(visibleText.includes(projectDescription));
  for (const evidence of [
    "Python",
    "llama.cpp",
    "OpenAI-compatible APIs",
    "Hugging Face",
    "JSONL",
    "One endpoint with workload-specific model aliases and managed model lifecycle",
    "Compatibility gates for visible completions and structured tool calls",
    "Layered throughput, server-path, and quality evaluation workflows",
  ]) {
    assert.ok(visibleText.includes(evidence), `expected Projects to include: ${evidence}`);
  }
  assert.match(html, /href="\/projects\/local-ai-lab"[^>]*>Read case study<\/a>/);
  assert.match(
    html,
    new RegExp(`href="${sourceRepository}"[^>]*target="_blank"[^>]*>Source</a>`),
  );
});

test("Local AI Lab documents compatibility, layered evaluation, and bounded use", async () => {
  const html = await readBuiltFile("dist/projects/local-ai-lab/index.html");

  for (const heading of [
    "An experimental AI project",
    "What the lab explores",
    "Where local models are useful",
    "Where they fall short",
    "When to escalate",
    "Compatibility before promotion",
    "Layered evaluation",
    "Evidence boundaries",
    "What this demonstrates",
    "Explore the project",
  ]) {
    assert.match(html, new RegExp(`<h2[^>]*>${heading}</h2>`));
  }

  assert.match(html, /OpenAI-compatible aliases/);
  assert.match(html, /structured tool calls/);
  assert.match(html, /\.\/scripts\/lab bench-llama coder --all-candidates/);
  assert.match(html, /\.\/scripts\/lab bench-server coder --all-candidates --unload-after/);
  assert.match(html, /\.\/scripts\/lab bench-quality coder --all-candidates/);
  assert.match(html, /bounded experiments/);
  assert.match(html, /small targeted changes/);
  assert.match(html, /higher-stakes/);
  assert.match(html, /large-context/);
  assert.match(html, /reliability-critical/);
  assert.match(html, /frontier cloud models/);
  assert.match(html, /not production infrastructure/);
  assert.match(html, /<pre class="[^"]*overflow-x-auto[^"]*">/);
  assert.match(html, new RegExp(`href="${sourceRepository}"`));

  for (const pattern of prohibitedClaimPatterns) assert.doesNotMatch(html, pattern);
});

test("claim guards reject direct prohibited variants but allow explicit boundaries", () => {
  const prohibitedClaims = [
    "Local AI Lab is a replacement for frontier cloud models.",
    "Local AI Lab is ready for production.",
  ];
  const missedClaims = prohibitedClaims.filter(
    (claim) => !prohibitedClaimPatterns.some((pattern) => pattern.test(claim)),
  );

  assert.deepEqual(missedClaims, [], "expected guards to reject every prohibited claim variant");

  for (const boundary of [
    "Local AI Lab is not production infrastructure.",
    "Local AI Lab is not a replacement for frontier cloud models.",
  ]) {
    assert.equal(
      prohibitedClaimPatterns.some((pattern) => pattern.test(boundary)),
      false,
      `expected guard to allow: ${boundary}`,
    );
  }
});
