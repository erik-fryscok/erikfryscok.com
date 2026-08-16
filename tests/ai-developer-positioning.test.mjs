import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const headline = "Building practical AI systems for software development.";
const supportingCopy =
  "I’m a software development team lead and hands-on engineer working with coding agents, local and cloud-hosted models, developer tooling, evaluations, cloud infrastructure, and the systems that help engineering teams ship better software.";
const introduction =
  "I build and evaluate the systems around AI-assisted software development: agent workflows, developer tooling, model experiments, and the guardrails that make them useful in real teams. My leadership experience shapes the work—clear evidence, honest capability boundaries, maintainable systems, and better engineering outcomes over novelty.";
const collaborationCopy =
  "I’m interested in hands-on AI/software engineering roles, engineering leadership opportunities, and collaborations around agents, evaluations, model selection, and developer tooling.";
const proofDescriptions = [
  "An experimental learning and evaluation environment for AI model systems, exploring local llama.cpp and cloud-hosted OpenAI-compatible providers, routing, compatibility, benchmarks, and capability boundaries.",
  "Reusable, evidence-backed workflows that turn practical engineering judgment into dependable instructions for AI coding agents.",
  "What customizing coding agents, building evaluations, weighing usage costs, and testing workflow continuity taught me.",
];

test("Home leads with practical AI systems and ordered, calibrated proof", async () => {
  const html = await readFile(new URL("dist/index.html", root), "utf8");
  const visibleText = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
  const systemsLabPosition = html.indexOf(">AI Systems Lab</h3>");
  const agentSkillsPosition = html.indexOf(">Agent Skills</h3>");
  const codexPosition = html.indexOf(">Why I Keep Coming Back to Codex</h3>");

  assert.ok(visibleText.includes(headline));
  assert.ok(visibleText.includes(supportingCopy));
  assert.ok(visibleText.includes(introduction));
  assert.ok(visibleText.includes(collaborationCopy));
  for (const description of proofDescriptions) assert.ok(visibleText.includes(description));

  assert.ok(systemsLabPosition >= 0, "expected AI Systems Lab proof on Home");
  assert.ok(systemsLabPosition < agentSkillsPosition, "expected AI Systems Lab before Agent Skills");
  assert.ok(agentSkillsPosition < codexPosition, "expected Agent Skills before the Codex article");
  assert.match(
    html,
    /<a href="\/projects\/ai-systems-lab" class="[^"]*sm:col-span-2[^"]*"><p[^>]*>EXPERIMENTAL<\/p><h3[^>]*>AI Systems Lab<\/h3>/,
  );
  assert.match(html, /href="\/projects\/ai-systems-lab"/);
  assert.doesNotMatch(html, /Local AI Lab|\/projects\/local-ai-lab/);
  assert.match(html, /href="\/projects\/agent-skills"/);
  assert.match(html, /href="\/writing\/why-i-keep-coming-back-to-codex"/);
});

test("Writing describes model-system work across local and cloud environments", async () => {
  const html = await readFile(new URL("dist/writing/index.html", root), "utf8");
  const visibleText = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");

  assert.ok(
    visibleText.includes(
      "I write about AI-assisted software engineering, evaluations and reliability, local and cloud model systems, developer tooling, and the leadership practices that help teams adopt AI with appropriate judgment.",
    ),
  );
  assert.doesNotMatch(html, /local and open-weight model experiments/i);
});
