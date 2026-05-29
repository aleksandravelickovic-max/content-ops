# Pipeline contracts and Keyway hand-delivery

How the 15-stage pipeline guarantees that each stage receives an input it can actually work on. Decision source: 2026-05-28 Lucas direction in the wake of the content-team-pipeline-quality discussion.

## The problem

The original pipeline (`/run-piece`) ran stages in order and trusted each agent to either produce a usable artifact or write `BLOCKED.md`. In practice, agents would silently produce *plausible-shaped* output that the next agent would accept and operate on — leading to gate failures for the wrong reason (the downstream agent failing because the upstream agent produced garbage, not because the draft itself was wrong). Concretely:

- `/draft-product-page` would produce a draft missing section 5 (Installation). `material-guard` would then run, find no "approved for pools" claim, and PASS — even though the draft was structurally broken. Errors surfaced 6 stages later in `voice-judge` as a low "specificity" score, masking the real root cause.
- `/brief` would produce a brief without a named voice reference. `/draft-{type}` would proceed and invent a register. The terminology and material rules would all pass mechanically because the prose was on-topic. Jamie would reject the piece editorially. No gate caught the upstream cause.

The fix is **contract-based hand-delivery**: each pipeline boundary (Keyway) has an explicit YAML contract that declares the invariants the receiving stage requires. Between stages, a `keyway-check` agent validates the upstream output against the downstream contract before the next stage is invoked. Mismatch -> halt with a precise diagnostic naming the broken invariant.

## The Keyways

Not every stage-to-stage transition is a Keyway. Inside the enforcer cluster (stages 3-10), each enforcer is independent and shares the same input — the draft. Their handoffs are sequential PASS/FAIL via `state.json`; no contract needed.

The five Keyways live where the **semantics** of the artifact change:

| ID | From | To | Why it matters |
|---|---|---|---|
| **B1** | `/brief` | `/draft-{type}` | Brief defines every premise the drafter cannot invent. A missing key forces fabrication. |
| **B2** | `/draft-{type}` | enforcer cluster (stages 3-10) | Draft must have the structural shape (required sections, contact block, no placeholders) the enforcers assume to function. |
| **B3** | enforcer cluster | judges (stages 13-14) | Every critical enforcer must have PASSED. Spending Sonnet judge budget on a draft with a critical failure is waste. |
| **B4** | judges | `/ship` | Both voice and koray scores at floor (>=80) before the synthesizing QA pass runs. |
| **B5** | `/ship` | `/render-html` | Ship verdict is "Ready to ship" before the canonical delivery artifact is produced. |

Each Keyway has a YAML contract at `content-toolkit/contracts/{Bn}-{from}-to-{to}.yml`. The `keyway-check` agent (`content-toolkit/agents/keyway-check.md`) loads the contract, validates the invariants against the prior stage's output, and returns PASS or BLOCKED.

## Contract shape

```yaml
boundary: B2
from_stage: draft
to_stage: enforcer-cluster
purpose: |
  Plain-language description of why this Keyway exists and what
  category of error it is meant to catch.

required_invariants:
  - id: stable_kebab_case_id_for_diagnostics
    check: |
      A description the agent can verify. Prefer mechanical checks (regex,
      file presence, YAML field presence). Where semantic verification is
      needed (e.g., "draft actually discusses the named material"), mark
      `tier: sonnet` so keyway-check delegates to a Sonnet sub-check.
    severity: critical | warning
    tier: haiku | sonnet
    source: STYLE-SYSTEM section or other authority

operator_override:
  allow_path: clients/{client}/campaigns/{campaign}/runs/{slug}/piece-spec.yml
  override_keys: [list of invariant ids the operator may relax]
```

## How `/run-piece` uses contracts

After each prior-stage completes, before the next stage is invoked:

1. Orchestrator reads `state.json` and the latest stage output.
2. Orchestrator invokes `keyway-check` with three arguments: the boundary id, the path to the prior-stage output, and the path to any operator-supplied `piece-spec.yml`.
3. `keyway-check` reads the contract, runs each invariant (haiku checks inline, sonnet checks via Task() delegation — these can run in parallel across invariants of the same severity), and returns a verdict.
4. PASS: orchestrator marks the Keyway as crossed in `state.json` and invokes the next stage.
5. BLOCKED: orchestrator writes `BLOCKED.md` with the failing invariant ids and stops. The pipeline does not skip ahead.

## Operator override (per-piece spec)

For pieces where an invariant legitimately does not apply (e.g., a colorway page where the audience is hard-coded "Trade-only" and the brief does not need to name an audience), the operator can drop a `piece-spec.yml` next to the run:

```
clients/{client}/campaigns/{campaign}/runs/{slug}/piece-spec.yml
```

```yaml
overrides:
  B1:
    audience_segment_present:
      relax: true
      reason: "Trade-only colorway page; audience fixed at the campaign level."
```

`keyway-check` honors override only for invariants where the contract's `operator_override.override_keys` permits it. Critical safety invariants (e.g., `colorway_verified`, `prop65_link_required`) are never overridable.

## Parallel Sonnet sub-checks

Where an invariant requires semantic reading (e.g., "the brief actually grounds the draft topic in the source documents Aleksandra cited" — not just "brief mentions the source"), `keyway-check` delegates to a Sonnet sub-check via Task(). Multiple sonnet sub-checks within one Keyway run in parallel — they share the same input (prior stage output), do not depend on each other, and their verdicts are aggregated by `keyway-check` before returning.

This is the "multiple Sonnets executando essa tarefa em paralelo" the design calls for. It is reserved for invariants where mechanical pattern matching would produce false positives or negatives.

## Why this raises quality

Today, when Jamie rejects a piece, Aleksandra audits the pipeline and finds that some gate scored 84 instead of catching the real issue. The piece "passed" but was rejected. The Keyway pattern shifts the failure to the right boundary: if a brief is missing its voice reference, B1 halts and names the invariant. If a drafter produces a draft without section 5, B2 halts before any enforcer wastes a turn. If voice-judge scores 78 because the draft never had a chance, B3 was the wrong gate — the real failure was earlier and Keyway diagnostics surface it.

The result: an editorial rejection becomes a question about which Keyway should have caught it, not a re-prompting cycle. That is exactly the "fix the source, not the symptom" principle the IMPROVEMENT-LOOP already names, applied at the architectural boundary instead of after the fact.
