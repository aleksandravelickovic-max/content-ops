# QA Report — glass-mosaic-tile-design

- **Draft:** drafts/glass-mosaic-tile-design-v1.md (QA run 2026-07-02, post-revision state)
- **Final:** final/glass-mosaic-tile-design.md
- **Verdict:** PASS — all critical gates clear. Violations found during drafting/QA are listed below with resolutions.

---

## 1. COMPLIANCE.yml — banned terms (exact-match scan)

| Term | Severity | Result |
|---|---|---|
| free shipping / discount / cheap / affordable / peel-and-stick | critical | Absent |
| **returns** | critical | **VIOLATION (3x) — FIXED.** Verb use ("returns light") in intro, bathroom intro, and backsplash FAQ collided with the exact-match business-exclusion ban. Rewritten to "reflects light" / "makes the most of whatever light a small room offers" / "brightens the work area". |
| sources (production attribution) | critical | Absent |
| products | critical | Absent (tiles/collections/material used throughout) |
| bestselling / best seller / most popular / most specified / most often specified | warning | Absent |
| laid | warning | Absent ("set" used) |
| the correct choice | warning | Absent (one near-miss in grout section, "Neither approach is the correct answer," rewritten to "Both approaches have a place") |
| The practical summary / Practical summary: / Understanding the differences between | warning | Absent |

## 2. COMPLIANCE.yml — technical guards

| Rule | Result |
|---|---|
| cotto_no_pools / cotto_allende_no_freeze_thaw / zellige_no_freeze_thaw / cement_non_freeze_thaw_only / no_combined_cotto_sealing | N/A — no other materials referenced |
| no_crazing_on_unglazed | PASS — no chips/pits/crazing anywhere; variation language is color, sheen, hand-placement per materials/glass-mosaics.md |
| no_kiln_type | **VIOLATION — FIXED.** A revision introduced "electric kilns in place of gas-fired ones"; the gas-fired contrast is unverified and was cut. "Electric kilns" itself is live-page-verified ("uses electric kilns"). |
| no_light_exposure_patina | N/A — no patina claims |
| no_unsold_products | PASS — no Saltillo, no competitor materials, no unsold items |
| overage_rate_correct | PASS — "15-20%" (2x) + "25%" (2x); no 10-15% anywhere |
| prop65_link_required | PASS (vacuous) — no Prop 65 mention; blog has no Installation & Finishing section, so §4.5 block not triggered |
| phone_present_with_email | PASS — 310-844-1170 appears with info@ziatile.com in all 3 occurrences (closing, install FAQ, quantity FAQ) |
| colorway_verified | PASS with one fix — all names cross-checked against live page (fetched 2026-07-02). **VIOLATION — FIXED:** Damascus (hue unknown) sat inside a neutrals-to-saturated gradient claim; swapped for self-describing Clover. Hue statements restricted to self-describing names only (Milk, Paperwhite, Canary, Clover, Kiwi, Jet Black, Rye, Camel, Umber, Lemon Drop, Tranquil Blue). Pattern/colorway pairings cited (Vaso Jasper + Piscine, Murano Marine Layer + Vespertine, d'Orsay Roma + Milk, Ells Tranquil Blue + Milk, Tesserae Milk + Camel + Umber, Cheque Marmot + Milk, Murano Lemon Drop + Kiwi, d'Orsay/Cheque Jet Black + Paperwhite) all live-verified. |
| production_step_verified | PASS — production claims limited to live copy + material config: 98% recycled glass, hand-placed 12x12 grids, wind/solar, electric kilns, Northern Spain |

## 3. COMPLIANCE.yml — voice bans

luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted (standalone), normal (variation), built to, deepens with use — **all absent**. Also scanned and absent: unique, truly, really, simply, of course, timeless, seamless, elevate, transform, robust, straightforward, slightly different, works as.

## 4. COMPLIANCE.yml — required presence

- **contact_block:** PASS — email + phone together in closing (§ "Glass Mosaic Tile at Zia"), installation FAQ, and quantity FAQ.
- **person_consistency:** PASS — first person ("our glass mosaics") held throughout; zero second-person hits (grep `\byou\b|\byour\b`). Imperatives limited to approved contact phrasings; "your project" removed from the stock overage phrasing.

## 5. Hard rules (recurring Jamie failures)

| Rule | Result |
|---|---|
| No em dashes | PASS — zero em/en dashes in file |
| No second person | PASS |
| No invention | PASS — all patterns, colorways, pairings, and suitability claims trace to the live collection page, materials/glass-mosaics.md, or STYLE-SYSTEM §11. Pattern geometry never described (unverified); only named pairings used. |
| No zellige language on glass | PASS — no dynamic glazes, no chips/pits/crazing |
| shower surround / grout spacing / trim pieces | Absent ("shower walls," "grout joints" used) |
| Negative framing (withstands/protects/endures/resists) | PASS — "suits kitchen conditions, including the heat and moisture behind a range" framing; "naturally stain-resistant" retained as the material config's own property language |
| Fragments | **VIOLATION (2x) — FIXED.** Standalone "Yes." / "No." FAQ openers rewritten as complete direct-answer sentences. |
| Meta-setup openers / report-style labels / name-drops | Absent (Union Station is a place reference from live copy, not a name-drop) |
| Overage 15-20% + 25% | PASS. **VIOLATION — FIXED:** first pass reused the §8.4-avoided rationale "allows greater freedom during the dry layout"; replaced with "plan for 25% across the full order." |
| Installation Guide link, descriptive anchor | PASS — "installation guides" linked in Samples section |
| 2-3 internal links, none opening a paragraph | PASS — 2 links (collection, installation guides). **VIOLATION — FIXED:** collection-section paragraph originally opened on the link; restructured to open on "Seven hand-placed patterns…" |

## 6. STYLE-SYSTEM §12 checklist

- **Voice & tone:** warm lead anchored in place (Northern Spain) and material behavior (light, sheen); no cliché adjectives; no sentence-ending prepositions (one fixed: "decisions the material calls for"); antithesis/"rather than" constructions reduced from 5 to 0 in the human-writing pass; metaphors cut ("opens the door," "deep bench," "center of gravity").
- **Terminology:** "each" used for individual tiles ("every" absent); collection anchored ("our Vaso," "our Ells," "our Piscine"); grout joints / shower walls correct.
- **Technical accuracy:** freeze/thaw SUITABLE, pools/spas SUITABLE (saltwater or chlorine), sealing = none for glass + optional grout sealing only, slip spec = minimum 1/8" grout joints + anti-slip treatment after installation — all per materials/glass-mosaics.md (confidence: high). Slip language appears only in wet-area sections (pool wet floors, shower floors, shower FAQ).
- **Blog structure:** material/place lead, collection + patterns named in first paragraph (§6.2); each H2 a new angle (definition, collection, pool, bathroom, backsplash, grout, ordering); every H2/H3 ≥3 sentences; proper concluding recap section ending on the contact line; FAQ of 7 direct-answer paragraphs.
- **SEO:** exact "glass mosaic tile" in H1, first sentence, "What Is" H2, recap H2, and 4 FAQ headings; "glass tile backsplash" and "glass pool tile" as H2s; meta title 57 chars; meta description 144 chars with keyword + 3 use cases (pools, shower walls, kitchen backsplashes); paragraphs 2-4 sentences, varied length; no -ing verbs in headings ("need sealing" in an FAQ heading is a noun use).
- **Word count:** 1,540 body words (target 1,500-2,000).

## 7. Violation counts (found and fixed)

| Type | Count |
|---|---|
| Critical banned term ("returns" verb collision) | 3 |
| Technical guard (unverified kiln contrast) | 1 |
| Colorway hue inference (Damascus gradient; plus pre-write cuts: Vespertine/Marine Layer "deeper water tones," Marmot "quieter") | 3 |
| Fragments (Yes./No. FAQ openers) | 2 |
| Approved-phrasing conflicts (§8.4 overage rationale; "your project" in stock contact phrasing; "the correct answer") | 3 |
| Link placement (paragraph opening on a link) | 1 |
| AI-pattern cleanup ("rather than" x5, metaphors x4, preposition ending x1, repetition x5) | 15 |

## 8. Flagged uncertainties (not blocking)

1. **Milk 1x1 shows "In Transit" on the live page.** Milk is used in copy as a colorway (it appears in many live pattern pairings). If stock status matters editorially, swap standalone-solid mentions of Milk for Paperwhite.
2. **"Seven patterns" reconciled:** live page names exactly seven pattern families (Vaso, Union, d'Orsay, Ells, Tesserae, Murano, Cheque), matching §11's "7 patterns."
3. **Cleaning claims** kept generic ("routine cleaning") — no pH-neutral-cleaner specifics asserted, since cleaning guidance is not in the material config; the FAQ defers to installation guides.
4. **Pool wet-floor slip guidance** extends the config's "shower floors and wet floors" rule to pool-adjacent floors; the config wording supports it, but confirm with Alex if pool decks were meant to be out of scope.
5. **Solid colorway count not stated** in copy (live page lists fifteen incl. Milk); avoided a written-out count in case the catalog shifts.
