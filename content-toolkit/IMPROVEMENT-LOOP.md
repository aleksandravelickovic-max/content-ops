# Improvement loop — how the agents get better at producing content

This is the agentic-ops feedback pattern. The pipeline produces content; some pieces fail a gate or get editorial pushback; you fix the underlying agent prompt or material config so the next batch is better. The system is the codebase, not any single piece. Same pattern Lucas runs on Roto-Rooter.

## The core loop

```
batch run -> some pieces fail -> diagnose where (prompt, config, or fact) ->
  fix the source -> re-run only the failed pieces -> commit the fix
```

The most important rule: **the system memory is git, not the model.** When you find a recurring mistake, you fix it in the repo, not by re-prompting harder. Otherwise you re-discover the same issue every batch.

## When a piece fails a gate — decision tree

### 1. Material-guard FAIL

```
Pool/spa rule wrong, freeze/thaw wrong, sealing combined incorrectly, etc.
```

Check the order:

| Source | What it carries | Authoritative? |
|---|---|---|
| `materials/{material}.md` frontmatter | Hard rules (freeze/thaw, pool, sealing, variation) | Yes — first source |
| `raw/research/materials-reference.md` Quick Reference | Live-site Tile Usage matrix | Yes — second source, wins on disagreement |
| STYLE-SYSTEM.md §4.1 / §11 / §12 | Style-system rules | Yes |
| The page itself | The draft's claim | NO — under review |

**If the draft contradicts the config**: the draft is wrong. Fix the draft (or fix the prompt that produced it). Do NOT loosen the config to make the draft pass.

**If the config contradicts the reference doc**: the CONFIG is wrong. Open `materials/{material}.md` and reconcile against the reference doc. The 2026-05-25 reconciliation (commits 2c57dce..8364396) is the model: one commit per material, source-cited.

**If the reference doc is silent**: leave the rule `verify` and surface for Alex. Never invent.

### 2. Terminology-lint FAIL

```
Banned term hit, required term wrong, second person in body.
```

If the term is **clearly banned by STYLE-SYSTEM** (§3.2): fix the draft. The lint is right.

If the term is a **judgment call** (e.g., "perfectly imperfect" being flagged for non-zellige): tighten the lint's logic so it only flags the right context. Update `agents/terminology-lint.md` with the contextual rule.

If **Jamie has recently revised** a term decision (e.g., new banned phrase, or lifted a ban): update STYLE-SYSTEM.md §3.1/§3.2 first, then re-run.

### 3. Person-consistency FAIL

```
Second person in body, or first/third switch within a piece.
```

Almost always a draft issue, not a config issue. Fix the draft.

Exception: if a piece's intended voice changed (e.g., a new content type that legitimately uses second person), update `page-templates/{type}.md` to declare the allowed person, and update the agent prompt to check against it.

### 4. Voice-judge < 80

```
Reads too marketer-y, too generic, weak lead, weak closer.
```

Read the dimension breakdown. If one dimension keeps tanking across many pieces (e.g., "Lead and closer quality" averaging 10/15 across a batch):
- Update the **drafter prompt** (`commands/draft-product-page.md` or `draft-collection-page.md`) to emphasize the weak dimension.
- Optionally add concrete examples from already-approved pieces in the same material to the prompt.
- Commit, then re-run.

If only one piece tanks: fix that piece's lead/closer manually. Don't change the prompt for one outlier.

### 5. Koray-judge < 80

```
SEO structure, entity coverage, schema readiness, internal-link logic, etc.
```

Same dimension-by-dimension review. Most common pattern: weak internal-link depth. Fix: update the drafter prompt to always link the relevant Installation Guide + the sibling product where appropriate.

### 6. Claims-grounding FAIL

```
A claim has no source in raw/.
```

Two paths:
- The claim is true but missing from knowledge → ADD a `raw/knowledge/facts/{slug}.md` or update an existing one with the source. Re-run.
- The claim is unverifiable → REMOVE from the draft. Don't invent.

Never solve a claims-grounding fail by hand-editing the draft to dodge the question. The next piece will hit the same gap.

## When a piece is editorially rejected (Aleksandra / Emanuel / Jamie)

A piece can pass every gate and still be rejected by humans for taste, register, or a nuance the gates don't catch yet.

**Treat every editorial rejection as input to the prompt or the config.** Ask:
- Is this a rule the gates SHOULD catch? → Add or sharpen a gate (new banned phrase, new material-guard rule, new compliance flag).
- Is this a voice nuance? → Update `voice-judge.md` with the new register example, or add the corrected wording to the relevant page-template / STYLE-SYSTEM section.
- Is this a one-off taste call? → Fix the piece, don't update the system.

Distinguish "the system missed a real rule" from "the editor expressed a preference." The first goes into the repo; the second goes in the piece.

## Versioning conventions

- **Agent prompts and commands** live in `content-toolkit/`. Edit in place. Git history is the version. Commit messages should name the dimension being improved (e.g., `feat(agents): voice-judge — penalize CTA-style closers more harshly`).
- **Material configs** live in `clients/{client}/materials/`. Edit in place. Each commit names the rule flip + the source (e.g., `fix(zia): cantera freeze/thaw not_suitable — per Materials Reference Guide v3`).
- **STYLE-SYSTEM.md, COMPLIANCE.yml, contact-block.md** — edit in place, commit with the editorial source (whose call, what session).

Do not fork prompts into v2/v3 folders unless you actually need to run two versions side-by-side. Git history is the audit trail.

## Re-running only the failed pieces

When you fix a config or a prompt and need to re-run, target ONLY the pieces that failed. Do not re-run the whole batch:

```
/parallel-pieces zia-tile product cotto "red-clay-8x8,oscura-2x6"  # the two that failed
```

The parallel orchestrator accepts an explicit piece list. Use it. This saves session budget and review effort.

## Anti-patterns

- **Re-prompting until the gate passes.** If a gate keeps failing on similar pieces, the prompt or config has the bug. Fix the source.
- **Loosening a gate to make a draft pass.** A wrong pool/spa rule is a factual error; loosening material-guard so a wrong draft slips through means the next draft will publish the same error. Fix the draft.
- **Editing one piece per session indefinitely.** That's not the pipeline; that's manual writing with extra steps. If the system isn't producing at scale, find the bottleneck (prompt, config, or knowledge gap) and fix that.
- **Treating Aleksandra's edit as a one-off.** When she rewrites the same kind of sentence twice, that's a rule. Encode it.

## Cadence (suggested)

- **After every batch:** spend 10-15 minutes on the matrix. Find the most common failure dimension. Fix it in the source. Commit.
- **Weekly:** re-read STYLE-SYSTEM.md against the past week's edits. Anything Jamie corrected that isn't in STYLE-SYSTEM yet is a rule that's about to be missed.
- **At the start of every new material:** read `materials-reference.md` for that material end-to-end before producing the first batch. The Quick Reference matrix is the cheapest place to find the next big rule flip.

## Reference

- The 2026-05-25 reconciliation commits are the canonical example of fixing the source instead of the symptom: 10 atomic commits, one per material, each citing the authoritative reference. See `git log --oneline 2c57dce..8364396`.
- `content-toolkit/PIPELINE.md` for the standard pipeline ordering.
- `commands/parallel-pieces.md` for the fan-out pattern.
