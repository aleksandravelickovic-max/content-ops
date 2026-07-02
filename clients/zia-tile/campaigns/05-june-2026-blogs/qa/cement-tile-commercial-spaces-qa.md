# QA Report — cement-tile-commercial-spaces-v1.md

Date: 2026-07-02. Checked against: COMPLIANCE.yml (all banned_terms, technical_guards, voice_bans, required_presence), STYLE-SYSTEM §12 (Voice, Terminology, Technical, Blog, SEO), and the hard rules for this piece. Draft body word count: 1,712.

## Gate summary

| Gate | Result |
|---|---|
| Em dashes / en dashes | PASS (0 found) |
| Second person (you/your) | PASS (0 found) |
| COMPLIANCE banned_terms (free shipping, discount, cheap, affordable, returns, peel-and-stick, bestselling, best seller, sources, products, laid, the correct choice, most popular/specified, practical summary, understanding-the-differences opener) | PASS on all except "printed" equivalent list — see V1 |
| COMPLIANCE voice_bans (luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted-standalone, normal, built to, deepens with use) | PASS (0 found) |
| Technical: cement_non_freeze_thaw_only | PASS (FAQ states "non-freeze/thaw climates only" plainly) |
| Technical: never fired / hydraulic press / mineral pigments / matte | PASS (definition section + FAQ) |
| Technical: no glaze/zellige language on cement (no crazing, no dynamic glazes, no chips/pits) | PASS |
| Technical: pools/spas not asserted (materials/cement.md: verify) | PASS (not mentioned) |
| Technical: overage_rate_correct (15-20% + 25%; never 10-15%) | PASS |
| Technical: slip spec (1/8" grout joints + anti-slip treatment, wet areas only; no "consult your installer") | PASS (wet-zones H3 + slip FAQ only) |
| Technical: prop65_link_required | N/A (no Prop 65 mention in piece) |
| required_presence: contact_block (email + phone together in closing + overage FAQ + installation-adjacent FAQ) | PASS (3 paired instances) |
| Internal links (2-3, descriptive anchors, none opening a paragraph) | PASS (collection page x1, installation guides x2) |
| SEO: keyword in H1, exact match in first sentence, in >=1 H2/H3 | PASS |
| Meta title <60 chars / description 140-160 with keyword + 2 use cases | PASS (58 / 144) |
| Word count 1,500-2,000 | PASS |
| "Straightforward" in care sections | PASS (0 found) |
| Fragments | FAIL — see V3 |

## Violations found (fixed in final)

### Critical

- **V1 — Banned term "printed" (§3.2: remove entirely; Jamie flagged as meaningless).** "What Cement Tile Is," para 2: "a depth that printed or glazed alternatives do not carry." Fixed: clause removed, sentence rebuilt around the pigment-layer mechanism.
- **V2 — Person consistency (§6.4, required_presence: person_consistency).** Two third-person "Zia" intrusions in an otherwise first-person piece: "Zia's full range lives in our cement tile collection" (intro) and the link anchor "Zia installation guides" (sealing section). Fixed: both converted to first person ("The full range lives in our..." / "our installation guides").
- **V3 — Fragment (§2.1: complete sentences only).** FAQ 1 opened with standalone "Yes." Fixed: folded into the answer sentence.
- **V4 — Unsold-material reference (COMPLIANCE no_unsold_products, §5.5).** Hospitality section compared cement favorably against "uniform porcelain," a material category framing Zia content should not lean on. Fixed: comparison removed; corridor depth described on its own terms.

### Warnings / style

- **V5 — Negative "X rather than Y" contrast constructions (Jamie's pattern: cut the negative half; §2.2, §2.5).** Five instances: "not glazed over it" (intro), "rather than a coating" (definition), "history rather than fatigue" (why-commercial), "rather than decor" (hospitality), "rather than a maintenance problem" (maintenance). Fixed: negative halves cut; "a starting point, not a forever state" retained as Jamie-approved phrasing.
- **V6 — Endurance/negative framing (§2.6: lead with what the material gives).** "hold up to service" (restaurant intro), "holds up to daily contact better than painted drywall" (retail), "the color and pattern hold through years" (FAQ 1). Fixed: reframed positively ("carries daily service," "keeps its finish through daily contact," "stay true through years").
- **V7 — -ing verb headings (SEO heading rule).** "Planning a Commercial Cement Tile Project" and "Sealing and Maintenance in Commercial Settings." Fixed: "How to Specify Commercial Cement Tile" (also places the primary keyword in a second H2) and "Sealer Schedules and Routine Care in Commercial Settings."
- **V8 — Product anchoring (§3.1: Our [Product] / Zia's [Product]).** Several colorway/pattern lists ran bare (Madrid, Zig Zag, Bone, Sage, Emerald, Delta Moon, Pompeii). Fixed: "our" anchor added to each list's lead name.
- **V9 — Word audit (§6.3).** "for decades" x4, "naturally matte" x3, "sign/signage" x2 across nearby sections. Fixed: varied to two/one/one instances.
- **V10 — Awkward subject "Never fired is the defining distinction."** Fixed: "That never-fired cure is the defining distinction."
- **V11 — Overage FAQ echoed the §8.4 avoided phrasing** ("...during the dry layout process" flexibility rationale). Fixed: 25% option tied to dispersing tone variation instead; "curation and cuts" rationale retained.
- **V12 — Ambiguous pattern names.** "An expanse of Delta Moon or Pompeii" used names whose pattern-vs-colorway role is ambiguous on the live page. Fixed: swapped to Samba and Currents, which appear unambiguously as patterns.

## Counts

- Critical: 4 found, 4 fixed.
- Warning/style: 8 found, 8 fixed.
- Remaining critical violations in final: 0.

## Flagged uncertainties (not blocking)

1. **Color count.** STYLE-SYSTEM §11 states 68 colors; the live collection page does not state a total on-page (roughly 30+ colorways were visible in the fetched listing). The canonical 68 is used. Confirm with Alex if the catalog count has changed.
2. **Origin framing.** The live page credits the technique to "French and Catalan craftspeople of the 1850s" and does not name Vietnam; STYLE-SYSTEM §11 states Vietnam. Both are used together (made in Vietnam, 1850s French/Catalan method) as they are compatible, but the pairing has not been Jamie-reviewed.
3. **Pattern/colorway roles.** Pattern names (Zig Zag, Madrid, Monstera, High Line, Cairo, Sonora, Samba, Currents, Stars & Cross) and colorways (Bone, Sage, Emerald, Everglade, Jaipur Pink, Elemental Blue) are verified present on the live page, but the page listing mixes pattern and colorway naming; roles were assigned conservatively.
4. **Resealing cadence.** SERP consensus is a 1-2 year traffic-based cycle; Zia's own guides were not fetched to confirm a number, so the piece says "a cycle keyed to traffic" and routes to the installation guides rather than asserting an interval.
