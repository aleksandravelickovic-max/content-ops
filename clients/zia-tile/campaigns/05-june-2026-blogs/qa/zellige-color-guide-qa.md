# QA Report: zellige-color-guide

- **Draft checked:** drafts/zellige-color-guide-v1.md (2026-07-02)
- **Final:** final/zellige-color-guide.md — all critical gates pass
- **Method:** exact-match grep sweep of every COMPLIANCE.yml term + manual read against STYLE-SYSTEM §12 (Voice, Terminology, Technical, Product Knowledge, Blog, SEO) and the task hard rules
- **Word count (final, incl. meta block):** 2,006 (~1,950 body) — within 1,500-2,000

## Violations found in v1 and fixed in final

| # | Type | Location (v1) | Issue | Fix |
|---|---|---|---|---|
| 1 | Ranking framing (task hard rule) | Intro, para 3 | "works best at the level of tone family" introduced the word "best" | Reworded: "is easier at the level of tone family" |
| 2 | Sentence-ending preposition (§2.1) | Grout paragraph | "...the full surface to play across." | "...an uninterrupted surface." |
| 3 | Repeated phrase (§6.3/§7.2) | Intro + FAQ 1 | "Our zellige collection features more than two hundred tiles" appeared twice verbatim | FAQ 1 reworded to "The collection spans more than two hundred tiles" |
| 4 | Word-audit repetition (§6.3) | Dark Tones, Combinations, FAQ 5 | "high contrast/high-contrast" three times | FAQ 5 reworded ("at the boldest end") |
| 5 | Product anchoring (§3.1) | FAQ 5 | "Carbon Black with Casablanca" / "Burnt Sugar with Terra Rosa" without "our" anchor | "our Carbon Black..." / "our Burnt Sugar..." |
| 6 | Word-audit repetition (§6.3) | Whites, Browns, Blues, Rooms, Combinations | "sits/settles/keeps/leans" clustering across sections | Varied: "reads warm," "falls between," "stand apart," "holds the pattern steady," "are a natural fit" |

Counts by type: 1 ranking-framing, 1 grammar/preposition, 3 repetition/word-audit, 1 terminology-anchoring. 0 factual, 0 compliance-critical, 0 invented colorways in v1.

## COMPLIANCE.yml — every banned term checked (final)

banned_terms: free shipping, discount, cheap, affordable, returns, peel-and-stick, bestselling, best seller, sources (production attribution), products, laid, the correct choice, most often specified, most popular, most specified, The practical summary, Practical summary:, Understanding the differences between — **0 hits each** (grep, case-insensitive). Note: "returns"/"sources" verified absent even as substrings of other words.

voice_bans: luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted, normal, built to, deepens with use — **0 hits each**. ("Muted" avoided entirely; matte/olive/subdued descriptors always paired with room behavior.)

## Technical guards (final)

| Guard | Status |
|---|---|
| zellige_no_freeze_thaw | PASS — stated affirmatively: "zellige is not suitable for outdoor installation in freeze/thaw climates" (Room by Room) |
| colorway_verified | PASS — 24 names used, all dual-verified (table below). Aegean/Absinthe/Tulum/etc. = 0 hits |
| production_step_verified | PASS — hand-pressed, sun-dried, hand-shaped, hand-dipped glaze, earthen kiln, uneven heat (all §8.5 #7 verified steps). "Chiseled" = 0 hits |
| no_kiln_type | PASS — "earthen kiln" only (a verified step); no wood/gas-fired claim |
| no_light_exposure_patina | PASS — no patina claims at all; lighting language is perception ("brightens/appear deeper," verbatim from colorway-reference.md), not aging |
| overage_rate_correct | PASS — "15-20%" + "25%" in overage FAQ; "10-15%" = 0 hits |
| prop65_link_required | PASS (vacuous) — no Prop 65 mention in the piece, so no link required |
| phone_present_with_email | PASS — email + phone together in all 3 occurrences (installation FAQ, overage FAQ, closing) |
| cotto/cement/unsold-product guards | PASS (vacuous) — no other materials referenced; no Saltillo; no unsold tiles |
| no_crazing_on_unglazed | PASS — crazing applied to glazed zellige only; Unglazed Natural excluded from the piece (§4.9 separate category) |

## Required presence

- **contact_block:** PASS — info@ziatile.com + 310-844-1170 together in (1) shower/installation FAQ, (2) quantity/overage FAQ, (3) closing paragraph.
- **person_consistency:** PASS — first person plural ("our," "we recommend") held throughout; you/your = 0 hits.

## Task hard rules

- No em dashes: PASS (0 hits, final and v1)
- No second person: PASS (0 hits)
- No fragments: PASS (manual read; "Yes."-style FAQ openers avoided)
- "each" not "every": PASS ("every" = 0 hits)
- No best-seller/ranking framing despite "best zellige colors" keyword: PASS — intent served via "Which zellige colors suit a kitchen backsplash?" FAQ; "best" = 0 hits in final
- "set" not "laid": PASS ("set in a running bond"; "laid" = 0 hits; "dry layout" is approved §8.5 language)
- Dynamic glazes explained, zellige-only: PASS (3 uses, defined in the light section)
- Chips, pits, and crazing always as the trio: PASS (3 occurrences, all three terms each time)
- Internal links: 2 total — collection page (intro) and installation guides (bathroom section), descriptive anchors, neither paragraph-initial. Within the 2-3 range.
- Installation Guide linked with descriptive anchor: PASS ("zellige installation guides")
- Sealing: verbatim approved dry-space wording used ("Always seal zellige according to our installation instructions, whether in dry spaces or in areas exposed to moisture, such as pools, spas, and showers"); no sealer product names.
- Colorway descriptions in design language: PASS — each family describes room behavior and pairings (plaster, oak, limewash, travertine, walnut, brass, marble); no "soft, warm, and light" spec framing.
- Negative framing: PASS — kitchen wet/heat framed as "suited to kitchen conditions, including heat and moisture" (approved §2.6 phrasing); protects/withstands/endures/overcomes = 0 hits. The freeze/thaw limitation is the mandated affirmative disclosure, not negative framing.

## STYLE-SYSTEM §12 checklist highlights

- Opening leads with color + search intent (not process); exact keyword "Zellige colors" is the first two words of body copy — §6.1 color-topic exception + §10.4 both satisfied.
- H1 contains "Zellige Color Guide" and "Zellige Colors"; keyword variant in two H2s ("Why Zellige Colors Shift with Light," "Zellige Colors, Room by Room").
- Collection named and linked in paragraph 2 with early colorway names (Casablanca, Carbon Black) — §6.2.
- Meta title 46 chars; meta description 151 chars with primary keyword + 2 use cases (kitchen backsplashes, shower walls).
- Paragraphs 2-4 sentences, varied length; every H3 ≥3 sentences; each H2 opens on its own subject.
- Proper concluding paragraph ending with the approved contact line; closes on a practical aside, not a CTA beyond the mandated contact line.
- Formats referenced (4x4, 2x2, 2x6, hex, trapezoid, 8x8 mesh checkerboard) all verified on live site + colorway-reference.md — §6.6 specific formats named in application sections.

## Colorway inventory (every name in the final draft + verification source)

All 24 names verified in BOTH `materials/colorway-reference.md` (Zellige section) AND the live collection page fetch (https://ziatile.com/collections/zellige, pages 1-2, 2026-07-02):

Casablanca (7 uses), Carbon Black (5), Terra Rosa (3), Savanna (3), Rouge (3), Racing Green (3), Pure White (3), Plum (3), Jade (3), Burnt Sugar (3), Amber (3), Tidepool (2), Sumac (2), Skylight (2), Night Blue (2), Za'atar (1), Prairie Green (1), Portuguese Blue (1), Pietro Pink (1), Nana's Lipstick (1), Glazed Earth (1), Desert Bloom (1), Cayenne (1), Brownstone (1).

Checkerboard pairings used (verified in colorway-reference.md mosaic table): Tidepool + Casablanca; Carbon Black + Casablanca; Burnt Sugar + Terra Rosa. Tone descriptors for each colorway cross-checked against the config table (e.g., Tidepool neutral-cool aqua, Racing Green cool jewel-toned, Sumac matte with coarser texture, Rouge burgundy/maroon notes that shift with light).

## Flagged uncertainties (not blocking, needs human follow-up)

1. **Live catalog vs config drift (HIGH priority):** the 2026-07-02 fetch of collection page 2 lists **Aegean and Absinthe** — the exact names COMPLIANCE.yml `colorway_verified` flags as invented — plus Tulum, Moroccan Blue, Glacier Blue, Superior Blue, Maya Blue, Cadmium, Graphite Grey, Slate Grey, and pattern series (Gambit, Lattice, Prismatic, Rubric, Perpetual Check, Radian) absent from `materials/colorway-reference.md`. Either the catalog grew after the June 2026 config compile or the fetch summary is unreliable. All were excluded fail-closed from this piece. Aleksandra/Emanuel should reconcile the master list and update the config + COMPLIANCE note.
2. **Internal cannibalization check:** Zia's live "Colors of Zellige: The Origin Story" post ranks for "zellige colors." This guide targets selection intent (distinct), but confirm positioning before publish.
3. "More than two hundred tiles" sourced from STYLE-SYSTEM §11 ("200+ tiles, mesh-backed mosaics"); the page-1 fetch estimated 80+ visible SKUs across a paginated collection, which does not contradict but also does not independently confirm the figure.
