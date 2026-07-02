# QA — tile-grout-guide (v1 → final)

Checked: COMPLIANCE.yml (all banned_terms, technical_guards, voice_bans, required_presence), STYLE-SYSTEM §12 (Voice & Tone, Terminology, Technical Accuracy, Blog Posts, SEO blocks), universal rules, and the orchestrator hard rules. Date: 2026-07-02.

## COMPLIANCE.yml gates

| Gate | Result |
|---|---|
| banned_terms (free shipping, discount, cheap, affordable, returns, peel-and-stick, bestselling/best seller, sources [attribution], products, laid, the correct choice, most often specified/popular/specified, practical summary labels, "Understanding the differences") | PASS — zero hits |
| cotto_no_pools / cotto_allende_no_freeze_thaw | N/A — Cotto not referenced |
| zellige_no_freeze_thaw | PASS — no outdoor/freeze-thaw claim made for zellige |
| cement_non_freeze_thaw_only | PASS — no exterior-climate claim; "exterior work" mentioned only for sealer finish choice, no freeze/thaw suitability asserted |
| no_combined_cotto_sealing | N/A |
| no_crazing_on_unglazed | PASS — crazing used only in the zellige trio; cement variation described as matte/porous/pattern, no crazing on cement |
| no_kiln_type | PASS — no kiln type named |
| no_light_exposure_patina | PASS — no patina/light claims |
| no_unsold_products (Saltillo etc.) | PASS |
| overage_rate_correct | N/A — quantity does not come up, so no overage figure required; no 10-15% present |
| prop65_link_required | PASS — Proposition 65 mention hyperlinked to https://ziatile.com/proposition-65-warnings |
| phone_present_with_email | PASS — both appear together in closing and in the installation/sealing FAQ |
| colorway_verified | PASS — no colorway names used anywhere (also satisfies Jamie's no-grout-color-names rule) |
| production_step_verified | PASS — "hand-shaped and glaze-dipped" (zellige), "pressed... never fired" (cement); no "chiseled" |
| voice_bans (luxury, sophisticated, charming, beautiful, stunning, gorgeous, exquisite, defects, recessive, muted standalone, normal-variation, built to, deepens with use) | PASS — zero hits |
| contact_block | PASS |
| person_consistency | v1 FAIL in 2 spots — see issue 2 |

## Issues found in v1 (fixed in final)

| # | Type | Severity | Location | Issue | Fix |
|---|---|---|---|---|---|
| 1 | Banned language (universal §2.2 "seamless") | Critical | FAQ "Can zellige be installed without grout?" | "reads as nearly seamless" | Rewrote: "still reads as one continuous surface" |
| 2 | Person consistency (implied second person via imperative mood) | Critical | FAQ "Does grout stain cement tile?" ("seal... work... wipe... reach for") and How to Grout Cement Tile ("never grout the entire floor at once, and wipe excess grout away") | Instruction-mode imperatives address the reader directly | Recast both passages in third person. Retained the two mandated verbatim imperatives: the §4.3 dry-space sealing sentence ("Always seal...") and the approved contact-block phrasing ("Reach out to our team...") |
| 3 | Terminology (§3.1 "each" not "every" for individual tiles) | Warning | Grout Color section | "emphasizing every uneven edge" | Changed to "each uneven edge" |
| 4 | Unverified terminology (no-invention) | Warning | Grout Joints by Material | "encaustic motif" — "encaustic" not a term verified in Zia materials or STYLE-SYSTEM | Changed to "patterned motif" |
| 5 | Accuracy (materials/cement.md) | Warning | Opening paragraph | "pressed from mineral pigment" omits cement from the composition | Changed to "pressed from mineral pigments and cement" |
| 6 | Meta-reference filler (§2.3) | Warning | How to Grout Zellige, closing line | "which is covered below" announces structure instead of delivering content | Removed the clause |
| 7 | Preposition/particle sentence ending (§2.1) | Warning | FAQ "How long does grout take to cure?" | "before the float comes out" | Changed to "before any grouting begins" |
| 8 | Word choice | Warning | Concluding paragraph | "once the room is set" misapplies the installation verb | Changed to "once the tile is set" |

**Counts: 2 critical, 6 warning. All 8 fixed in final.**

## Hard-rule verification (final)

- No second person, no imperatives outside the two mandated verbatim phrasings; first person plural ("our zellige," "our installation guides," "our team") held throughout — PASS
- No em dashes or en dashes anywhere — PASS (grep clean)
- No fragments — PASS (manual read; every sentence carries subject + verb)
- "Grout joints" only; zero instances of "grout spacing" — PASS
- Chips, pits, and crazing appear as the full trio all 3 times, zellige contexts only; "dynamic glazes" zellige-only (1 instance) — PASS
- Cement tile: never fired, matte, porous, sealed before grouting — matches installation-guides/cement.md and materials/cement.md — PASS
- 1/8" minimum grout joints for wet commercial floors + anti-slip treatment after installation — present in body and FAQ — PASS
- No grout or sealer brand names (Mapei/Fila/Miracle/511/Schluter/DITRA all absent); readers directed to the Installation Guide — PASS
- No specific grout color names (buff, warm grey, bright white, etc.); color handled as match-vs-contrast approach with visual outcomes — PASS
- Internal links: exactly 3 content links (installation-guides, zellige collection, cement-tile collection) + required Prop 65 compliance link; all mid-paragraph with descriptive anchors; no paragraph opens with a link — PASS
- No name-drops, no bestseller framing, no negative tile-attribute framing ("protects against/withstands/endures" absent; "grout protects the tile edges" is the guide's own functional grout claim, not tile-attribute framing) — PASS
- All grout instructions trace to installation-guides/zellige.md, installation-guides/cement.md, materials/*.md, or STYLE-SYSTEM §4.4; general sanded/unsanded/epoxy characteristics are industry-standard definitions per SERP research (flagged in brief), with the guides' specification stated as outranking them — PASS

## SEO checks (final)

- H1 contains primary keyword variant ("Tile Grout Guide") — PASS
- Exact "tile grout" in first sentence of body — PASS
- Keyword in H2s: "What Tile Grout Does," "Tile Grout FAQ"; secondary "grout for zellige" opens the How to Grout Zellige section — PASS
- Meta title 55 chars (<60) — PASS
- Meta description 157 chars (140–160), includes "tile grout" + use cases (shower walls, kitchen backsplashes, floors) — PASS
- Body word count 1,632 (target 1,500–2,000) — PASS
- Paragraphs 2–4 sentences, varied length; direct answer opens each H2 and each FAQ answer — PASS
- Proper concluding paragraph ends with the contact line — PASS

## Flagged uncertainties

1. **Live-site ground truth:** ziatile.com/pages/installation-guides is an index page with no grout content; the per-material guide pages were not individually fetched. Repo guides treated as authoritative per instructions. If the live zellige/cement guide pages have diverged from the repo copies, the figures (1/16", 1/8", 48-hour cures, soak times) should be spot-checked before publish.
2. **Repo zellige guide internally uses "grout spacing" and "laid"** (installation-guides/zellige.md lines 74–78). The article uses the compliant terms (grout joints, set); flagging the guide file itself as a candidate for the same terminology cleanup.
3. **"A lighter, neutral joint leans traditional"** (cement color section) comes directly from the cement installation guide's grout-color note. "Neutral" is an approach descriptor, not a swatch name, so it is treated as compliant with Jamie's §3.2 rule; flag for Jamie if stricter reading is preferred.
4. **Epoxy grout paragraph** is general industry knowledge (SERP-verified), not Zia guidance; it is framed descriptively and subordinated to the installation guides' specification.
