# QA Report — fireplace-tile-zellige-and-cement (v1 → final)

Date: 2026-07-02. Checked against COMPLIANCE.yml (all banned terms, technical guards, voice bans, required-presence), STYLE-SYSTEM §12 (Voice & Tone, Terminology, Technical Accuracy, Product Knowledge, Blog Posts, SEO), and the campaign hard rules.

## COMPLIANCE.yml — banned terms (exact-match scan, full file)

| Term | Result |
|---|---|
| free shipping / discount / cheap / affordable / returns / peel-and-stick | PASS (0 hits) |
| bestselling / best seller | PASS |
| sources (production attribution) | PASS |
| products | PASS ("materials," "tiles," "collections" used) |
| laid | PASS ("set" used throughout) |
| the correct choice / most often specified / most popular / most specified | PASS |
| The practical summary / Practical summary: / Understanding the differences between | PASS |

## COMPLIANCE.yml — technical guards

| Rule | Result |
|---|---|
| cotto_no_pools / cotto_allende_no_freeze_thaw / no_combined_cotto_sealing | N/A — Cotto not referenced |
| zellige_no_freeze_thaw | PASS — stated plainly: "Glazed zellige is not suitable for outdoor installation in freeze/thaw climates" (body + outdoor FAQ) |
| cement_non_freeze_thaw_only | PASS — "suitable for exterior use in non-freeze/thaw climates only" (body + outdoor FAQ) |
| no_crazing_on_unglazed | PASS — chips/pits/crazing applied to zellige only (3 uses, all zellige); cement described via tone, pattern, matte surface |
| no_kiln_type | PASS — "kiln-fired" generic only, no wood/gas claim |
| no_light_exposure_patina | PASS — cement patina "with wear and time" |
| no_unsold_products | PASS with note — "firebrick" named once as the firebox lining (construction fact needed for the honest heat framing, not a tile positioned against Zia's range) |
| overage_rate_correct | PASS — exact strings "15-20%" and "25%" present; no 10-15% variant |
| prop65_link_required | PASS — Proposition 65 mention hyperlinked to ziatile.com/proposition-65-warnings |
| phone_present_with_email | PASS — 5/5 occurrences of info@ziatile.com paired with 310-844-1170 in the same sentence |
| colorway_verified | PASS — all zellige names (Casablanca, Pure White, Glazed Earth, Burnt Sugar, Amber, Racing Green, Tidepool, Plum) and cement names (Elemental Blue, Midnight, Jaipur Pink, Zig Zag, Kepler, Flora, Stars & Cross) verified on the live collection pages 2026-07-02; formats match live listings |
| production_step_verified | PASS — zellige: hand-glazed / hand-shaped; cement: hand-poured, pressed, never fired (live-page + config language); no "chiseled" |

## COMPLIANCE.yml — voice bans

luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted (standalone), normal (variation), built to, deepens with use: **0 hits — PASS.**

## Required presence

- contact_block: PASS — email + phone together in closing and in the quantity, sealing/installation, hearth, and zellige-fireplace FAQ answers.
- person_consistency: PASS — third person ("Zia's zellige") held; zero you/your/we/our; imperatives limited to FAQ/contact phrasings matching the approved checkerboard v5 pattern.

## Hard rules (campaign brief)

- No second person: PASS (regex scan, 0 hits).
- No em dashes: PASS (0 em/en dashes in the article).
- Chips/pits/crazing as trio, zellige only: PASS. "Dynamic glazes" zellige-only: PASS (1 use, zellige section).
- Freeze/thaw per material: PASS. Cement never fired + matte: PASS (stated twice).
- No invention: all colorways/formats from live pages; tone descriptions limited to names verified in the approved checkerboard v5 (Casablanca off-white register, Tidepool cool, Burnt Sugar/Glazed Earth/Amber warm) or name-evident tones.
- Banned Jamie terms (built/wear-use/recessive/negative framing/fragments/meta openers/report labels/name-drops): PASS. No designer or competitor brand names.
- Installation Guide linked with descriptive anchor: PASS. Internal links: 3 editorial (zellige collection, cement collection, Installation Guide) + the required Prop 65 compliance link. No paragraph opens with a link (see fix 4).
- Sentence-ending prepositions: regex scan 0 hits.

## SEO (§10.4, §12)

- H1 contains "Fireplace Tile": PASS. Exact keyword in first sentence: PASS.
- Keyword in H2s ("Fireplace Tile at Zia," "Fireplace Tile Ideas for Each Surface"); "zellige fireplace" variant in H3 + body: PASS.
- Meta title 49 chars, keyword at front: PASS. Meta description 154 chars, keyword + use cases (surrounds, feature walls, chimney breasts): PASS.
- Body word count 1,966 (target 1,500-2,000): PASS.
- Paragraphs 2-4 sentences, varied length: PASS.

## Issues found in v1 → fixed in final

| # | Type | Location | Issue | Fix |
|---|---|---|---|---|
| 1 | Structure (§6.3 H3 minimum) | Hearth FAQ | Answer ran 2 sentences; FAQ answers elsewhere run 3+ | Expanded to 3 sentences |
| 2 | Repetition (word audit) | 4 uses of "rather than" across the piece | Mechanical echo | Reduced to 2; rewrote cement-surround, feature-wall, and sealing-FAQ sentences |
| 3 | Repetition | "quiet consistency" in §Fireplace Tile at Zia intro and recap | Duplicate phrase | Intro rephrased to "steady matte pattern" |
| 4 | Linking rule | Cement H3 first paragraph opened "Zia's [cement tile](…)" | Link in paragraph-opening position | Link moved to the second sentence |
| 5 | Repetition (§6.3) | "surround" 3x inside The Surround and Face section | Same noun >2x in one section | Cement paragraph rewritten around "the frame"/"the face" |
| 6 | Grammar | "stretches a low fireplace taller" | Awkward construction | "draws a low fireplace upward" |

Counts: 0 critical compliance violations; 6 editorial/structural issues found and fixed. All critical gates clear in final.

## Flagged uncertainties (not fixable in copy — for Aleksandra/Alex)

1. **Heat/fireplace suitability is unverified for both materials.** Neither `materials/zellige.md`, `materials/cement.md`, nor the live collection pages state heat or fireplace suitability. Competitors (Clé, Zelligery, Riad) claim zellige heat-resistance outright; this piece deliberately does not. The article frames both materials around the surround/feature-wall surface, states the firebox is a separate refractory assembly, and routes working-fireplace specification questions to Zia's team. STYLE-SYSTEM §10.3's approved meta example lists "fireplace walls" as a zellige application, which is the only in-system grounding for the surface framing. **Confirm with Alex/Zia whether an affirmative heat statement can be added later.**
2. **Hearth guidance does not exist in any Zia source.** The hearth FAQ answers honestly (exposure differs; contact the team) rather than asserting suitability.
3. **Zellige colorway gate is `verify` in the material config.** All names used were re-verified against the live collection page on 2026-07-02; if the catalog changes before publish, re-check.
4. **Link count:** 3 editorial internal links plus the mandatory Prop 65 link = 4 total anchors. Counted the Prop 65 link as compliance, not editorial; flag if the 2-3 rule is meant to be absolute.
