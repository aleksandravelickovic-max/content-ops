# Meeting walkthrough — 2026-05-28: how the scaled pipeline works

Audience: Aleksandra, Emanuel, possibly Henry. Goal: unblock the team from per-piece Claude Code sessions hitting Max-plan rate limits, and show how the agentic pipeline matches the RR scale pattern.

This is Lucas's script + handout. Run it in ~30 minutes.

## The reframe in one sentence

> "You don't need a separate Roto-Rooter-style app. The same pattern that produces 1000+ RR pages runs natively inside Claude Code: one session, one parallel command, N pieces fan out as sub-agents at the same time. The repo already has it."

## What changed since last week (lead with this)

Aleksandra's concern was real: running `/run-piece` per piece serially burns sessions. Three things fixed since:

1. **`/parallel-pieces`** — new orchestrator that fans out N pieces in parallel inside one session. Same RR pattern, packaged.
2. **`/sku-multiplier`** — removed the "max 5 per batch" cap I had put in cautiously. No cap now.
3. **Material configs reconciled** with Emanuel's `materials-reference.md` v3 — 10 commits, multiple rule flips, `material-guard` now blocks four categories of errors that earlier configs would have let through.

Hand them a one-page version of `IMPROVEMENT-LOOP.md` if needed.

## Demo sequence (~20 min)

### Demo 1: the parallel pattern (5 min) — THE main point

Open Claude Code in `content-ops/` and run:

```
/parallel-pieces zia-tile product cotto "red-clay-8x8,adobe-4x4,fired-earth-13x13"
```

Talk while it runs:
- "Three SKUs, three parallel sub-agents, one session."
- "Each sub-agent reads STYLE-SYSTEM + materials/cotto.md + the reference draft + the aegean-4x4 pattern, then drafts, then runs material-guard + terminology-lint + contact-line-check + person-consistency inline."
- "When all three return, the orchestrator gives you the matrix."

If it works clean: show the matrix. Pull up one of the produced files in the portal.

If a piece fails a gate: even better — that's the cue to demo improvement-loop.

### Demo 2: improvement loop (5 min)

Take whichever piece failed (or inject a failure if all passed). Show:
- "Failed gate says exactly what's wrong. Material-guard says 'this draft asserts pool/spa approved on a Cotto page; config says NOT_SUITABLE.'"
- "I don't re-prompt. I look at where the wrong claim came from. If it's the draft, fix the draft. If it's the prompt that keeps producing this kind of mistake, fix the prompt and commit. If it's the config disagreeing with the reference doc, fix the config."
- "Then I re-run JUST that piece — `/parallel-pieces zia-tile product cotto "red-clay-8x8"`. Don't re-run the whole batch."

Reference `IMPROVEMENT-LOOP.md` for them to read after.

### Demo 3: speed math (5 min) — the why

- Serial `/run-piece`: ~12-15 min per piece end-to-end, 1 session token budget per piece. 100 pieces = 100 sessions = days of wall time + hit rate limits constantly.
- Parallel `/parallel-pieces`: 100 pieces in one fan-out, ~25-35 min wall time, 1 session token budget for the orchestrator + N parallel sub-agents (each cheap). Same plan, same day.
- The session is the bottleneck, not the work. Parallelism is the fix.

Lucas runs 2 Max plans alternating. For sustained throughput beyond what one plan handles, do the same.

### Demo 4: backlog visibility (3-5 min) — bonus if time

```
/batch-review clients/zia-tile/campaigns/01-product-collection-pages/drafts/
```

"This is the read-only scan across the whole backlog. Tells you exactly which pieces still need work and what's the most common gate failure across the batch — that's the input to the next improvement-loop pass."

## Talking points for likely objections

### "We've been using Claude Code and hit rate limits constantly"

Right — because you were running serial `/run-piece` or freestyle prompts. The fan-out runs all sub-agents inside one session; the parent session pays the token budget once, not N times. The Max plan handles a fan-out of 20-50 pieces routinely.

### "Can we just use OpenRouter for the bulk runs?"

Manick said no — agentic-only inside Claude Code. The parallel pattern is the answer to the speed problem WITHOUT going back to OpenRouter.

### "Will the parallel sub-agents produce drafts as good as Emanuel's hand-tuned ones?"

The pipeline ports Emanuel's aegean-4x4 SKU pattern as the reference draft, and runs material-guard + voice-judge + koray-judge as gates. A piece that passes all gates is in the same quality range as Emanuel's manual drafts. Pieces that don't pass get fixed in the improvement loop. After a couple of cycles the gates catch the recurring issues and quality stabilizes.

### "Roman Mosaics / Cotto Allende / etc. — how do we know the rules are right?"

`materials/{material}.md` carries the rules with their source. Today's reconciliation cross-references `raw/research/materials-reference.md` (Emanuel's v3 guide). When the reference disagrees with the config, the reference wins — there's an explicit commit pattern for the flip. Aleksandra/Emanuel can audit every rule by reading the config file.

### "What about Henry's expectation of a full RR-style app?"

We can show him the parallel demo — that IS the equivalent of the RR app's automation, just running inside Claude Code. The reporting / status UI that the RR app had — that can come back as a separate output layer (the portal already serves that; we can extend it). The generation engine is in the repo.

## Post-meeting Slack template (paste this)

```
Quick recap of today's session:

1. /parallel-pieces is the speed lever — N pieces in parallel sub-agents,
   one Claude Code session. Use this instead of running /run-piece in a loop.

2. Material configs were reconciled today against Emanuel's Materials
   Reference Guide v3. Several rule flips (terrazzo/limestone/ceramics/
   cantera/marble: no pools, no freeze/thaw; roman-mosaics: yes pools).
   material-guard now enforces these mechanically.

3. Read content-toolkit/IMPROVEMENT-LOOP.md before the next batch — it's
   how we keep the system getting smarter instead of re-discovering the
   same mistakes.

4. For sustained throughput beyond what one Max plan handles, we'll
   rotate two plans the same way Lucas does for Roto-Rooter.

Try a small parallel batch (5-10 pieces) when you get back to it and
post the matrix output here. I'll watch for failure patterns to feed
into the prompts.
```

## If Manick joins (CEO-mode framing)

- Lead with: "The agentic pipeline is operational and matches RR throughput. No UI, no OpenRouter calls outside Claude Code, all gated by quality + compliance checks."
- Show only Demo 1 + the speed math.
- Skip the improvement-loop internals.
- Numbers to mention: 15 agents, 14 commands, 13 material configs, 36 commits live on Forge, one verified pipeline-produced Cotto Allende page (voice 86 / koray 84). After today's session: +10 reconciliation commits + parallel command + improvement loop doc.
- Anchor outcome: "Zia content team unblocked from rate limits; same pattern ports to the other 13 LinkGraph clients."

## What to have open in tabs

- Claude Code session in `content-ops/`
- The portal at http://127.0.0.1:8000/admin/campaigns/zia-tile/01-product-collection-pages
- `content-toolkit/PIPELINE.md` (runbook)
- `content-toolkit/IMPROVEMENT-LOOP.md` (today's new doc)
- `clients/zia-tile/raw/research/materials-reference.md` (Emanuel's reference)
- `clients/zia-tile/campaigns/01-product-collection-pages/drafts/product-pages/aegean-4x4.md` (the proven SKU pattern)

## Risk to flag in the meeting

If Aleksandra has been burning Claude Code sessions running serial /run-piece, her usage will look heavy in the dashboard. Manick or Henry may notice. The pivot to parallel-pieces fixes this — usage per piece drops to a fraction of serial. Frame it as a fix landing today, not a problem.
