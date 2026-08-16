import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const sourceRepository = "https://github.com/erik-fryscok/ai-systems-lab";
const projectDescription =
  "An experimental learning and evaluation environment for AI model systems, exploring provider-neutral routing, model lifecycle, compatibility, benchmarks, and local llama.cpp and cloud-hosted OpenAI-compatible capability boundaries.";
const projectsIntroduction =
  "Selected projects showing how I build, test, and reason about AI developer systems. AI Systems Lab is an experimental learning environment; Agent Skills is the more directly reusable developer workflow project.";
const prohibitedClaimPatterns = [
  /\b(?:is|appears|offers|provides|serves as)\s+(?!not\b)(?:(?:an?\s+)?production(?:-ready)?(?:\s+(?:solution|architecture|infrastructure|system))?|ready\s+for\s+production)\b/i,
  /\b(?:(?:can\s+)?replaces?|(?:is|serves as)\s+(?!not\b)(?:a\s+)?replacement for)\s+(?:flagship\s+)?frontier(?:\s+cloud)?\s+models\b/i,
  /\b(?:viable|suitable|effective|ready|works)\s+for\s+(?:every|all)\s+workloads?\b/i,
];

async function readBuiltFile(path) {
  return readFile(new URL(path, root), "utf8");
}

test("AI Systems Lab leads Projects with calibrated framing and working project links", async () => {
  const html = await readBuiltFile("dist/projects/index.html");
  const visibleText = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
  const systemsLabPosition = html.indexOf(">AI Systems Lab</h2>");
  const agentSkillsPosition = html.indexOf(">Agent Skills</h2>");
  const websitePosition = html.indexOf(">erikfryscok.com</h2>");

  assert.ok(systemsLabPosition >= 0, "expected AI Systems Lab on Projects");
  assert.ok(systemsLabPosition < agentSkillsPosition, "expected AI Systems Lab before Agent Skills");
  assert.ok(agentSkillsPosition < websitePosition, "expected Agent Skills before erikfryscok.com");
  assert.match(
    html,
    /<article[^>]*><p[^>]*>EXPERIMENTAL<\/p><h2[^>]*>AI Systems Lab<\/h2>/,
  );
  assert.ok(visibleText.includes(projectsIntroduction));
  assert.ok(visibleText.includes(projectDescription));
  for (const evidence of [
    "Python",
    "llama.cpp",
    "OpenAI-compatible APIs",
    "Hugging Face",
    "JSONL",
    "Workload-specific model aliases across local llama.cpp and cloud-hosted OpenAI-compatible provider backends",
    "Compatibility gates for visible completions and structured tool calls",
    "Layered throughput, server-path, and quality evaluation workflows",
  ]) {
    assert.ok(visibleText.includes(evidence), `expected Projects to include: ${evidence}`);
  }
  assert.match(html, /href="\/projects\/ai-systems-lab"[^>]*>Read case study<\/a>/);
  assert.match(
    html,
    new RegExp(`href="${sourceRepository}"[^>]*target="_blank"[^>]*>Source</a>`),
  );
});

test("AI Systems Lab documents compatibility, layered evaluation, and bounded use", async () => {
  const html = await readBuiltFile("dist/projects/ai-systems-lab/index.html");

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
  for (const evidence of [
    "local llama.cpp remains a first-class backend",
    "cloud-hosted OpenAI-compatible providers participate in the same chat and evaluation paths",
    "provider-neutral request path",
    "provider-specific request construction",
    "credentials are opt-in environment variables",
  ]) {
    assert.match(html, new RegExp(evidence, "i"));
  }

  for (const pattern of prohibitedClaimPatterns) assert.doesNotMatch(html, pattern);
});

test("claim guards reject direct prohibited variants but allow explicit boundaries", () => {
  const prohibitedClaims = [
    "AI Systems Lab is a replacement for frontier cloud models.",
    "AI Systems Lab is ready for production.",
  ];
  const missedClaims = prohibitedClaims.filter(
    (claim) => !prohibitedClaimPatterns.some((pattern) => pattern.test(claim)),
  );

  assert.deepEqual(missedClaims, [], "expected guards to reject every prohibited claim variant");

  for (const boundary of [
    "AI Systems Lab is not production infrastructure.",
    "AI Systems Lab is not a replacement for frontier cloud models.",
  ]) {
    assert.equal(
      prohibitedClaimPatterns.some((pattern) => pattern.test(boundary)),
      false,
      `expected guard to allow: ${boundary}`,
    );
  }
});
