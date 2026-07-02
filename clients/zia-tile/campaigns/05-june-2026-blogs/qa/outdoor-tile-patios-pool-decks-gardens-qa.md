# QA report: outdoor-tile-patios-pool-decks-gardens

- **Draft audited:** drafts/outdoor-tile-patios-pool-decks-gardens-v1.md (1,827 words incl. meta block)
- **Date:** 2026-07-02
- **Result:** v1 passes all mechanical COMPLIANCE.yml gates. Manual audit found 9 issues (2 technical-accuracy, 7 voice/precision). All fixed in final/outdoor-tile-patios-pool-decks-gardens.md.

---

## 1. COMPLIANCE.yml banned terms (grep, exact match)

| Term | Severity | Result |
|---|---|---|
| free shipping | critical | absent |
| discount / cheap / affordable / returns / peel-and-stick | critical | absent |
| bestselling / best seller | warning | absent |
| sources (production attribution) | critical | absent ("sources" does not appear at all) |
| products | critical | absent (tiles/collections/materials/lines used) |
| laid | warning | absent ("set" used) |
| the correct choice | warning | absent ("a great choice" used once, per approved wording) |
| most often specified / most popular / most specified | warning | absent |
| The practical summary / Practical summary: | warning | absent |
| Understanding the differences between | warning | absent |

## 2. COMPLIANCE.yml voice bans (grep)

luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted, normal (variation), built to, deepens with use — **all absent.** Patina phrased as "deepens with wear" and "Use and time deepen the tone" (both approved forms, §3.2/§6.5).

## 3. COMPLIANCE.yml technical guards

| Guard | Severity | Result |
|---|---|---|
| cotto_no_pools | critical | PASS. Cotto stated as not suitable for full submersion in three places, all using the approved §8.3 wording. Cotto is presented for decks/exterior floors only, never pool interiors. |
| cotto_allende_no_freeze_thaw | critical | PASS. Stated affirmatively in the Cotto Allende H3, the pool FAQ (approved §8.3 wording verbatim), and the freeze/thaw FAQ. |
| zellige_no_freeze_thaw | critical | PASS. "Not suitable for outdoor installation in freeze/thaw climates" stated plainly in body prose (Zellige H3) and in two FAQ answers. |
| cement_non_freeze_thaw_only | critical | PASS. "Suitable for exterior use in non-freeze/thaw climates only" in the Cement H3, plus the climate section and two FAQs. No pool claim made (config: verify). |
| no_combined_cotto_sealing | critical | PASS. No sealing instructions given inline; article states Cotto and Cotto Allende "follow separate instructions" and directs to the Installation Guide. No sealer product names. |
| no_crazing_on_unglazed | critical | PASS. Chips/pits/crazing trio applied to zellige only. Cotto variation described via tone/patina only. |
| no_kiln_type | warning | PASS. "High-fired" only; no kiln type named. |
| no_light_exposure_patina | warning | PASS. Patina drivers are use, time, and wear only. |
| no_unsold_products | critical | PASS. No Saltillo. Marble excluded (not on the live outdoor collection page). No porcelain or competitor materials named. |
| overage_rate_correct | critical | PASS. "15-20%" + "25%" present in overage FAQ; no 10-15% pattern anywhere. |
| prop65_link_required | critical | N/A — no Prop 65 mention in the piece (blog format; no product-page installation section). Gate cannot trip. |
| phone_present_with_email | critical | PASS. info@ziatile.com + 310-844-1170 appear together in all three locations (closing, sealing FAQ, overage FAQ). |
| colorway_verified | critical | PASS with note. Cotto: Adobe, Fired Earth, Red Clay, Blanco, Madera, Oscura (config allowed list). Cantera: Sierra only (config list + live page; 7-vs-8 open question avoided). Zellige: Pure White and Tidepool sourced from the live outdoor collection page (2026-07-02 fetch) since the config colorway list is gated `verify` — flagged below. Cotto Allende: v1 named Sayulita/Arroyo/Pedregal (config-listed); final describes the range instead per Jamie's "describe colorway range, don't list names" blog rule. |
| production_step_verified | critical | FIXED. v1 opening applied "hand-dipped" to both glazed lines; hand-dipping is verified for zellige only, Cotto Allende is "hand-glazed" (§5.4). Final: "hand-glazed color." Zellige uses verified verbs (hand-shaped, hand-dipped in glaze); no "chiseled." Cotto: hand-pressed, sun-dried, high-fired (§5.1). Cement: pressed hydraulically, cured rather than fired (config). |

## 4. Required-presence rules

| Rule | Result |
|---|---|
| contact_block | PASS. Email + phone together in closing and in installation-adjacent (sealing) and overage FAQs, using contact-block.md approved phrasings. |
| person_consistency | PASS. First person plural ("our Cotto") held throughout. Zero second-person hits (grep: you/your/yours/yourself). "At Zia" appears only in headings per the §6.7 skeleton. Imperatives limited to approved contact/overage/sealing phrasings. |

## 5. Hard rules from the assignment

| Rule | Result |
|---|---|
| No em dashes | PASS (grep for both em dash and double hyphen: zero). |
| No second person | PASS. |
| No invention | PASS after fixes 1-3 below. Every format, colorway, and suitability claim traces to a config, STYLE-SYSTEM §5/§11, or the live outdoor page (see §7 audit table). |
| Contact line placement | PASS (closing + installation FAQ + overage FAQ). |
| Installation Guide link, descriptive anchor | PASS ("tile installation guides" in Garden Paths section). |
| Internal links | 2 total (outdoor collection, installation guides); within 2-3; no paragraph opens with a link. |
| 15-20% + 25% | PASS. |
| No Saltillo / no name-drops / no fragments / no report labels / no meta-setup openers | PASS. One-word FAQ answers avoided; all answers open with a complete direct-answer sentence. |
| No "withstands"/negative framing | PASS. Grep for withstand/endure/protect/resist/overcome: zero. Limitations phrased as "is not suitable for..." per the mandated form. |
| Word count 1,500-2,000 | PASS (~1,780 body words in v1; ~1,760 in final). |
| Meta title <60 | PASS (58 chars). |
| Meta description 140-160 + keyword + 2 use cases | PASS (155 chars; patios, pool decks, garden paths). |
| Keyword placement | "Outdoor patio tile" opens the first body sentence; variant in H2 "Outdoor Patio Tile at Zia." Secondary keywords open their sections ("Pool tile divides into two decisions," "Garden tile rewards pattern at a small scale"). |

## 6. Issues found in v1 and fixed in final (9 total)

**Technical accuracy (2):**
1. Opening called Cotto Allende's color "hand-dipped" — verified only for zellige. Fixed to "hand-glazed" (production_step_verified).
2. Exclusivity overclaims: "Six of our collections travel outdoors," "unglazed Cotto is the outdoor material," "among all six lines." The live outdoor page also lists Ceramics (all-weather), Terra Forms, and Terrazzo, so exclusive framing was factually wrong. Reworded to non-exclusive framing ("Our outdoor range spans clay and stone," "among these lines").

**Voice / claim precision (7):**
3. "Eighteen-colorway range covering everything from pale neutrals to deep glazes" — unverified color characterization. Replaced with config-verified matte-to-glossy + geography/flora framing; also dropped the Sayulita/Arroyo/Pedregal name list per Jamie's blog rule (describe the range, don't list names).
4. "The mark of a stone floor that has been walked for years" — awkward construction. Now "a record of the years it spends underfoot."
5. "And that rule holds no matter the exposure" — emphasis beyond what the config states. Cut.
6. "Like the other stone lines, Cantera..." — forward reference to a section not yet read. Cut to a plain statement.
7. FAQ pool answer "a deck material rather than a pool interior" — mismatched comparison. Now "belongs on the deck rather than inside the pool."
8. Cement "one flat plane of pigment at a time" — opaque. Replaced with config-grounded pressed-pigment sentence.
9. Word-audit repetition: "68" stated twice, "field" 4x, "palette" 3x, "sets/brings" clusters, "asks for" twice, "mild-climate patio" twice in one paragraph. Varied throughout.

## 7. Claim-by-claim suitability audit (final)

| Claim in article | Config source |
|---|---|
| Cotto suits exterior use in any climate, including freeze/thaw | materials/cotto.md `freeze_thaw: suitable`; STYLE-SYSTEM §4.1 |
| Cotto not for pools/spas (full submersion); approved FAQ wording used | materials/cotto.md `pools_spas: not_suitable`; §4.2, §8.3 |
| Cotto six colorways: Adobe, Fired Earth, Red Clay, Blanco, Madera, Oscura | materials/cotto.md allowed_colorways; §5.2 |
| Cotto formats: 13x13 square, Big Alcazar 13x13 arrowhead/geometric star, Hexagon 8x9, Stars & Cross 6x6 (Granada to Puebla), Alcazar 6x6 | §5.3; Adobe Hex confirmed on live outdoor page |
| Patina: "Use and time deepen the tone"; "deepens with wear" | §6.5 approved wording; §3.2 |
| "Glazed Cotto Allende is ideal for wet spaces, including pools" | Jamie's exact wording, §4.2; materials/cotto-allende.md `pools_spas: suitable` |
| Cotto Allende not suitable for outdoor freeze/thaw | materials/cotto-allende.md `freeze_thaw: not_suitable`; §4.1 |
| Cotto Allende: eighteen colorways (written out), geography/flora names, 4 shapes (4x4, 4x8, triangle, 1.5x8 mini bar), matte-to-glossy with speckling | §5.4 |
| CA/pool FAQ: "approved for pools and spas, but should not be installed outdoors in freeze/thaw climates" | §8.3 approved wording verbatim |
| Zellige approved for pools and spas | materials/zellige.md `pools_spas: suitable` (v3 Quick Reference, live-chart precedence) |
| Zellige in Moroccan fountains and pools for centuries | Live outdoor collection page (2026-07-02) |
| Zellige not suitable for outdoor freeze/thaw, stated plainly in body prose | materials/zellige.md `freeze_thaw: not_suitable`; §4.1 |
| Zellige chips/pits/crazing trio + dynamic glazes (zellige only) | materials/zellige.md variation rules; §3.1 |
| Zellige colorways Pure White, Tidepool | Live outdoor page (config list gated `verify` — flagged) |
| Cement: Vietnam, 19th-c method, pigment pressed hydraulically, never fired, matte, 68 colors | materials/cement.md; §11 |
| Cement exterior non-freeze/thaw only; no pool claim | materials/cement.md `freeze_thaw: not_suitable`, `pools_spas: verify` |
| Cairo White Black (cement) in outdoor collection | Live outdoor page |
| Cantera: volcanic stone, Mexico, visible aggregate + mineral inclusions | materials/cantera.md |
| Cantera: interiors plus non-freeze/thaw exteriors; not pools/spas | materials/cantera.md `freeze_thaw: not_suitable`, `pools_spas: not_suitable` (2026-05-25 reconciliation — stricter than STYLE-SYSTEM §11 and stricter than the task prompt; config wins) |
| Cantera Sierra 12x24 | Config colorway list + live outdoor page |
| Limestone: Fez + Bordeaux, solid blocks, honed or bush-hammered, natural patina | materials/limestone.md; §11 |
| Limestone: non-freeze/thaw exteriors only; not pools/spas | materials/limestone.md (2026-05-25 reconciliation) |
| Cotto DCOF 0.98 vs 0.42 threshold; 1/8" grout joints + anti-slip for wet commercial floors | materials/cotto.md slip resistance; §4.4 |
| Sealing applies in all installations incl. dry spaces; Cotto/CA separate; guide referral | §4.3; both material configs |
| "Always seal Cotto according to our installation instructions..." | §4.3 approved dry-space wording verbatim |
| Samples ship from Los Angeles within two business days | §11.1 |
| 15-20% overage for curation and cuts; 25% for uniform/specialty | §8.4, §9; COMPLIANCE pattern_require |
| Marble excluded | Not on live outdoor collection page (task instruction) |

## 8. STYLE-SYSTEM §12 checklist

- Voice & tone: warm leads anchored in place (San Miguel de Allende, Fez, Granada-to-Puebla) and sensory detail (glazes shifting with light, patina underfoot); no clichés; no fragments; no sentence-ending prepositions found on read-through; no negative framing; no meta sentences or report labels. ✓
- Terminology: "each" not "every"; "Our Cotto/our Sierra" anchoring; trio for zellige only; "terra cotta" lowercase as material, Cotto/Cotto Allende capitalized; "eighteen" written out; no banned terms. ✓
- Technical accuracy: all §4.1/§4.2 rules verified per material (see §7 table); no kiln type; no light-exposure patina. ✓
- Blog: opens with material/place/design decision + keyword in first sentence; collections named in first two paragraphs; first person held; each section a new angle; proper conclusion (practical aside closer, not a CTA). ✓
- SEO: exact keyword first sentence + H2 variant; paragraphs 2-4 sentences, varied; direct answer opens each section; meta title/description compliant. ✓

## 9. Flagged uncertainties (carried into brief + final sign-off)

1. **Ceramics** appears on the live outdoor page as all-weather and pool-recommended, but has no verified material config → omitted from the article entirely. Recommend creating materials/ceramics.md before any outdoor piece includes it.
2. **Zellige colorway names** (Pure White, Tidepool) rest on the live outdoor page fetch, since the config colorway list is gated `verify`. Low risk (live-site precedence), but worth Aleksandra/Emanuel confirmation.
3. **Cement + pools** left unstated per config `verify`.
4. **Cantera** described more narrowly than the task prompt suggested ("indoor + outdoor") because the 2026-05-25 config reconciliation restricts exteriors to non-freeze/thaw. Config followed.
