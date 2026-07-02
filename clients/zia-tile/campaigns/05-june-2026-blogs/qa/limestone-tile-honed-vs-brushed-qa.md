# QA Report — limestone-tile-honed-vs-brushed (v1 → final)

Date: 2026-07-02
Draft audited: `drafts/limestone-tile-honed-vs-brushed-v1.md`
Gates: COMPLIANCE.yml (all banned terms, technical guards, required presence), STYLE-SYSTEM §12 (Voice, Terminology, Technical, Blog, SEO), materials/limestone.md, campaign hard rules.

## Method

Mechanical pass: scripted exact-match scan of every COMPLIANCE.yml banned term, voice ban, and pattern rule, plus second person, em/en dashes, sentence-ending prepositions, "every" for tiles, zellige-language bleed, light/UV patina, contact-block presence, overage rates, links, and meta lengths. Editorial pass: manual read against §12 and the material config.

## COMPLIANCE.yml results (v1)

| Check | Result |
|---|---|
| banned_terms (all 16: free shipping, discount, cheap, affordable, returns, peel-and-stick, bestselling, best seller, sources, products, laid, the correct choice, most often specified, most popular, most specified, report-label phrases) | PASS — zero hits |
| voice_bans (luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted, normal, built to, deepens with use) | PASS — zero hits |
| technical_guards: freeze/thaw + pools/spas | PASS — stated affirmatively as not suitable, matching materials/limestone.md (both `not_suitable`) |
| technical_guards: no_light_exposure_patina | PASS — patina tied to wear and time only |
| technical_guards: no_crazing_on_unglazed / zellige bleed | PASS — no chips/pits/crazing, no dynamic glazes; variation language limited to tone, finish, natural stone variation |
| technical_guards: overage_rate_correct | PASS — 15-20% + 25% uniform option; no 10-15% anywhere |
| technical_guards: prop65_link_required | N/A — no Prop 65 reference in the piece (blog has no installation section; installation FAQ routes to the Installation Guide) |
| technical_guards: phone_present_with_email | PASS — email and phone appear together in all 3 locations |
| technical_guards: colorway_verified | **FAIL in v1 — see Critical #2** |
| technical_guards: no_unsold_products | PASS — no Saltillo, no unsold materials; "brushed" handled as a search term mapped to bush-hammered, never asserted as a Zia finish |
| required_presence: contact_block | PASS — closing + quantity/overage FAQ + installation FAQ |
| required_presence: person_consistency | PASS — first person ("our") held; zero second person |

## Violations found in v1 and fixed in final

### Critical (3)

1. **Meta-setup sentence** (intro, para 2): "The pages that follow the finish decision... make up the rest of this guide." Banned pattern (§2.3, §3.2 — meta sentences announcing what the piece will do). **Fix:** replaced with a verified sample-logistics sentence (ships from LA within 2 business days, STYLE-SYSTEM §11.1).
2. **Invented colorway descriptions** (What Is section): Buff described as "light, sanded warmth," Monument as "deeper grey," Basilica as "soft mid-range." Tone descriptions not verifiable from the live page or config — invention (CLAUDE.md hard gate 4, COMPLIANCE colorway_verified). **Fix:** colorway names retained (verified on live collection page), all invented tone descriptions removed.
3. **§4.3 dry-space sealing wording incomplete** (Bathrooms section): "Always seal limestone" appeared without "according to our installation instructions." **Fix:** exact required wording restored, adapted for limestone (see flag #3 below).

### Major (4)

4. **Meta description 164 chars** (over the 140-160 ceiling). **Fix:** trimmed to 157 chars, keyword + 3 use cases retained.
5. **"wear and time" repeated 3x** (§6.3 word audit). **Fix:** Exteriors instance cut; 2 remain, in separate sections.
6. **Contradictory sentence** (comparison intro): texture "carries the marks of daily traffic without showing them." **Fix:** rewritten as "folds daily wear into the surface."
7. **Subject-verb mismatch** (bush-hammered H3): "A search... and our Bush Hammered listings answer the same design intent, a matte stone surface..." **Fix:** rewritten with "point to the same design intent:" construction.

### Minor (4)

8. **Generic lifestyle framing**: "the settled look of a floor that has been in place for generations" sits in the register Jamie flags on openers. **Fix:** "a floor decades into its life."
9. **Format list repeated** in intro and What Is section. **Fix:** intro list shortened; full verified list kept once.
10. **Colorway names repeated** in intro and What Is section. **Fix:** named once, in the intro (§6.2 early-collection rule satisfied there).
11. **Word-frequency**: "matte" 6x / "even" 2x in one section / "texture" 3x in one H3. **Fix:** varied ("a smooth field," "visible relief," "a different route to a similar surface"); no descriptor now exceeds 2 per section.

## Hard-rule verification (final)

- Second person: 0 instances. Em dashes: 0. En dashes: 0. Fragments: none found. Sentence-ending prepositions: none found.
- H1 contains primary keyword; exact "limestone tile" is in the first sentence of body copy; keyword variant in two H2s ("Honed vs. Brushed Limestone Tile," "How to Care for Limestone Tile"); "limestone flooring" secondary in one H2.
- Internal links: 2 (collection page in body, installation guides in care section). No paragraph opens with a link. Installation Guide linked with descriptive anchor.
- Contact line (info@ziatile.com + 310-844-1170 together): closing, quantity/overage FAQ, installation FAQ.
- Word count: ~1,660 (target 1,500-2,000). Meta title 56 chars. Meta description 157 chars.
- FAQ: 7 questions from SERP research, one direct-answer paragraph each.
- Patina: wear and time only. No pools/freeze-thaw claims beyond the config. No "set"/"laid" errors ("set in offset rows" uses the correct verb).

## Flagged uncertainties (not blocking, for reviewer awareness)

1. **Live page lists finishes beyond the config.** The fetched collection page shows Antiqued Polished and Heathered in addition to Honed and Bush Hammered. materials/limestone.md and STYLE-SYSTEM §11 verify only honed and bush-hammered, so the article asserts only those two. If the extra finishes are real catalog additions, the material config needs an update.
2. **Belgian Bluestone and French Cobblestone** appear on the live collection page but are omitted from the article: their origin is unverified and Belgian sourcing would conflict with the Fez/Bordeaux origin statement in the config. Confirm with Alex before referencing.
3. **§4.3 sealing template adapted.** The required dry-space wording ends "...such as pools, spas, and showers." Limestone is not pool/spa suitable, so the article uses "...such as showers" to avoid implying pool suitability. Deliberate deviation; flag for Jamie/Alex sign-off.
4. **Resealing cadence** (water-bead test, high-traffic rooms resealing sooner) is industry-consensus care guidance from SERP sources, not from Zia's Installation Guide. Framed as a test rather than a Zia spec; verify against the actual guide if possible.
5. **Capitalization**: live listings show "Bush Hammered"; STYLE-SYSTEM writes "bush-hammered." Prose uses the lowercase hyphenated form; the capitalized form appears once, referring to the listings themselves.
6. **Colorway structure**: the live page listing shows Buff, Monument, and Basilica as names in the collection; whether they are colorways of French Limestone specifically could not be confirmed from the fetch. The article names them as tones in the collection without asserting the relationship.
