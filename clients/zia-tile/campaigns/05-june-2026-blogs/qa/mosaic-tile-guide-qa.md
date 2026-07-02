# QA report — mosaic-tile-guide (v1 → final)

Checked: drafts/mosaic-tile-guide-v1.md, 2026-07-02
Method: grep pass over every COMPLIANCE.yml term/guard/presence rule + manual read against STYLE-SYSTEM §12 (Voice, Terminology, Technical, Blog, SEO) and the campaign hard rules.

## COMPLIANCE.yml — banned terms (exact match)

| Term | Severity | Result |
|---|---|---|
| free shipping | critical | PASS (absent) |
| discount / cheap / affordable / returns / peel-and-stick | critical | PASS |
| bestselling / best seller | warning | PASS |
| sources (production attribution) | critical | PASS (also checked "sourced") |
| products | critical | PASS ("tiles," "collections," "materials" used) |
| laid | warning | PASS ("set" used; "dry layout" noun only) |
| the correct choice | warning | PASS ("a great choice" used once) |
| most often specified / most popular / most specified | warning | PASS |
| The practical summary / Practical summary: | warning | PASS |
| Understanding the differences between | warning | PASS |

## COMPLIANCE.yml — technical guards

| Rule | Result |
|---|---|
| cotto_no_pools | N/A — Cotto not referenced |
| cotto_allende_no_freeze_thaw | N/A |
| zellige_no_freeze_thaw | PASS — stated affirmatively: "not suitable for outdoor installation in freeze/thaw climates" |
| cement_non_freeze_thaw_only | N/A |
| no_combined_cotto_sealing | N/A |
| no_crazing_on_unglazed | PASS — chips/pits/crazing applied to glazed zellige only; Roman Mosaics use veining/tone; glass uses color/sheen/hand-placement |
| no_kiln_type | PASS — no kiln claims |
| no_light_exposure_patina | PASS — no patina/light claims |
| no_unsold_products | PASS — no Saltillo, no unsold materials, no brand/designer name-drops |
| overage_rate_correct | PASS — "15-20%" + "25%" in Samples section and overage FAQ; no 10-15% variant |
| prop65_link_required | PASS by absence — Prop 65 not mentioned (blog carries no Installation section; install questions routed to Installation Guide + contact) |
| phone_present_with_email | PASS — 3 occurrences of info@ziatile.com, each paired with 310-844-1170 in the same block |
| colorway_verified | PASS — all stone/pattern names verified against the live collection page 2026-07-02 (Carrara, Giallo Reale, Rosso Alicante, Verde Alpi, Bardiglio Imperiale, Grigio Carnico, Nero Marquina; 5/8 solids, Ventaglio, Check, Mini Check; Check pairings with Carrara confirmed). No zellige colorways named (gated `verify`). No glass pattern names invented. |
| production_step_verified | PASS — "chiseled" verified from live Roman Mosaics page copy; "hand-placed" from glass config; no zellige production verbs used |

## COMPLIANCE.yml — voice bans

luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted, normal (variation), built to, deepens with use — ALL PASS (absent). Also checked: unique, truly, really, simply, of course, works as, module, sub-line, printed, straightforward, slightly different, shower surround, trim pieces, grout spacing, withstand/protects against/endures/overcomes (negative framing), "today" closer — all absent.

## COMPLIANCE.yml — required presence

| Rule | Result |
|---|---|
| contact_block | PASS — closing (Samples section), installation FAQ, overage FAQ; email + phone together each time |
| person_consistency | PASS — first person ("our") held throughout; zero second-person hits (you/your/yours/yourself). Imperatives limited to approved contact/sealing/overage phrasings. |

## Hard rules (campaign)

| Rule | Result |
|---|---|
| No em dashes | PASS — grep for — / -- returns only the markdown `---` separator after the meta block |
| No second person | PASS |
| No invention | PASS — suitability claims traced to materials/roman-mosaics.md, glass-mosaics.md, zellige.md; product facts to live page + STYLE-SYSTEM §11/§11.1; slip spec to §4.4 |
| Historical anchoring | PASS — "decorative geometric and floral shapes," villa floors and bath houses; no vague heritage language |
| Installation Guide linked, descriptive anchor | PASS — 2 internal links total (target collection + installation guides); no paragraph opens with a link |
| Overage 15-20% + 25% | PASS |
| Prop 65 link | N/A (not mentioned) |
| No fragments | PASS (manual read) |
| No sentence-ending prepositions | PASS (manual read) |
| "each" not "every" | PASS ("every" absent) |
| Meta title | PASS — 59 chars, keyword at front |
| Meta description | PASS — 154 chars, "Mosaic tile" first words + use cases (backsplashes, shower floors, pools) |
| Keyword placement | PASS — exact "mosaic tile" in H1 and first sentence of body; in three H2s |
| Word count | 1,581 body words — within 1,500-2,000 |
| FAQ from SERP | PASS — 8 questions, each a direct-answer paragraph |
| Concluding section + contact line before FAQ | PASS (§6.7 order) |
| §6.3 H3 minimum 3 sentences | PASS — each H3 carries 3+ sentences |
| Semicolons | 0 (§6.7 prose discipline) |

## Violations found in v1 (fixed in final)

| # | Type | Location | Issue | Fix |
|---|---|---|---|---|
| 1 | Voice / AI pattern (rule of three) | "How Designers Use Mosaic Tile" intro | "quieter in texture, denser in grout, more willing to follow a curve" is a tricolon | Restructured into two sentences with varied rhythm |
| 2 | Vague claim (§2.3) | Glass Mosaics section | "Glass travels the furthest of the three materials" delivers no information | Replaced with the capability: fewest placement limits |
| 3 | SEO heading rule | Conclusion H2 | "Samples and Ordering" uses an -ing verb in a heading | Renamed "Samples and Quantities" |
| 4 | Repetition (§6.3 word audit) | Pools section vs FAQ #4 | "the route for submerged marble surfaces" / "the marble route for submerged surfaces" near-duplicate | FAQ wording varied |
| 5 | Repetition (§6.3 word audit) | Shower section vs FAQ #3 | "Mosaic is a great choice for shower floors" verbatim in both | FAQ opener varied ("well suited") |

Counts: 0 critical compliance violations, 0 technical-accuracy violations, 5 editorial/voice/SEO issues (2 voice, 2 repetition, 1 heading) — all fixed in final/mosaic-tile-guide.md.

## Flags for the reviewer

1. **Naming:** the live site did NOT move Roman Mosaics under Marble — https://ziatile.com/collections/roman-mosaics resolves as its own collection (checked 2026-07-02). No fallback needed.
2. **Spelling divergence:** live site spells the green marble **Verde Alpi**; STYLE-SYSTEM §11 Marble row says "Verdi Alpi." Live site used per §7.4 (match capitalization/naming to the live site). STYLE-SYSTEM §11 may need a correction.
3. **Bardiglio Imperiale** appears in the live Roman Mosaics range but not in the §11 Marble stone list; included on live-page authority.
4. **§4.3 exact dry-space sealing wording** uses "our installation instructions" (first person) — piece was set to first person partly so this verbatim string and the person-consistency gate coexist.
5. The approved overage-FAQ contact phrasing in contact-block.md contains "your project" (second person); shortened to "For help estimating quantities, contact..." to hold the no-second-person rule.
