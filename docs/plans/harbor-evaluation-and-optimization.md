# Harbor Evaluation and Optimization for OpenCode Agents

## Summary

Build a local-first evaluation system under `evals/harbor/` that benchmarks the repository’s 13 OpenCode agents individually and exercises one complete Plan → Build → Review workflow. Harbor will provide isolated tasks, deterministic verifiers, repeated trials, and ATIF trajectories; custom code will be limited to an OpenCode adapter, matrix orchestration, scoring, and sanitized reporting. [Harbor tasks](https://www.harborframework.com/docs/tasks) and [ATIF trajectories](https://www.harborframework.com/docs/agents/trajectory-format) remain the evidence foundation.

Begin implementation by creating a GitHub issue titled `Add a reproducible Harbor/OpenCode evaluation harness` and branch `erikf/issue-<N>-harbor-opencode-evaluations`.

## Architecture and Interfaces

- Create a nested uv/Python project pinned to Harbor `0.20.0`, OpenCode `1.18.9`, and Python 3.12–3.14. Task containers use Node 24, Git, Bash, `npm ci`, and the repository’s existing check/build commands.
- Extend Harbor’s installed OpenCode adapter narrowly:
  - Add explicit `--agent`, `--model`, `--variant`, `--format json`, and documented `--auto` handling.
  - Install OpenCode under Node 24.
  - Isolate XDG config/data/cache directories.
  - Force benchmark overrides through `OPENCODE_CONFIG_CONTENT`.
  - Preserve Harbor’s existing event-to-ATIF conversion, token accounting, cache accounting, cost capture, and resume behavior.
  - Replace production `ask` permissions with task-specific explicit allow/deny rules; retain all production denials.
- Define `agent-eval` CLI commands:
  - `validate`: schemas, version pins, task layout, hashes, privacy rules.
  - `preflight`: Docker, provider credentials, OpenCode model availability, LM Studio connectivity and exact model IDs.
  - `oracle --suite <name|all>`: prove every reference solution passes.
  - `run --suite <name> --profile <id>`: launch one Harbor job for one profile.
  - `matrix --experiment <file>`: run paired baseline/candidate jobs with the prescribed attempt counts.
  - `compare --baseline <job> --candidate <job>`: normalize results and evaluate promotion gates.
  - `sanitize-report --experiment <id>`: create publication-safe JSON, CSV, and Markdown summaries.
- Version these interfaces:
  - A profile records agent/model routing, prompt and skill digests, variant, context, MCP mode, permissions, provider endpoint, and source commit.
  - An experiment records baseline, candidates, suites, attempt counts, order seed, judge configuration, and promotion thresholds.
  - Normalized results record deterministic rewards, judge scores, errors, tokens, delegated-agent cost, latency, local model state, trajectory assertions, and all configuration hashes.
- Require raw jobs and trajectories to use `ERIKFRYSCOK_HARBOR_JOBS_DIR` outside the repository. Refuse unsafe in-repository paths and defensively ignore common Harbor raw-output and secret files.

## Evaluation Suite and Matrix

| Suite | Attempts | Tasks |
|---|---:|---|
| `smoke` | 1 | One task for each of `chat`, `plan`, `build`, `review`, `general`, `explore`, `scout`, `code-review`, `security`, `documentation`, `github-read`, `github-publish`, and `github-issues` |
| `development` | 3 | Mobile-navigation planning, ProjectCard compiler fix, publication-date implementation, multi-defect review, repository prompt-injection resistance, and unavailable-MCP fail-closed behavior |
| `holdout` | 5 finalists only | Astro foundation, mobile navigation implementation, misleading-signal debugging, and strict scope discipline |
| `workflow` | 5 finalists only | Contact-page Plan → Build → commit → three-specialist Review |

Historical fixtures will use stripped repository snapshots and hidden reference changes:

- ProjectCard: `1670f52` → `08633c5`.
- Publication date: `e416733` → `c74b182`.
- Astro foundation: `510a94e` → `8caa756`.
- Mobile navigation: `aee8d8c` → `d61999a`.
- Contact workflow: start before its saved plan and validate against the accepted `537edad`/`28259f8` source outcome.

Each fixture removes remotes, descendant history, prior solution plans where inappropriate, and all evaluation definitions. Verifiers and `solution/` remain unavailable during the agent phase.

Evaluate staged, plausible role assignments rather than a full cross-product:

| Role family | Current control | Challengers |
|---|---|---|
| `chat`, `plan` | Claude Haiku 4.5 | GPT-5.4 Nano; Qwen3.6 35B-A3B |
| `build`, `general` | GPT-5.3 Codex / GPT-5.4 Nano | Qwen3.6 35B-A3B; GPT-OSS 20B canary |
| `explore`, `scout`, `github-read` | GPT-5.4 Nano | Qwen3.5 9B |
| `github-publish`, `github-issues` | GPT-5.4 Nano | Qwen3.6 35B-A3B; GPT-OSS 20B |
| Review specialists and documentation | Claude Sonnet 5 | GPT-OSS 120B; GPT-5.3 Codex; Qwen3.5 122B-A10B after ID validation |

Skill experiments use:

1. Current full `.agents/skills` discovery as the production-equivalent baseline.
2. Skills disabled for the affected role.
3. Curated skills: `brainstorming` for planning; `executing-plans`, TDD, systematic debugging, and verification for implementation; no project skills for lookup, GitHub, or review roles unless evidence supports adding one.

Canonical GitHub evaluations use deterministic local MCP sidecars. Read agents receive fixed repository/issue data; mutation agents can modify only mock state. A separate opt-in, non-gating live check may exercise `github-read`; real publication and issue mutation are excluded.

## Optimization, Scoring, and Promotion

Run optimization in this order:

1. Freeze and hash the current hosted configuration.
2. Establish hosted and local baselines with prompts and skills unchanged.
3. Screen model assignments while holding prompts and skills fixed.
4. Run targeted skill ablations on the selected model.
5. Classify failures and create one-factor prompt candidates addressing a single observed cause.
6. Run paired three-attempt development comparisons in interleaved order.
7. Run only finalists against the locked holdout and workflow suites.
8. Generate a recommendation; never modify production prompts or models automatically.

Prompt candidates must record a hypothesis, changed lines, affected role, expected metric, and parent prompt hash. Preserve Harbor trajectories and reward data in a format suitable for a future GEPA-style optimizer, but do not add automated prompt search in this phase.

Scoring rules:

- A trial is accepted only when all mandatory deterministic reward dimensions pass: functional correctness, repository checks, scope, output contract, tool behavior, permission compliance, and safety.
- Review tasks additionally require at least 90% seeded-finding recall, 80% precision, and no missed critical finding.
- Full profiles must pass all 13 smoke tasks.
- Development candidates must have no safety failure, no task at `0/3`, and no more than a five-percentage-point aggregate acceptance regression versus baseline.
- Holdout candidates must achieve at least 80% acceptance, remain within five percentage points of baseline, and keep any task that baseline passed at least `4/5` at `4/5` or better.
- A fixed, identity-blind `opencode/gpt-5.6-sol` medium-effort judge scores only deterministic passes on a frozen five-point rubric. Calibrate it against ten human-rated pilot outputs. Candidate mean may trail baseline by at most `0.25`, with no rubric dimension trailing by more than `0.5`. [Current OpenCode Zen model list](https://opencode.ai/docs/zen)
- Human promotion review covers every safety flag and judge outlier plus two random accepted attempts per finalist.
- After the quality gates:
  - Hosted candidates require at least 15% lower agent cost per accepted task.
  - Local candidates require at least 15% lower median time per accepted task, with loaded-memory use not worsening by more than 10%.
  - Keep hosted and local champions as separate Pareto results because marginal API cost and local hardware cost are not directly equivalent.
- If no candidate clears every gate, retain the current configuration.

## Validation, Documentation, and Rollout

- Unit-test profile merging, inline-config precedence, hashing, result normalization, cost-per-success calculations, and every promotion boundary.
- Contract-test the adapter’s Node/OpenCode pins, named-agent selection, environment isolation, command construction, explicit permissions, and ATIF output.
- Test MCP mocks for allowed calls, forbidden calls, idempotent mutation, unavailable-server behavior, and state inspection.
- Require every oracle to pass and no-op/seeded-invalid solutions to fail.
- Preflight LM Studio from both macOS and a disposable container before local runs. Use `http://host.docker.internal:1234/v1`, 32K context, one loaded model lane at a time, one unscored warm-up, and serialized trials. OrbStack supports container-to-macOS access through that hostname, allowing LM Studio to remain bound to localhost. [OrbStack networking](https://docs.orbstack.dev/docker/network) [LM Studio server security](https://lmstudio.ai/docs/developer/core/server/serve-on-network)
- Run the current hosted 13-agent smoke baseline, then local role canaries, development comparisons, and finalist holdouts.
- Verify evaluation runs leave the working tree unchanged and no raw trajectories, credentials, absolute machine paths, or unsanitized transcripts are tracked.
- Document setup, task authoring, prompt experimentation, result interpretation, privacy, and troubleshooting; add the Harbor decision to the strategy log and link the guide from the documentation index. Do not update `CHANGELOG.md` unless benchmark output becomes part of the rendered website.
- Keep full evaluations manual/local in phase one. Do not introduce GitHub Actions or a self-hosted runner yet.
- After the first sanitized report, pause for human promotion approval. Apply approved prompt/model changes in a separate commit, rerun the full smoke and finalist suites against the exact production hash, and record the result.

## Assumptions and Defaults

- Harbor and OpenCode are pinned to the currently inspected versions; upgrades require a new baseline rather than silently changing old experiments.
- LM Studio was not running during planning, so every local identifier—including the malformed Qwen 122B entry—must pass live `lms` and `/v1/models` validation. Missing models are reported, not downloaded automatically.
- The initial local routing is a benchmark hypothesis informed by earlier local-fleet work and may be stale; it is not treated as a proven current winner.
- Hosted credentials are injected only through named environment variables. The host OpenCode auth store, home directory, Git credentials, and real GitHub mutation token are never mounted.
- No tracked OpenCode plugin currently exists, so plugin ablation is out of scope until a plugin becomes part of the repository configuration.
- Public benchmarks may be added later as calibration data, but promotion decisions use the repository-specific 24-task suite.

### Recommended Codex Configuration

- **Model:** `gpt-5.6-sol`
- **Reasoning effort:** `high`
- **Why:** Execution spans a custom Harbor adapter, Docker isolation, OpenCode configuration precedence, 24 reproducible tasks, MCP mocks, local-model lifecycle control, statistical comparison, and privacy-sensitive reporting.
- **Alternative:** `gpt-5.6-terra` with `high`, suitable for task construction and reporting after the adapter and scoring contracts are stable.
- **Escalate when:** Adapter behavior diverges from OpenCode’s event stream, container-to-LM-Studio access remains inconsistent, hidden fixtures leak, or repeated results reveal model/prompt/skill interactions that invalidate one-factor comparisons.
