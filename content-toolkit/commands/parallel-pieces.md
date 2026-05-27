---
description: Fan-out N pieces through the full pipeline in parallel inside one Claude Code session. The Roto-Rooter scale pattern, packaged for Zia. Each piece runs end-to-end in its own sub-agent; the orchestrator aggregates results.
argument-hint: <client> <type> <material> <count|list> [--from-collection <slug>]
model: opus
---

The speed lever. The Zia team needs to produce hundreds of pages without burning a Max-plan session per piece. This command runs N pieces concurrently in one session by spawning a Task() sub-agent per piece. Same pattern Lucas runs on Roto-Rooter to produce 1000+ pages.

If you find yourself running `/run-piece` in a loop, you should be running `/parallel-pieces` instead.

## Input

`$ARGUMENTS`: `<client> <type> <material> <count|list> [flags]`

| Arg | Examples |
|---|---|
| `client` | `zia-tile` |
| `type` | `product` / `collection` / `blog` |
| `material` | `zellige`, `cotto`, `cotto-allende`, `terrazzo`, etc. |
| `count\|list` | A number (`10`) or an explicit list (`"aegean:4x4,bejmat:2x6,oscura:8x8"`) |
| `--from-collection <slug>` | Derive the SKU list from the named collection's colorways × formats |

If a count is given without `--from-collection` or an explicit list, derive SKUs from the material's colorways × formats in STYLE-SYSTEM.md / raw/ — same logic as `/sku-multiplier`. Never invent SKUs.

## Client context protocol (mandatory before fan-out)

Load once, share with every sub-agent in their prompt:
1. `clients/{client}/STYLE-SYSTEM.md`
2. `clients/{client}/materials/{material}.md`
3. `clients/{client}/raw/research/materials-reference.md` (the Quick Reference matrix)
4. `clients/{client}/page-templates/{type}.md`
5. `clients/{client}/contact-block.md`
6. `clients/{client}/COMPLIANCE.yml`
7. The proven reference draft for `{client}/{type}` (e.g. for Zia product: `campaigns/01-product-collection-pages/drafts/product-pages/aegean-4x4.md`)

The orchestrator reads these once; the sub-agents each re-read what they need (per CLAUDE.md hard gate 2). This is fine — the cost is bounded by the Max plan, not by the read pattern.

## Fan-out (the key mechanism)

**Resolve the SKU list, then in a single response emit N `Task` tool calls — one per piece, all in the same response.** The Claude Code harness runs them concurrently. Each sub-agent is independent: own context, own output, returns once.

For each piece, the sub-agent prompt must be self-contained:

```
You are producing one {type} page for {client} / {material} / {sku-or-topic}.

Required reads (do these first, in order):
1. clients/{client}/STYLE-SYSTEM.md
2. clients/{client}/materials/{material}.md
3. clients/{client}/raw/research/materials-reference.md (Quick Reference matrix only)
4. clients/{client}/page-templates/{type}.md
5. clients/{client}/contact-block.md
6. The reference draft: {reference-draft-path}

Then produce the {type} page following the template, applying material-guard +
terminology-lint + contact-line-check + person-consistency + claims-grounding
inline as self-checks (do not skip any of them).

Write the draft to: clients/{client}/campaigns/{campaign-slug}/drafts/{type}-pages/{piece-slug}.md

Return a single JSON block:
{
  "piece_slug": "...",
  "file_path": "...",
  "gates": {
    "material_guard": "PASS|FAIL",
    "terminology_lint": "PASS|FAIL",
    "contact_line": "PASS|FAIL",
    "person_consistency": "PASS|FAIL",
    "claims_grounding": "PASS|FAIL"
  },
  "verify_with_alex": [...],
  "blockers": [...]
}

Do not produce content if any critical gate fails. Report the blocker instead.
```

Use `subagent_type: general-purpose` for each Task. The mechanical gates run inline inside each sub-agent; voice-judge and koray-judge run as a follow-up batch by the orchestrator (see below).

## Aggregation (after all sub-agents return)

The orchestrator collects the N returned JSON blocks and builds:

```
## Parallel run: {N} {type} pieces for {client}/{material}

### Per-piece matrix
| Piece | File | mat-guard | terminology | contact | person | claims | Notes |
|---|---|---|---|---|---|---|---|
| {slug} | {path} | PASS | PASS | PASS | PASS | PASS | clean |
| {slug} | {path} | FAIL | PASS | PASS | PASS | PASS | pool/spa misapplied — fix and re-run this piece |
| ...

### Aggregate
- Clean: {n} pieces
- Blocked (need fix): {n}
- Verify-with-Alex items shared across the batch: {list}

### Next
- Run `voice-judge` and `koray-judge` on the {n} clean pieces (optional second batch; spawn a Task per piece).
- Fix the {n} blocked pieces using the improvement-loop pattern (content-toolkit/IMPROVEMENT-LOOP.md) and re-run JUST those pieces.
```

## Optional second batch (scored judges)

Voice + Koray are slower and scored. After the mechanical-gate batch passes, spawn a SECOND parallel batch: one Task per clean piece that runs voice-judge + koray-judge on it and returns the two scores. Aggregate into the matrix.

This is the "fail-fast cheap, then score" pattern from PIPELINE.md applied at scale.

## When to use what

| Situation | Use |
|---|---|
| Producing 1 piece, careful | `/run-piece` |
| Promoting 1 existing v3 | `/promote-v3` |
| Multiplying SKUs off an approved collection | `/sku-multiplier` (now uses parallel fan-out internally) |
| **Net-new batch of N pieces of the same type** | `/parallel-pieces` ← this command |
| Pure QA across an existing backlog | `/batch-review` |

## Practical guidance for Max plan rate limits

If a batch is large enough to risk hitting the per-session token budget on a single Max plan:
- Rotate plans (run alternating sessions on two plans, as Lucas does for RR).
- Split the batch by material — material-guard reads are amortized within a material.
- Prefer one wide parallel run (fan-out) over many sequential calls. The harness amortizes the orchestrator overhead across the fan-out.

## Constraints

- One single response emits all N Task calls. Do not stage them across messages — that defeats the parallelism.
- Each sub-agent is independent; it must not assume context from siblings.
- Material-guard is non-skippable inside each sub-agent. A bad freeze/thaw or pool rule is a factual error.
- Aggregate first, only score (voice/koray) on clean pieces.
- No invention. Any unconfirmed fact = `verify_with_alex` entry, not a fabricated answer.
- Do not use em dashes.
