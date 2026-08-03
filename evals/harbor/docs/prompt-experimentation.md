# Prompt Experimentation

Candidate creation, hypothesis tracking, and parent-hash discipline.

## Candidate Profiles

Create candidate profile files in `profiles/candidates/` and experiment definitions in `experiments/`.

Each candidate must document:

- Hypothesis
- Exact prompt delta
- Parent profile/hash
- Expected tradeoff (quality, latency, cost)

## Prompt Variant Metadata

For each prompt variant in `experiments/prompt-candidates.yaml`, record:

- `parent_hash`
- changed lines/sections
- rationale and expected outcome

## Evaluation Flow

1. Run baseline and candidate on the same suite/attempt matrix.
2. Compare with `agent-eval compare`.
3. Generate sanitized output with `agent-eval sanitize-report`.
4. Promote only when gates pass.
