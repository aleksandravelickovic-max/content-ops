# Production Log

## Batch: june-blogs-batch-01

**Date:** 2026-07-02
**Input:** `batches/june-blogs-batch-01.csv` (built from the LG Team tracker table)
**Topics processed:** 8 / 10 (2 skipped as On Hold)
**QA failures requiring revision:** All 8 required at least one revision pass. Zero critical violations remained in any final (aggregate grep sweep confirmed: 0 em dashes, 0 second person, 0 COMPLIANCE.yml critical terms, correct overage, contact block paired in every file).
**Voice-gate follow-up:** Initial voice-judge pass found 2 / 8 above the 80 floor (Fireplace 83, Grout 83) and 6 / 8 below floor (Glass Mosaic 78, Mosaic 78, Limestone 78, Zellige Color Guide 78, Outdoor 78, Commercial Cement 72). Follow-up revisions attached technical claims to surface behavior, light, texture, and room-read rather than leaving suitability/sealing specs as bare checklist copy.
**Post-editorial QA pass:** Aleksandra feedback applied after the initial final set. All 8 finals now include visible keyword metadata, exactly 4 FAQ questions, Jamie-preferred overage phrasing (minimum 15%, 20% for tighter control, 25% for more uniform selection), and verified product-level links where available. Targeted scan confirmed 0 hits for `15-20`, `approved/approval`, `performs`, `every`, `uneven`, `reach out`, em dashes, and second person. See `qa/post-editorial-batch-qa-2026-07-02.md`.
**Skipped topics:** Marble Tile (On Hold), Hand-Painted Tiles / Artisan Ceramics (On Hold)

---

### Topic 1: Fireplace Tile: Zellige and Cement for Feature Walls
- **Slug:** fireplace-tile-zellige-and-cement
- **Files:** briefs/, drafts/ (-v1), qa/, final/ — all present. Final: 1,970 words.
- **QA issues fixed:** 6 (structure, repetition, link placement, grammar). 0 critical in v1.
- **Flags:** Heat/fireplace suitability is UNVERIFIED for zellige and cement in configs and live pages — article frames around surround/feature-wall surfaces and routes firebox specs to the team. Confirm with Alex before any affirmative heat claim.
- **Status:** PASS

### Topic 2: Glass Mosaic Tile: Pool, Bathroom & Backsplash Design
- **Slug:** glass-mosaic-tile-design
- **Files:** all present. Final: 1,540 body words.
- **QA issues fixed:** 28 (3 critical "returns"-verb collisions, 1 unverified kiln contrast, hue inferences, fragments, 15 voice cleanups).
- **Voice follow-up:** Initial voice score 78. Revised pool/wet-floor and FAQ passages so freeze/thaw, pool approval, and 1/8" grout-joint specs carry light, water, and grid behavior rather than repeating as flat suitability copy.
- **Flags:** Milk 1x1 shows "In Transit" on live page; pool-deck slip guidance extends the config's wet-floor rule — confirm scope with Alex.
- **Status:** PASS

### Topic 3: Tile Grout Guide: Choosing Grout for Zellige & Cement
- **Slug:** tile-grout-guide
- **Files:** all present. Final: 1,621 body words.
- **QA issues fixed:** 8 (2 critical: "seamless", implied second person; 6 warnings).
- **Voice follow-up:** Initial voice score 83. Kept the required closing contact line, but preserved the maker-intent final sentence so the piece no longer ends on a CTA beat.
- **Flags:** Repo zellige installation guide itself uses "grout spacing" and "laid" (lines 74-78) — source-file cleanup candidate. Spot-check joint/cure figures against live guides before publish.
- **Status:** PASS

### Topic 4: Limestone Tile: Honed vs Brushed + Care Guide
- **Slug:** limestone-tile-honed-vs-brushed
- **Files:** all present. Final: 1,630 words.
- **QA issues fixed:** 11 (3 critical incl. invented colorway tone descriptions — cut).
- **Voice follow-up:** Initial voice score 78. Revised care, wet-floor, and ordering passages so cleaning chemistry, sealing, and finish choices are tied to the matte face, stippled relief, patina, and actual room light.
- **Flags:** Live finishes are Honed and Bush Hammered ("brushed" mapped as search term only). Live page shows Antiqued Polished + Heathered finishes and Belgian Bluestone / French Cobblestone lines not in config — config update + Alex confirmation needed.
- **Status:** PASS

### Topic 5: Mosaic Tile: What It Is and How Designers Use It
- **Slug:** mosaic-tile-guide
- **Files:** all present. Final: 1,596 words.
- **QA issues fixed:** 5 (0 critical; tricolon, repetition, -ing heading).
- **Voice follow-up:** Initial voice score 78. Reworked Roman Mosaics, glass, zellige, shower-floor, and pool FAQ passages so approval/sealing specs sit beside veining, water, dynamic glazes, dense grout texture, and hand placement.
- **Flags:** Roman Mosaics is still its own live collection (NOT merged under Marble). Live site spells "Verde Alpi"; STYLE-SYSTEM §11 says "Verdi Alpi" — style system likely needs the fix. Bardiglio Imperiale on live page, absent from §11.
- **Status:** PASS

### Topic 6: Cement Tile for Commercial Spaces
- **Slug:** cement-tile-commercial-spaces
- **Files:** all present. Final: 1,684 words.
- **QA issues fixed:** 12 (4 critical: "printed", person mixing, fragment, unsold-material comparison).
- **Voice follow-up:** Initial voice score 72. Revised wet-zone, care, and FAQ sections so slip specs, pH-neutral cleaning, and resealing guidance connect to matte surface behavior and hospitality/retail room use.
- **Flags:** 68-color count is from STYLE-SYSTEM §11 only — live page states no total; confirm with Alex. Vietnam + 1850s French/Catalan origin pairing not yet Jamie-reviewed.
- **Status:** PASS

### Topic 7: The Zellige Color Guide
- **Slug:** zellige-color-guide
- **Files:** all present. Final: ~1,950 body words.
- **QA issues fixed:** 6 (0 factual/colorway violations in any version).
- **Voice follow-up:** Initial voice score 78. Reworked abstract color-position lines (Pure White, Jade, Skylight, Sumac), removed "great choice" buying-guide phrasing, and moved the contact line before the closing eight-hundred-years image.
- **Colorways:** 24 used, each verified in BOTH materials/colorway-reference.md AND the live collection (2026-07-02).
- **Flags:** CONFIG/CATALOG DRIFT (high priority): live page now lists Aegean and Absinthe — the exact names COMPLIANCE.yml flags as invented — plus 8 more colorways and 6 pattern series absent from the config. All excluded fail-closed. Reconcile colorway-reference.md + the COMPLIANCE.yml note. Also check cannibalization vs the existing "Colors of Zellige: The Origin Story" post.
- **Status:** PASS

### Topic 8: Outdoor Tile for Patios, Pool Decks and Gardens
- **Slug:** outdoor-tile-patios-pool-decks-gardens
- **Files:** all present (QA includes a 28-claim suitability audit, each claim mapped to its config source). Final: 1,760 body words.
- **QA issues fixed:** 9 (2 technical: "hand-dipped" on Cotto Allende → "hand-glazed"; exclusivity overclaim vs live outdoor page).
- **Voice follow-up:** Initial voice score 78. Revised material and FAQ sections so climate/pool limits are paired with garden light, matte cement in sun, Cantera aggregate, limestone finish texture, Cotto patina, and wet-floor traction planning.
- **Flags:** Ceramics is on the live outdoor page (all-weather, pool-recommended) but has no complete outdoor entry in configs — omitted; create/extend ceramics.md before future outdoor pieces. Cantera written per config (non-freeze/thaw exterior only), which is stricter than the tracker note.
- **Status:** PASS

---

## Summary

| Metric | Count |
|---|---|
| Topics in tracker | 10 |
| Topics processed | 8 |
| Skipped (On Hold) | 2 |
| Briefs / drafts / QA reports / finals | 8 each |
| QA passes on first draft | 0 |
| QA passes after revision | 8 |
| Critical violations remaining in finals | 0 |
| Voice scores below floor on first judge pass | 6 |
| Warmth revisions completed | 8 |

**Most common v1 violations across the batch:** negative/contrast framing ("rather than", endurance verbs), repetition caught by the §6.3 word audit, implied or literal second person, banned exact-match terms colliding with ordinary usage ("returns light", "printed").

**Voice-gate note:** The repeated failure mode was over-corrected technical copy: suitability rules, sealing steps, and grout specs were accurate but too often stood alone. Revisions kept the facts intact and added earned warmth through material behavior: glaze shift, hand placement, patina, matte surfaces, aggregate shadow, grout-grid texture, and real room light.

**Cross-batch source-of-truth gaps surfaced (for Aleksandra/Emanuel/Alex):**
1. Zellige colorway config vs live catalog drift — incl. Aegean/Absinthe now being REAL live colorways despite the COMPLIANCE.yml invented-name flag.
2. Limestone config missing two live finishes and two lines.
3. STYLE-SYSTEM §11 "Verdi Alpi" vs live "Verde Alpi".
4. No ceramics outdoor config despite live outdoor-collection placement.
5. Heat/fireplace suitability unverified anywhere in the knowledge base.
6. Repo zellige installation guide uses non-compliant terminology internally.

**Review status:** All 8 finals passed Aleksandra's post-editorial QA feedback pass and await Emanuel/final delivery review. Nothing delivered to Jamie.
