# Agent Skills Case Study — Design

Related work: [GitHub issue #40](https://github.com/erik-fryscok/erikfryscok.com/issues/40)

## Goal

Present [Agent Skills](https://github.com/erik-fryscok/skills) as the leading project on the website and explain how its first shipped skill turns a practical software-development review into a reusable, evidence-backed agent workflow.

The case study should demonstrate the design of the tooling without implying adoption, a delivered plugin catalogue, or a mature ecosystem. At launch, `github-public-readiness` is the only shipped skill featured.

## Public interfaces

- Repository: `https://github.com/erik-fryscok/skills`
- Website route: `/projects/agent-skills`
- CLI collection source: `erik-fryscok/skills`
- First skill slug: `github-public-readiness`
- First skill source: `https://github.com/erik-fryscok/skills/tree/main/skills/github-public-readiness`

## Project positioning

Use the title **Agent Skills** and the tagline “Reusable, evidence-backed agent skills for practical software development.” The project is an open-source collection of agent workflows, not a claim of broad adoption or a finished tooling platform.

Place Agent Skills first on `/projects`, followed by `erikfryscok.com`. Reuse the existing `ProjectCard` interface unchanged, with an internal case-study link and an external repository link.

## Case-study structure

Use the established narrow case-study layout and explain:

1. **Problem and purpose** — useful engineering judgment is often trapped in one-off prompts or personal habits; a skill makes the workflow inspectable and repeatable.
2. **Skill-package anatomy** — distinguish the workflow instructions, evaluation rubric, and report template so each concern can evolve without blurring evidence or presentation.
3. **Execution flow** — establish scope, inspect disclosure risks, review usability and repository hygiene, evaluate portfolio value separately, then return a verdict and ordered checklist.
4. **Safety and evidence design** — default to read-only inspection, cite concrete repository evidence, keep public-readiness and portfolio judgments separate, and avoid changing visibility or files unless explicitly requested.
5. **Reusable foundation** — describe additional skills and plugin packaging as future intent. Standalone plugins or MCP products may receive separate repositories when they become independent products.
6. **Practical usage** — include installation, one-off invocation, example prompts, expected report contents, and links to both the collection and first skill.

## CLI guidance

Show the collection install command and one-off skill invocation exactly:

```bash
npx skills add erik-fryscok/skills
npx skills use erik-fryscok/skills@github-public-readiness
```

Include three prompts that demonstrate the normal audit, a disclosure-first release review, and a portfolio-value assessment:

```text
Use $github-public-readiness to audit this repository for safe public release and portfolio value.
```

```text
Audit this repository before I make it public. Prioritize disclosure risks and the smallest release checklist; do not modify files or visibility.
```

```text
Assess whether this repository is worth featuring in my portfolio, keeping public safety and showcase value as separate verdicts.
```

Describe the expected output as a readiness classification, a separate portfolio judgment, evidence-linked findings, an ordered release checklist, and the verification performed. Do not promise a guaranteed safety outcome; the report summarizes inspected evidence and identified risks.

## Repository-name rationale

Use the generic `erik-fryscok/skills` name intentionally. The [skills CLI](https://github.com/vercel-labs/skills#install-a-skill) and [skills.sh API model](https://www.skills.sh/docs/api) foreground individual skill names while retaining `owner/repo` as source provenance, so a collection name supports multiple focused skills without making the repository itself the primary discovery label.

Preserve the former GitHub repository name as a redirect rather than reusing it. The local directory name does not need to match the renamed remote repository.

## Responsive and interaction design

- Preserve the existing Projects card behavior: the case-study link is internal and the repository link is external.
- Keep the case-study content in a narrow readable column with semantic heading order.
- Apply horizontal overflow handling to command and prompt containers so long CLI sources and prompts remain usable at 375px.
- Validate `/projects` and `/projects/agent-skills` at 375px and 1280px, including readable hierarchy, prompt overflow, and link behavior.

## Evidence boundaries

- Treat `github-public-readiness` as the only shipped skill featured at launch.
- Describe future skills, plugin manifests, and packaging only as direction or intent.
- Do not publish install counts, adoption metrics, delivered-plugin claims, or mature-ecosystem language without verifiable evidence.
- Keep all examples grounded in the public repository and its documented workflow; do not expose employer, client, credential, or non-public design information.

## Validation

- Build-output tests verify project ordering, route generation, CLI commands, prompts, expected report language, and repository links.
- `npm run check` and `npm test` complete successfully.
- `dist/projects/agent-skills/index.html` exists and contains the documented public interfaces.
- Repository searches identify unintended active references to `developer-skills`; historical planning context may be reported separately.
- Browser review covers 375px and 1280px layouts.

## Out of scope

- Claiming immediate skills.sh catalogue indexing as a release requirement.
- Adding or changing the `ProjectCard` interface.
- Shipping additional skills, plugins, or MCP products as part of the case study.
- Moving the full usage narrative into the repository README; the repository keeps a concise quick start.
