# Local Models, Real Software

Status: active strategy
Related work: [GitHub issue #8](https://github.com/erik-fryscok/erikfryscok.com/issues/8)

## Promise

> Build a real product on one MacBook with open-weight models, no API bill, and
> results measured by what actually passes review.

The recurring episode test is:

> **Can Local AI Ship It?**

The series is about software outcomes, not leaderboard scores or the novelty of
running a large model. It tests how model size, speed, agent compatibility,
privacy, memory use, and human intervention affect accepted work on a real
public product.

## Audience

- Developers who want useful local AI without a recurring inference budget.
- Apple Silicon owners deciding which model sizes are practical.
- Engineering leaders evaluating privacy, reliability, and human-review needs.
- Viewers interested in reproducible coding-agent comparisons rather than
  edited demonstrations of only successful moments.

## Hardware Disclosure

Experiments run on:

- 16-inch MacBook Pro;
- Apple M5 Max;
- 18-core CPU;
- 40-core GPU;
- 128 GB unified memory;
- 4 TB SSD.

Marginal API spend is reported as `$0`. That does not mean the work is free:
the hardware has an acquisition cost, downloads consume storage and bandwidth,
and inference uses electricity. Those costs are disclosed separately when they
can be measured credibly.

## Experimental Contract

When comparing models, hold these constant:

- coding agent and version;
- prompt and fresh conversation;
- Git baseline and isolated branch or worktree;
- runtime and runtime version;
- quantization class;
- context limit;
- issue acceptance criteria;
- validation commands.

Each implementation is evaluated in this order:

1. Automated acceptance criteria and repository tests.
2. First-attempt completion and required human repair.
3. Blind human review against the issue contract.
4. Wall-clock time, tool calls, tokens, throughput, peak memory, and optional
   energy use.
5. Local cross-model judging as secondary evidence only.

A faster failing result never outranks a slower passing result. Role winners
are chosen by accepted-task count, then fewer human interventions, then shorter
elapsed time and lower peak memory.

## Scoreboard

Every published experiment records:

| Field | What is reported |
| --- | --- |
| Model | Exact model ID, release verification date, and parameter class |
| Runtime | llama.cpp version, quantization, context, and agent |
| Task | Public prompt, issue contract, and Git base |
| Attempts | First attempt, retries, and human interventions |
| Validation | Commands, automated outcomes, and blind-review disposition |
| Performance | Elapsed time, tool calls, tokens, throughput, and peak memory |
| Cost | `$0` marginal API spend plus hardware/electricity context |
| Outcome | Accepted, repairable, or failed |
| Limitations | Runtime, modality, prompt-template, and agent-scaffold caveats |

The public scoreboard is a publication format, not a duplicate live roadmap.
Issue #8 and the GitHub Project track delivery status.

## First Case Study

The first episode uses the two implementations of
[website issue #2](https://github.com/erik-fryscok/erikfryscok.com/issues/2):

- gpt-oss-120b completed in 4 minutes 32 seconds;
- gpt-oss-20b completed in 2 minutes 56 seconds;
- the 120B run took approximately 55% longer;
- only the 120B implementation met the usability and acceptance bar;
- the 20B result introduced dependency claims that did not produce an
  installable implementation.

This is the foundational lesson: model size and speed matter only after the
result satisfies the contract.

## Episode Format

Each episode follows the same shape:

1. State the task, acceptance contract, and why the selected models are
   comparable.
2. Disclose model, quantization, context, runtime, agent, and hardware.
3. Show the prompt and unedited outcome-relevant agent behavior.
4. Run the same validation and review process.
5. Compare interventions, elapsed time, memory, and accepted outcome.
6. Publish the result, limitations, and next model-selection decision.

Planned comparison themes:

1. Why the 55%-slower model won.
2. Building the local model garage.
3. 9B versus 27B versus 35B-A3B.
4. Qwen versus Devstral.
5. The 120B local frontier.
6. Can local vision help build a website?
7. Can local models reliably review each other?

Future episodes are hypotheses, not publication commitments.

## Public and Private Boundaries

The private local-model lab owns raw benchmark state, machine paths, service
configuration, model files, runtime logs, and unsanitized agent transcripts.

This public repository may contain:

- sanitized benchmark summaries;
- prompts intentionally prepared for publication;
- accepted diffs from this public repository;
- validation evidence;
- generalized lessons and disclosed limitations.

Do not publish credentials, private filesystem paths, machine identifiers,
private-repository content, employer or client information, proprietary source,
or non-public designs. Every benchmark artifact must pass the lab's public
export sanitizer and a human privacy review before it is copied here.

## Publishing Surfaces

- Website: durable write-up, methodology, scoreboard, accepted diff, and links.
- YouTube: narrated experiment, agent behavior, validation, and conclusion.
- GitHub issue: active scope, discussion, dependencies, and delivery status.
- Private lab: reproducible raw evidence and fleet admission history.

No product-brief or changelog update is required until series material becomes
visible in the rendered site.
