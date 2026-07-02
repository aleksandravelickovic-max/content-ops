# Brief: Outdoor Tile for Patios, Pool Decks and Gardens

- **Slug:** outdoor-tile-patios-pool-decks-gardens
- **Type:** Multi-material application guide (STYLE-SYSTEM §6.7 design-ideas skeleton)
- **Primary keyword:** outdoor patio tile (9.9K) — exact match in H1 context, first sentence of body, and at least one H2/H3
- **Secondary keywords:** pool tile (5K), garden tile
- **Search intent:** Buyer researching which tile materials work outdoors, by climate and application (patio, pool, garden)
- **Target URL to link:** https://ziatile.com/pages/outdoor-collection
- **Also link:** https://ziatile.com/pages/installation-guides (descriptive anchor). 2-3 internal links total.
- **Word count:** 1,500-2,000
- **Person:** First person plural ("our Cotto"), held throughout. No second person anywhere.
- **Meta title (<60 chars):** Outdoor Tile for Patios, Pool Decks and Gardens | Zia Tile (58)
- **Meta description (140-160 chars):** Outdoor patio tile guide from Zia Tile: which handmade materials suit patios, pool decks, and garden paths, from freeze/thaw Cotto to glazed Cotto Allende. (155)

---

## Live-site check (2026-07-02)

Fetched https://ziatile.com/pages/outdoor-collection. Findings:

- **Non-freeze/thaw outdoor group:** Cantera, Cement, Ceramics, Cotto, Cotto Allende, Limestone, Terra Forms, Terrazzo, Zellige
- **All-weather group:** Ceramics, Cotto
- **Pool recommendations on page:** glazed Zellige ("used in fountains and pools in Morocco for centuries"), Cotto Allende, Ceramics
- **Named tiles on page:** Cairo White Black (Cement), Pure White 2x6 and 2x2 (Zellige), Casablanca (Zellige), Unglazed Natural 2x2 and 2x6 (Zellige), Glazed Earth (Zellige), Sierra 12x24 (Cantera), Adobe Hex (Cotto), Racing Green 4x4 and 2x2 (Zellige), Tidepool 2x2 and 2x6 (Zellige)
- **Marble is NOT on the outdoor collection page** → excluded from the article per instruction.
- **Ceramics, Terra Forms, Terrazzo** appear on the page but have no material config in this task's verified set → excluded from suitability claims; flagged as a coverage gap below.
- **Unglazed Natural zellige** appears on the page, but unglazed zellige is a separate gated category (STYLE-SYSTEM §4.9) → not referenced in the article.

## Verified material/climate matrix (config sources)

| Material | Exterior freeze/thaw | Exterior non-freeze/thaw | Pools/spas (submersion) | Source |
|---|---|---|---|---|
| Cotto (unglazed) | Suitable — any climate, a selling point | Suitable | NOT suitable (full submersion) | materials/cotto.md (freeze_thaw: suitable; pools_spas: not_suitable); STYLE-SYSTEM §4.1, §4.2 |
| Cotto Allende (glazed) | NOT suitable | Suitable | Approved. Jamie framing: "Glazed Cotto Allende is ideal for wet spaces, including pools." | materials/cotto-allende.md (freeze_thaw: not_suitable; pools_spas: suitable); §4.1, §4.2 |
| Zellige (glazed) | NOT suitable — state plainly and affirmatively in body prose | Suitable | Suitable (glazed only) | materials/zellige.md (freeze_thaw: not_suitable; pools_spas: suitable); §4.1, §11 |
| Cement | NOT suitable | Suitable (non-freeze/thaw only) | VERIFY — do not assert either way | materials/cement.md (freeze_thaw: not_suitable; pools_spas: verify); §11 |
| Cantera Stone | NOT suitable (config corrects §11's broad "indoor + outdoor") | Suitable | NOT suitable — do not assert for pools | materials/cantera.md (freeze_thaw: not_suitable; pools_spas: not_suitable, 2026-05-25 reconciliation) |
| Limestone | NOT suitable | Suitable | NOT suitable | materials/limestone.md (freeze_thaw: not_suitable; pools_spas: not_suitable, 2026-05-25 reconciliation) |
| Marble | (excluded — not on outdoor collection page) | — | — | Live-page check 2026-07-02 |

**Note on the task prompt:** the prompt described Cantera as "indoor + outdoor." The config is stricter — non-freeze/thaw exteriors only — and the config wins (2026-05-25 reconciliation against the live Tile Usage chart). The article follows the config.

**Pool deck vs. pool interior:** unglazed Cotto is suited to exterior floors in any climate but not full submersion (approved §8.3 FAQ wording). The article keeps the deck (exterior floor) and the pool interior (submerged) explicitly separate so cotto_no_pools cannot trip.

## Verified formats and colorways to name in context

- **Cotto shapes (§5.3):** 13x13 squares and Big Alcazar (13x13) for open patios; Stars & Cross (6x6) and Alcazar (6x6) for compact courtyards; Hexagon (8x9). Colorways (config allowed list): Adobe, Fired Earth, Red Clay, Blanco, Madera, Oscura. Adobe Hex confirmed on live outdoor page.
- **Cotto Allende (§5.4):** eighteen colorways (write out "eighteen"); assert only the seven config-listed names (Sayulita, Cacao, Creosote, Peyote, Arroyo, Condesa, Pedregal). Four shapes: 4x4 square, 4x8 rectangle, triangle, 1.5x8 mini bar.
- **Zellige colorways:** gated `verify` in config, but the live outdoor page names Pure White, Casablanca, Glazed Earth, Racing Green, Tidepool — live page is an approved source. Use sparingly (Pure White, Tidepool).
- **Cantera:** Sierra 12x24 (appears in both the config colorway list and the live outdoor page). Do not enumerate the full colorway set (7 vs 8 open question).
- **Cement:** 68 colors (§11); Cairo White Black on live page. Never fired, matte.
- **Limestone:** honed or bush-hammered finish; Fez, Morocco and Bordeaux, France (§11).

## SERP research (2026-07-02)

Reviewed top organic results for "outdoor patio tile" and "pool deck tile": Oasis Tile, Tile Club, RUBI, Edward Martin, OUTERclé, Family Handyman, Mineral Tiles, Daltile, Novoceram, Apollo Tile.

**What the SERP covers:**
- Porcelain-first framing (density, low water absorption, "frost-proof") dominates every guide
- DCOF 0.42+ threshold for wet outdoor surfaces appears repeatedly
- Freeze/thaw mechanics: porous tile absorbs water, freezing water expands and cracks the tile
- Pool decks: matte/textured surfaces, travertine and natural stone, glass for vertical pool walls only
- Generic material lists with no named formats, no origin, no craft narrative

**Coverage gaps (our angle):**
- No handmade or artisanal materials covered at all; the entire SERP is porcelain and commodity stone
- No treatment of glazed vs unglazed terra cotta, or which handmade materials are freeze/thaw capable
- No specific formats, colorways, or layout guidance
- Pool guidance never separates the submerged interior from the surrounding deck
- Sealing guidance is thin or absent

**FAQ candidates (from PAA and SERP patterns):**
1. What makes a tile suitable for outdoor use? (body, firing, porosity, climate)
2. Which tile can be installed outdoors in freeze/thaw climates? (freeze/thaw question — required)
3. What tile is best around a pool? (pool question — required)
4. Can zellige be installed outdoors?
5. Is terra cotta a good patio tile?
6. Do outdoor tiles need to be sealed? (installation FAQ → Installation Guide link + contact line)
7. How much outdoor tile should a project order? (overage FAQ → 15-20% + 25% + contact line)
8. Are outdoor tiles slippery when wet? (Cotto DCOF 0.98; 1/8" grout joints + anti-slip for wet floors)
9. What is the difference between Cotto and Cotto Allende outdoors? (product-difference)
10. Can cement tile go outside? (non-freeze/thaw only)

Final FAQ selects 6: #1, #2, #3, #5, #6, #7 (covers required freeze/thaw + pool + installation + overage; #9's content folds into #2/#3 answers).

## Outline (§6.7 skeleton)

1. **H1 + opening** — design decision (climate first), "outdoor patio tile" in first sentence, name Cotto, Cotto Allende, zellige, cement, Cantera, limestone early; link outdoor collection mid-paragraph
2. **H2 What Makes a Tile Outdoor-Suitable** — body, firing, glaze, and climate; freeze/thaw mechanics stated affirmatively (which materials suit which climates)
3. **H2 Outdoor Tile at Zia** — H3 per material: Cotto / Cotto Allende / Zellige / Cement / Cantera Stone / Limestone; each states suitability affirmatively with verified formats
4. **H2 Patios** — Cotto 13x13 + Big Alcazar for open patios; cement + limestone for mild climates
5. **H2 Pool Decks and Pools** — Cotto Allende (Jamie framing) + glazed zellige for the pool itself; Cotto for the surrounding exterior floor in cold climates; slip resistance (DCOF 0.98, 1/8" grout joints, anti-slip)
6. **H2 Garden Paths and Courtyards** — Stars & Cross + Alcazar, Spanish courtyard; Cantera Sierra; bush-hammered limestone
7. **H2 Matching Material to Climate** — the trade-off section; prose recap of the matrix
8. **H2 recap/closing** — ties materials together + contact line (info@ziatile.com + 310-844-1170)
9. **H2 FAQ** — 6 questions above, one direct-answer paragraph each

## Hard-rule reminders for the draft

- No second person; first person plural held throughout
- No em dashes anywhere
- No "withstands," "endures," "protects against," "resists" — positive framing only; glazed materials get "is not suitable for freeze/thaw climates"
- No "products," "sources" (production attribution), "laid" (use "set"), "built" (aging), "luxury/sophisticated/charming/beautiful/stunning," bestseller framing, fragments, meta-setup openers, report-style labels
- 15-20% overage plus 25% uniform option wherever quantity appears
- No Saltillo, no invention, no Prop 65 mention (avoids the hyperlink gate; blog has no product-page installation section)
- Contact line in closing and in installation + overage FAQ answers

## Flagged uncertainties

- **Ceramics** is on the live outdoor page as all-weather and pool-suitable, but has no verified material config in this task's set → omitted from the article. Worth a follow-up config (ceramics.md) so future outdoor pieces can include it.
- **Cement + pools:** config says `verify` → article makes no pool claim for cement.
- **Cantera colorway count** (7 vs 8) open question → article names only Sierra.
- **Zellige colorway master list** still gated `verify` → article uses only names shown on the live outdoor page.
