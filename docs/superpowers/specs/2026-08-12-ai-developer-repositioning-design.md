# AI Developer Website Repositioning — Design

Related work: [GitHub issue #42](https://github.com/erik-fryscok/erikfryscok.com/issues/42)

## Goal

Reposition erikfryscok.com around hands-on work building and evaluating practical AI systems for software development. The site should show an engineering leader who works directly with AI developer systems, while preserving leadership experience as the context that shapes the work rather than the sole subject of the site.

## Audience

- Engineering peers who want practical, evidence-oriented AI-assisted engineering work.
- Technical leaders assessing how AI developer systems can be introduced with clear reliability and capability boundaries.
- Hiring teams looking for hands-on engineering, evaluation, developer-tooling, and leadership experience.

## Positioning and themes

The site will organize its public narrative around four durable themes:

1. **AI-assisted engineering** — coding agents, developer workflows, and tooling that improve software-development work.
2. **Evaluations and reliability** — explicit evidence, compatibility checks, layered evaluation, and honest limits before promotion.
3. **Local and open-weight experimentation** — bounded experiments with local and open-weight models to learn where they are useful and where they are not.
4. **AI engineering leadership** — practical systems thinking, maintainability, and team outcomes informed by hands-on engineering and leadership experience.

The core identity is a hands-on engineering leader building and evaluating AI developer systems. Public claims must remain grounded in available evidence and must not imply external adoption, benchmark superiority, ML-research credentials, guaranteed privacy or safety, or unverified outcomes.

## Proof architecture

The Home page will lead with concrete work in this order:

1. **Local AI Lab** — the leading example of local-model experimentation, compatibility work, routing, lifecycle management, and evaluation boundaries.
2. **Agent Skills** — the more directly reusable developer-workflow project, demonstrating an evidence-backed agent skill.
3. **Codex writing** — the article *Why I Keep Coming Back to Codex*, which provides a written perspective on practical AI-assisted engineering.

This order signals that the site is about building and assessing AI developer systems, while keeping the strongest reusable workflow evidence distinct from the experimental lab.

## Local AI Lab boundaries and public interface

Local AI Lab will have the public route `/projects/local-ai-lab` and will always be described as an **experimental AI lab**, learning playground, and evaluation testbed for local and open-weight models.

It is not production infrastructure, a production architecture, a team-wide solution, or a replacement for frontier models. The case study may explain that local models can be useful for bounded experiments, small targeted changes, and fixes. It must also state that they fall short for higher-stakes, ambiguous, complex, large-context, or reliability-critical work. Flagship frontier cloud models are the escalation path when a task's risk or complexity exceeds demonstrated local capability.

The case study will describe public, reproducible concepts and interfaces without publishing raw benchmark data, model answers, local paths, machine details, credentials, employer or client information, or non-public designs.

## Content and interaction design

Keep the existing static Astro architecture, portrait-led Home experience, navigation, personal sections, and established project-card behavior. The Local AI Lab and Agent Skills cards use internal case-study links; source links remain external where provided.

The Local AI Lab case study uses the established narrow readable column and semantic heading order. Long command or prompt content must remain horizontally usable on narrow screens. The Home proof grid makes Local AI Lab visually dominant, followed by Agent Skills and Codex writing, without obscuring the lab's experimental label or limitations.

## Acceptance criteria

### Automated

- Build-output tests confirm the Home headline, support copy, proof order, experimental-lab label, and links to Local AI Lab, Agent Skills, and Codex writing.
- Build-output tests confirm `/projects/local-ai-lab` is generated; Local AI Lab appears before Agent Skills and erikfryscok.com on Projects; and required internal and external links resolve to the documented public interfaces.
- Tests verify the case study includes compatibility, structured tool calls, lifecycle, evaluation, bounded-work strengths, production limits, higher-stakes limitations, and frontier-cloud escalation.
- Tests reject language that presents Local AI Lab as a production solution, frontier-model replacement, or suitable for every workload.
- `npm run check`, `npm test`, and `git diff --check` pass for the completed implementation.

### Responsive and manual

- At 375px and 1280px, the Home proof hierarchy remains clear, the portrait remains balanced, and no horizontal overflow obscures content or controls.
- At 375px and 1280px, `/projects`, `/projects/local-ai-lab`, and `/projects/agent-skills` maintain readable heading hierarchy, visible experimental framing, usable links, and accessible focus states.
- Long commands and prompts on the Local AI Lab case study handle horizontal overflow without breaking the page layout.

## Out of scope

- Presenting Local AI Lab as production-ready or as a frontier-model replacement.
- Publishing raw evaluation artifacts, sensitive machine or repository details, or employer/client material.
- Claiming adoption, model parity or superiority, or guaranteed outcomes without public evidence.
- Adding RSS, structured data, social images, licensing decisions, or GitHub and LinkedIn profile changes as part of this repositioning.
