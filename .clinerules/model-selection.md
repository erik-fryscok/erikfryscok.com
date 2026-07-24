# Local model selection

Cline cannot switch its own model mid-task. The model is selected in Cline's
provider settings, while the resident llama.cpp model is controlled by the
private `local-ai-lab`. Recommend a role alias before substantial work, then
continue with the active model. Do not block on the recommendation.

## Baseline

Use the OpenAI-compatible localhost endpoint:

```text
http://127.0.0.1:8080/v1
```

Use only aliases that the private lab currently marks `core`. Local open-weight
inference is the baseline and requires no paid API. Never add credentials,
private lab paths, raw benchmark output, or machine-specific configuration to
this public repository.

## Role routing

Choose by task demands:

| Task profile | Local role alias |
| --- | --- |
| Summaries, documentation, repository exploration, and bounded mechanical edits | `fast` |
| Normal feature implementation, bug fixes, tests, and moderate refactors | `coder` |
| Ambiguous planning, difficult debugging, architecture, and multi-step reasoning | `reason` |
| Skeptical correctness, security, and final implementation review | `review` |
| Screenshot and UI analysis | `vision`, only after its multimodal runtime gate passes |

The role resolves to a validated model in the private lab. Do not pin this
public rule to a model family or parameter count; role winners can change as
experiments produce better evidence.

## Escalation

Escalate because of measured failure, not provider price or parameter count:

- an acceptance criterion is missed;
- a tool call is malformed or not executed;
- the model repeats a failed approach;
- required context exceeds the active profile;
- automated validation fails and the model cannot repair it;
- a blind review finds a material correctness or security issue.

Start a fresh conversation and clean worktree when comparing another role.
Return to a smaller role for bounded cleanup or documentation after the hard
part is resolved.

## Evidence

For series experiments, keep the prompt, Git base, agent, runtime, context,
quantization, validation commands, elapsed time, interventions, and outcome
constant or explicitly recorded. A faster failing result never outranks a
slower passing result.

Raw benchmark state stays in the private lab. Only sanitized summaries,
release-intended prompts, accepted diffs, validation evidence, and generalized
lessons belong here.
