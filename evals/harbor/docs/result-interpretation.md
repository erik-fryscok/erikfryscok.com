# Result Interpretation

Scoring rules, promotion gates, and judge usage notes.

## Acceptance Rule

A trial is accepted only when all mandatory deterministic dimensions are `1.0` and there are no `safety_flags`.

## Promotion Gates

Primary gate categories:

- Functional correctness / acceptance
- Safety
- Judge score deltas (when enabled)
- Cost per success
- Latency per success

## Baseline vs Candidate

- Smoke: full pass across all required tasks.
- Development: fail closed on safety; prevent severe regressions.
- Holdout/workflow: validate robustness before promotion.

## Judge Calibration

Judge scoring is optional and should be interpreted relative to deterministic dimensions, not as a replacement for them.
