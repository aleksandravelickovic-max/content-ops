# Stream C — audit-report.md Gaps on the 16 Templates

Apply [audit-report.md](../01-product-collection-pages/audit-report.md) findings to the 16 category templates in [drafts/](../01-product-collection-pages/drafts/). **The May 12 patch (commit `2ee3699`) did not touch any of the 16 templates** — it only patched 35 files in `gdocs-content/` (24 collection pages, 11 product pages). The systemic template-level findings flagged in audit-report.md are all still open.

This is the largest body of work in Campaign 02.

---

## The six top-line findings (apply to all 16 templates unless noted)

These are the Critical and Major findings from audit-report.md §"TOP-LINE FINDINGS" — apply across all 16 templates as one batch each.

### 🔴 Critical (will fail QA)

| # | Finding | audit-report.md ref | Status |
|---|---|---|---|
| C1 | Restructure to the 9 required sections in order — currently collapsed into 6. Pull Installation content out of About. | §6.1 | Outstanding |
| C2 | Add 25% overage option alongside 15–20% on every template | §3.1 + §5 | Outstanding |
| C3 | Add inline sealing guidance per use case (shower/pool/spa) — not only the catch-all "Sealing Required" row | §4.2 | Outstanding |
| C4 | Apply the §4.2 dry-spaces sealing wording verbatim to all 14 docs that currently omit or replace it; remove product names (511 Porous Plus, Fila Matte Wax) | §4.2 | Outstanding |
| C5 | Add slip-resistance spec (⅛" minimum grout joint + anti-slip product) to wet-floor bullets on all 16 | §4.3 | Outstanding |
| C6 | Add affirmative freeze/thaw prose to all 16 templates (chart marks alone don't satisfy §4.1) | §4.1 | Outstanding |

### 🟠 Major (style guide violations)

| # | Finding | audit-report.md ref | Status |
|---|---|---|---|
| M7 | Fix broken heading hierarchy — "Commercial Usage" as H4 under "Residential Usage" H3 in 8 of 16 docs; make both H3 uniformly | §heading | Outstanding |
| M8 | Replace paraphrased shipping copy with verbatim §8.2 wording ("We will ship the entire order together once all tiles are in stock"; "third party" not "third-party"; "8am–3pm") | §8.2 | Outstanding |
| M9 | Strip "Reference for usage: [URL]" internal writer notes from 15 of 16 Tile Usage sections | — | Outstanding |
| M10 | Tighten FAQ placeholder from "4–7 questions" to "minimum 6 covering: thickness variation, shower floor installation, crazing, cleaning, characteristic features, color mixing across collection" | §6.1 | Outstanding |
| M11 | Reword "Free full order pickup" to remove "free" (banned-term neighborhood with "free shipping") | §3.2 | Outstanding |

### 🟡 Minor (quality tightening)

| # | Finding | audit-report.md ref | Status |
|---|---|---|---|
| m12 | Replace "wholly unique" intensifier with the actual variation (color, tone, veining, surface texture) per template | §2.1 | Outstanding |
| m13 | Make "chips, pits, and crazing" the full trio everywhere it appears | §3.1 | Outstanding |
| m14 | Replace banned "grout spacing" with "grout joints" (Docs 1 + 2 specifically) | §3.2 | Outstanding |
| m15 | About section: remove installation guidance; refocus on craft heritage, artisan sourcing, historical context, color spectrum | §6.1 | Outstanding |

---

## Per-template tracking matrix

One row per (template × finding) — 16 templates × 15 findings = up to 240 worker tasks. Most are mechanical; the 9-section restructure (C1) is the heaviest and should be done first per template.

| Template | C1 | C2 | C3 | C4 | C5 | C6 | M7 | M8 | M9 | M10 | M11 | m12 | m13 | m14 | m15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-zellige |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 02-zellige-mosaic |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 03-unglazed-natural-zellige |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 04-unglazed-natural-zellige-mosaic |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 05-ceramics-matte |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 06-field-trip-japan |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 07-cotto |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 08-cotto-allende |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 09-glass-mosaics |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10-terrazzo |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11-marble-solids |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12-marble-patterns |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13-cantera |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14-limestone |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15-cement |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16-roman-mosaics |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

**Cell values:** ✅ patched / ⏳ in progress / ❌ blocked / — N/A

---

## Order of operations

The 15 findings split into two phases:

**Phase 1 — structural (do per template, sequentially):**
- C1 (9-section restructure) — biggest lift; touches the entire page layout. Do this first so subsequent findings land in the right section.
- m15 (About refocus) — pairs with C1; once Installation content is in its own section, About is free to refocus on heritage.

**Phase 2 — mechanical batches (run across all 16 templates in parallel):**
- C2, C3, C4, C5, C6, M7, M8, M9, M10, M11, m12, m13, m14 — each is a find/replace or template-fill pattern. One `ao batch-spawn` per finding, 16 workers each.

---

## Stream C interaction with Stream A

The 8 templates that have a v3 revision (09–16) need a decision:

- **If the v3 already addresses some Stream C findings:** mark those cells ✅ before patching `drafts/{NN}.md`. Promote v3 first (Stream A), then re-audit.
- **If the v3 does not address Stream C findings:** patch `drafts/{NN}.md` against Stream C first, then re-evaluate whether the v3 is still relevant or stale.

Sequencing: **Stream A → re-audit → Stream C** for templates 09–16. Templates 01–08 go straight to Stream C.

---

## Out of scope

- The 35 files patched by the May 12 audit (commit `2ee3699`) — already done.
- gdocs-content/ SKU pages — they inherit template structure once Stream C is complete; re-audit them after.
- Net-new SKU pages — separate campaign.
