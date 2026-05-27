---
description: Run one content piece end-to-end through the full Zia pipeline with a state file and resumable stages. Halts on any critical gate failure.
argument-hint: <client-slug> <content-type> <material> <topic-or-sku> [--resume]
model: opus
---

Orchestrate a single content piece from brief to scored draft. You are the orchestrator: you call each stage in order, persist state after each, and halt on any critical failure. Follow `CLAUDE.md`.

## Input

`$ARGUMENTS`: `<client-slug> <content-type> <material> <topic-or-sku> [--resume]`
- `content-type`: `collection` | `product` | `blog`
- `--resume`: continue from the last completed stage in the existing state file.

## Setup (before stage 1)

1. **Identify** client, content-type, material, topic.
2. **Confirm context files exist:** `clients/{client}/STYLE-SYSTEM.md`, `clients/{client}/materials/{material}.md`, `clients/{client}/page-templates/{content-type}.md`, `clients/{client}/contact-block.md`. If any is missing, stop and report.
3. **State file:** `clients/{client}/campaigns/{campaign}/runs/{piece-slug}/state.json`. On `--resume`, read it and skip completed stages. Otherwise create it with all stages `pending`.

## Pipeline (run in order, persist state after each)

| # | Stage | Agent / command | Gate behavior |
|---|---|---|---|
| 1 | Brief | `/brief` | advisory |
| 2 | Draft | `/draft-{content-type}` | advisory (drafter self-checks) |
| 3 | Material guard | `material-guard` | **critical**: any violation halts |
| 4 | Terminology lint | `terminology-lint` | **critical**: banned-term hit halts |
| 5 | Claims grounding | `claims-grounding` | **critical**: unverified factual claim or §4.10 trap halts |
| 6 | Person consistency | `person-consistency` | **critical**: second person or switch halts |
| 7 | Contact line | `contact-line-check` | **critical**: missing contact block halts |
| 8 | Humanize | `/humanize` | advisory |
| 9 | Ship QA | `/ship` | **critical**: "Not ready to ship" halts |
| 10 | Voice judge | `voice-judge` | **gate**: score < 80 halts |
| 11 | Koray judge | `koray-judge` | **gate**: score < 80 halts |
| 12 | Render HTML | `/render-html` | mechanical: never halts on its own |

Stages 3-7 are the mechanical enforcers (cheap, run first to fail fast). Stages 10-11 are the scored gates (run last on a clean draft). Stage 12 is deterministic — it converts the gate-cleared MD into the canonical `.html` delivery artifact (decision: 2026-05-27). It runs only after all critical stages pass; a halted piece does not produce an `.html`.

## Halt protocol

On any critical/gate failure:
1. Write the failure into `state.json` (stage, reason, findings).
2. Write `clients/{client}/campaigns/{campaign}/runs/{piece-slug}/BLOCKED.md` with the failing stage, the specific findings, and the suggested fix (for judges: the lowest-scoring dimensions and their fixes).
3. Stop. Do not proceed to later stages. Report the blocker to the user.

## Success output

On all stages passing:
1. Write the final draft to `clients/{client}/campaigns/{campaign}/drafts/{piece-slug}.md`.
2. Run stage 12: `/render-html clients/{client}/campaigns/{campaign}/drafts/{piece-slug}.md`. This produces `{piece-slug}.html` next to the MD. The HTML is the delivery artifact; the MD remains the source of truth for re-runs and gate review.
3. Write `RUN-SUMMARY.md` next to it:
   ```
   # Run summary: {piece-slug}
   - Client / type / material: {...}
   - Stages: all 12 passed
   - Voice score: {n}/100
   - Koray score: {n}/100
   - Verify-with-Alex items: {list from material-guard, or None}
   - Delivery artifact: {piece-slug}.html
   - Model tiers used: opus (orchestrator), sonnet (draft/judges), haiku (enforcers + render)
   ```
4. Report the MD path, the HTML path, and both scores to the user.

## State file shape

```json
{
  "piece_slug": "...",
  "client": "...",
  "content_type": "...",
  "material": "...",
  "topic": "...",
  "stages": [
    {"name": "brief", "status": "completed|pending|failed", "note": "..."},
    ...
  ],
  "updated": "ISO-8601"
}
```

## Constraints

- Run enforcers (3-7) before judges (10-11): fail fast and cheap.
- Never skip material-guard. A material error is a QA-failing factual error.
- Never auto-pass a `verify`-confidence material rule; surface it in RUN-SUMMARY for Alex.
- Persist state after every stage so `--resume` always works.
- Stage 12 (HTML render) only runs after stage 11 passes. A halted piece does not produce an HTML artifact.
- Do not use em dashes anywhere.
