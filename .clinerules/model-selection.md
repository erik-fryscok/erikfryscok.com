# Model selection for planning tasks

Cline cannot switch its own model mid-task — the model is chosen in the UI's model selector and provider settings. When a task enters planning, proactively **recommend** the best model/provider up front, then continue planning with whatever model is active. Do not block on the recommendation.

## Core constraint: direct creator APIs, pay-per-use only

This project tracks cost per call. Recommend only models reached via the **creator's own direct API** — configured in Cline's provider settings with that creator's API key and base URL. Do **not** recommend:

- **Subscription / plan-based access** — e.g. Cline Pass, Cline usage-based billing, or any aggregator that bundles many models behind one subscription. These do not expose clean per-call cost.
- **Third-party hosters of open-weight models** — e.g. Together, Groq, Cerebras, Fireworks, Replicate. The hoster is not the model's creator, which breaks the "direct to creator" rule and the per-call cost trail.

Open-weight models are allowed **only when their creator also offers a direct pay-per-use API** to them (e.g. DeepSeek, GLM).

## Provider catalog — by family and tier, not by version

The model landscape changes fast. Always recommend the **latest available** model in the chosen family and tier, and confirm the current model ID against the provider's docs when there is any doubt. Never pin a specific version as if it were permanent.

| Creator | Direct API (base URL) | Model family | Planning strengths |
| --- | --- | --- | --- |
| Anthropic | `api.anthropic.com` | Claude (flagship → standard → fast tiers) | Deep reasoning, agentic coding, long context, careful planning |
| OpenAI | `api.openai.com` (platform.openai.com) | GPT + o-series (the family behind ChatGPT) | Broad reasoning, tool use, structured planning |
| Google | Gemini API (`generativelanguage.googleapis.com`) / Google AI Studio | Gemini (flagship/Pro → Flash) | Very long context, multimodal, fast Flash tier |
| Zhipu / z.ai | z.ai (`open.bigmodel.cn`) | GLM | Cost-effective strong reasoning |
| DeepSeek | `api.deepseek.com` | DeepSeek (incl. reasoning models) | Very cost-effective reasoning and code |
| Mistral | `api.mistral.ai` | Mistral / Codestal | Cost-effective, strong on code |

A provider may be added to this catalog only if it meets the same gate: it **created** the model **and** offers a **direct pay-per-use API**. Re-evaluate the catalog whenever a creator's lineup changes.

## Task-based routing — pick tier/provider by reasoning load

Match the model to the task's **reasoning load**, not its file count.

| Task profile | Suggested tier (latest model in tier) | Provider families to draw from |
| --- | --- | --- |
| Architecture, multi-system design, security, migrations, ambiguous/under-specified requirements | **Flagship / reasoning** — strongest available, with high or extended thinking | Anthropic Claude (flagship), OpenAI GPT/o-series (flagship), Google Gemini (flagship/Pro), DeepSeek (reasoning), GLM (reasoning) |
| Single feature, moderate investigation, scope mostly clear | **Standard / mid** | Anthropic Claude (standard), Google Gemini (Pro), OpenAI (standard), GLM |
| Refining an already-validated plan, or a small well-scoped change | **Fast / value**, or skip heavy planning and use Act mode | Anthropic Claude (fast), Google Gemini (Flash), Mistral, DeepSeek |

## Planning-specific settings — recommend once, not every task

- Enable **"Use different models for Plan and Act"** in Cline Settings: a flagship/reasoning model for Plan, a fast/value model for Act.
- For large, multi-file, or architecturally significant tasks, recommend the **`/deep-planning`** slash command.
- Raise the thinking level (**high** / **xhigh**) for architectural decisions, security analysis, and multi-step planning.

## How to phrase the recommendation

- Make it **up front**, before planning starts.
- Name the **provider family + tier**, then the **specific latest model ID** in that tier; note the version may change and recommend verifying the current ID.
- State the **direct API route** to configure (creator + base URL) and that it is pay-per-use.
- When relevant, note the **cost trade-off** versus alternatives (reasoning/flagship models cost more; value tiers save on routine work).

## Don't

- Don't recommend subscription, usage-billing-wrapper, or third-party-hosted open-weight routes.
- Don't pin specific model versions as if they were permanent.
- Don't suggest a model after planning has begun — recommend before, then proceed.
- Don't try to switch models yourself; the user controls the model selector.
