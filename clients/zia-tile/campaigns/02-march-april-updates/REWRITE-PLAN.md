# March/April Rewrite Plan — Zia Tile Campaign 02

**Source of truth:** [Zia Tile – LinkGraph – Campaign Sheet](https://docs.google.com/spreadsheets/d/1frMiXuEZ59blQTqr9TJnMSQlU9zfe2Cp-z8YLgyui80/edit?gid=1815073147) (Google Sheets, last modified 2026-05-13)
**Drafted:** 2026-05-13
**Owner:** Aleksandra Velickovic
**Editorial pair:** Aleksandra + Emanuel
**Client review:** Jamie Greenspan
**Excluded:** Lucas (per agentic-content channel rules)

---

## Scope confirmed from the sheet

Active editorial work (Editing / In Progress / Zia to review) **only** — Published rows are out.

| Tab | March | April | Subtotal (Mar+Apr) | May (informational) |
|---|---:|---:|---:|---:|
| Collection / Core pages | 19 | 18 | **37** | 14 install guides |
| Product pages (SKUs) | 31 | 42 | **73** | 42 |
| Blog posts | 10 | 10 | **20** | 14 |
| **Total** | **60** | **70** | **130** | 70 |

**130 pieces in March/April scope.** 200 if May expands in.

The 3 already demonstrated ([blog-4-cotto](drafts/blog-4-cotto.md), [collection-cotto](drafts/collection-cotto.md), [product-red-clay-8x8](drafts/product-red-clay-8x8.md)) are the **golden reference patterns** for the remaining 127. Every batch below copies their structure and runs the same STYLE-SYSTEM + audit-report compliance pass.

---

## The 3 patterns — what each batch reuses

| Piece type | Reference file | What it standardizes |
|---|---|---|
| Blog post | [blog-4-cotto.md](drafts/blog-4-cotto.md) | First-person voice; Jamie's approved opener (material → place → distinctive); no product names; AD register; em-dash discipline; concluding paragraph; FAQ with mixing question |
| Collection page | [collection-cotto.md](drafts/collection-cotto.md) | "Our Take on [Material]" opener; no "charming"; no "well-suited for any climate" closer; FAQ block including Cotto vs Cotto Allende framing where relevant; verbatim sealing copy |
| Product page (SKU) | [product-red-clay-8x8.md](drafts/product-red-clay-8x8.md) | All 9 required sections in order; usage chart with correct freeze/thaw + pool/spa by material; inline sealing + 1/8" + anti-slip in shower row; verbatim §11.2 shipping copy; 6+ FAQ |

---

## Phase 1 — Reference set complete (today, done)

✅ blog-4-cotto.md, collection-cotto.md, product-red-clay-8x8.md committed and pushed to `feat/zia-campaign-02-scaffold` (commits `83e013c` + `88cb541`).
✅ [CHANGES.md](drafts/CHANGES.md) maps every edit to a STYLE-SYSTEM section or audit-report finding (X1–X10).
✅ Share docs ([share/](share/)) rendered as PDF + DOCX + HTML for Jamie review.

**Gate:** Jamie signs off on the 3 reference files. Nothing in Phase 2 ships until those are approved. If Jamie flags new patterns, they go into STYLE-SYSTEM.md before re-running.

---

## Phase 2 — Material collection pages (Stream B1, 12 pages)

12 of the 19 March collection pages are material/category pages that map 1:1 with templates already in [drafts/](../01-product-collection-pages/drafts/):

| Page (sheet) | Template in repo | v3 exists? |
|---|---|---|
| Material – Zellige | drafts/01-zellige.md | no |
| Material – Cement | drafts/15-cement.md | **yes** |
| ✅ Material – Cotto | drafts/07-cotto.md (done as collection-cotto.md) | no |
| Material – Cotto Allende | drafts/08-cotto-allende.md | no |
| Material – Glass Mosaics | drafts/09-glass-mosaics.md | **yes** |
| Material – Terrazzo | drafts/10-terrazzo.md | **yes** |
| Material – Marble | drafts/11-marble-solids.md + drafts/12-marble-patterns.md | **yes** |
| Material – Roman Mosaics | drafts/16-roman-mosaics.md | **yes** (held — folding into Marble per Jamie) |
| Material – Cantera | drafts/13-cantera.md | **yes** |
| Material – Limestone | drafts/14-limestone.md | **yes** |
| Material – Ceramics | drafts/05-ceramics-matte.md | no |
| Material – Field Trip: Japan | drafts/06-field-trip-japan.md | (held — folding into Ceramics per sheet comment) |

**Action:**
1. For each material page, pull the gdocs export from [gdocs-content/collection-pages/](../01-product-collection-pages/gdocs-content/collection-pages/) (the actual March/April production draft).
2. Run it through the same 10-step reconciliation that produced collection-cotto.md (CHANGES.md §X1–X10).
3. Output to `campaigns/02-march-april-updates/drafts/collection-{material}.md`.
4. For the 7 materials with a v3 revision in [drafts/v3/](../01-product-collection-pages/drafts/v3/), run the merge gate from [v3-promotion-worklist.md](v3-promotion-worklist.md) **first**, then run the Phase 2 reconciliation against the merged v3.

**Workers:** `ao batch-spawn` 10 workers (one per material, minus the 2 held). Each worker reads STYLE-SYSTEM.md + audit-report.md + the gdocs export + collection-cotto.md as the pattern, produces the corrected `.md`, and opens a PR. Estimated wall time with 4 concurrent workers: ~half a day.

**Gate:** Aleksandra + Emanuel review each output against collection-cotto.md. Hold merges to live until Jamie signs off on Cotto first.

---

## Phase 3 — Shape, Color, Space, Trade collection pages (Stream B2, 25 pages)

25 pages remaining across March (7 shapes) and April (13 colors + 4 spaces + 1 trade):

- **Shapes (7):** Square, Rectangle, Subway, Hexagon, Large Format, Special Shape, (one duplicate in sheet — confirm with Aleksandra)
- **Colors (13):** White, Tan, Yellow, Orange, Pink, Red, Brown, Grey, Green, Blue, Purple, Black, Pattern
- **Spaces (4):** Bathroom, Kitchen, Outdoor, Shower
- **Trade (1):** Trade Program

These don't have 1:1 templates in `drafts/`. The pattern is the same as material collection pages, but the content is different — these are **navigation / discovery pages** that aggregate products across materials.

Some of these already exist as gdocs in [gdocs-content/collection-pages/](../01-product-collection-pages/collection-pages/) (e.g., shape-hexagon, shape-subway, space-kitchen, space-outdoor, trade-program were in the May 12 patch). Audit each against the Cotto pattern + STYLE-SYSTEM.

**Workers:** `ao batch-spawn` 25 workers (batches of 8 concurrent). Each reads collection-cotto.md as pattern + the existing gdocs export + STYLE-SYSTEM.md. Estimated: ~1 day.

**Gate:** Aleksandra + Emanuel pair review; Jamie spot-checks 3 (one shape, one color, one space) before approving full batch.

---

## Phase 4 — Product page SKUs (Stream B3, 73 pages)

73 product pages: 31 March + 42 April. All have live URLs (column 3 in the sheet) and gdocs exports labeled "Structure Updated."

**Material breakdown** (sampled from sheet — full count to verify in execution):
- Zellige SKUs: largest group (~30-40 pages incl. Casablanca, Pure White, Burnt Sugar, Glazed Earth, Racing Green, Absinthe, Tidepool, Aegean, Rouge, Desert Bloom, and more)
- Cotto SKUs: ~10-15
- Limestone SKUs: ~5-8
- Ceramic / Terrazzo / Marble: smaller batches

**Pattern:** product-red-clay-8x8.md is the gold reference. Every SKU page must:
1. Have all 9 required sections in §8.5 order.
2. Use material-appropriate variation language (zellige = chips/pits/crazing trio; Cotto = tone/shape/edge/thickness; etc.).
3. Mark Pools+Spas correctly per material (unglazed Cotto ✗, Cotto Allende ✓, zellige ✗, marble varies).
4. Use verbatim §11.2 shipping copy.
5. No sealer/cleaner/grout product names.

**Workers:** Split into **3 sub-batches by material** to avoid cross-contamination of material-specific rules:
- **Sub-batch 4A: Zellige SKUs** — workers reference STYLE-SYSTEM §4 + §6.7-§6.8 zellige sections. Pools+Spas = ✗, freeze/thaw = ✗.
- **Sub-batch 4B: Cotto + Cotto Allende SKUs** — workers reference product-red-clay-8x8.md directly + STYLE-SYSTEM §5. Cotto Pools+Spas = ✗, Cotto Allende Pools+Spas = ✓.
- **Sub-batch 4C: Stone (limestone, marble, cantera) + ceramic + terrazzo SKUs** — workers reference STYLE-SYSTEM §4.1 climate table.

`ao batch-spawn` 73 workers across 3 sub-batches, ~10 concurrent. LLM-as-judge runs against the audit-report.md per-template findings before each PR opens. Estimated: 2-3 days.

**Gate:** Editorial pair signs off in groups of 10. Jamie spot-checks 1 SKU per material as the batch progresses.

---

## Phase 5 — Blog posts (Stream B4, 20 posts)

20 blog posts: 10 March + 10 April. Sheet's Tab 3 has Pillar Page (the collection it links to) and Target Keywords for each.

**Already flagged in the sheet:**
- "Saltillo Tile: What It Is and How to Use It" — **On Hold**, Jamie's comment: *"Do not want a Saltillo blog post... we do not sell Saltillo."* → Cancel this post; salvage keyword research into the Cotto blog instead.

**Pattern:** blog-4-cotto.md is the reference. Each blog needs:
1. Jamie's approved opener structure (material → place → distinctive characteristic).
2. First or third person held consistently throughout.
3. Pillar collection page linked in opener (sheet's "Pillar Page" column).
4. Target keywords (sheet column) integrated naturally — no keyword stuffing.
5. Concluding paragraph (not abrupt).
6. FAQ block when format permits.

**Workers:** `ao batch-spawn` 19 workers (20 minus Saltillo). 5 concurrent. Estimated: 1-2 days.

**Gate:** Editorial pair on each. Jamie reviews the first 3 (Terracotta Floor Tile, Zia Cotto Colors, Kitchen Backsplash) before the rest ship.

---

## Phase 6 — May install guides (informational only — out of scope unless approved)

14 install guides currently In Progress per the sheet. Treat as Phase 6 candidates if the team wants May rolled in. Otherwise hand off cleanly at end of April work.

---

## Total estimated effort

| Phase | Pieces | Workers (concurrent) | Wall time |
|---|---:|---:|---:|
| 1 — Reference set | 3 | 1 | done |
| 2 — Material collection pages | 10 | 4 | ~0.5 day |
| 3 — Shape/Color/Space/Trade | 25 | 8 | ~1 day |
| 4A — Zellige SKUs | ~35 | 10 | ~1 day |
| 4B — Cotto + Cotto Allende SKUs | ~15 | 10 | ~0.5 day |
| 4C — Stone/Ceramic/Terrazzo SKUs | ~23 | 10 | ~0.75 day |
| 5 — Blog posts | 19 | 5 | ~1.5 days |
| **Total to ship Mar/Apr** | **130** | | **~5-6 working days** |

Plus client review windows (Jamie's bandwidth is the real bottleneck — likely the binding constraint, not worker throughput).

---

## Prerequisites (gates before Phase 2 starts)

1. **Multi-Agent stack installed.** See [docs/sops/multi-agent-tab-system-setup.md](../../../../docs/sops/multi-agent-tab-system-setup.md). Without AO + GSD, phases 2-5 fall back to sequential edits, which kills throughput.
2. **Jamie signs off on the 3 reference files.** Without that gate, every batch risks rework.
3. **v3-promotion-worklist.md decisions logged.** 7 of the material collection pages depend on whether their v3 revision is approved (Phase 2 gating).
4. **STYLE-SYSTEM.md is the only style authority.** Confirm with the team that no one is writing from memory of the older style-guide-v2.md.

---

## Risks / known blockers

- **Roman Mosaics → Marble** and **Field Trip Japan → Ceramics** reorgs are pending Jamie confirmation. Don't ship those collection pages until the merge is approved.
- **Saltillo blog post on hold.** Confirm cancellation, don't let it slip back into a worker batch.
- **Collection page merges held pending Jamie's review.** Workers can produce PRs in Phase 2–3, but merges to live wait on Jamie.
- **Jamie's review bandwidth.** With 130 pieces in flight, batching the reviews (groups of 5-10) is required. Don't surface them one-by-one.
- **Writer team training.** Plan assumes Aleksandra + Emanuel + workers do the heavy lifting. If Milena / Emilija / James / Mina / Andresa / Mateus join, they should pair on the 3 reference files first.

---

## What ships when

| Milestone | What's shipped |
|---|---|
| End of Phase 1 (today) | 3 reference files reviewed by Jamie |
| End of Phase 2 (+0.5 day) | 10 material collection pages PR'd; 7 v3 decisions logged |
| End of Phase 3 (+1.5 days) | 25 navigation collection pages PR'd |
| End of Phase 4 (+3.5 days) | 73 SKU product pages PR'd |
| End of Phase 5 (+5 days) | 19 blog posts PR'd |
| End of review cycle (+1 week if Jamie batches well) | All 130 merged to drafts; collection pages held at merge to live |
