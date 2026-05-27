# Product page template (SKU) — Zia Tile

Skeleton for a single-SKU product page. The **proven, signed-off pattern** is `clients/zia-tile/campaigns/01-product-collection-pages/drafts/product-pages/aegean-4x4.md` (Emanuel, 2026-05-21). Match it. This template summarizes the structure; the aegean SKU is the reference draft.

Load `materials/{material}.md` and `raw/research/materials-reference.md` (Quick Reference matrix) before writing — freeze/thaw, pool/spa, sealing, and variation language are material-specific.

Usage charts are standardized at the category level (§4.7). Do NOT write usage bullets from scratch per SKU. Inherit the approved category usage chart for this material. Substitute only SKU-specific details (format dimensions, orientation, finish notes).

---

## Frontmatter (match Emanuel's pattern)

```yaml
---
sku: {colorway-format-slug}            # e.g. aegean-4x4
material: {material-slug}              # matches materials/{material}.md
url: https://ziatile.com/products/{slug}
title_tag: "{Colorway} {Format} {Material} | Zia Tile"   # 50-60 chars
meta_description: "Shop Zia's {colorway} {format} {material}. {one-line distinct value}. Suited for {2 use cases}."   # 140-160 chars
draft_date: YYYY-MM-DD
---
```

## Body structure (6 H2 sections + top block)

### Top block (before any H2)

```
## {Material}     ← parent material indicator, H2

# {Colorway} {Format}     ← SKU name, H1

[INSERT CART MODULE HERE]

---

{Romance paragraph 1: lead with what makes THIS colorway/format distinctive. Named maker, named color, named format use case. AD register. Avoid "stunning/charming/unique" without context.}

{Romance paragraph 2: how this SKU is made + the material variation language for this material. 2-4 sentences.}

[IMAGE: SIZE/THICKNESS DIAGRAM]

#### Order Details + Installation [Locked]

{Overage: 15-20% standard + 25% for uniform look. Both, in one sentence.}

{Installation specifics for this material: hand-set vs mallet-tap, soaking, grout joint, etc. 1-2 paragraphs.}
```

### ## About

Brief — 2-3 paragraphs. Variation framing + Prop 65 + drywall/mitered/Schluter + sealing direction + contact email. Keep to material-appropriate variation language from `materials/{material}.md`.

### ## Tile Usage

Two sub-sections, both as `###` H3 (uniform hierarchy):
- `### Residential Usage` — 11-row usage chart with the approved bullets for this material's category
- `### Commercial Usage` — same 11 rows, commercial context examples

Both charts use the SAME bullets, only swapping the example context. Pull bullets from the approved category template, not from scratch.

Each row's status (✓/✗) must come straight from `materials/{material}.md` frontmatter + the Materials Reference Guide v3 Quick Reference matrix. material-guard enforces this.

### ## How It's Made

Material-appropriate production narrative. 2-3 paragraphs. No kiln-type assertion without confirmation (§4.10). No light-exposure patina claims.

### ## Order & Shipping

Verbatim copy per §11.2:
- Sample: 2-business-day ship, up to 10 total (max 4 per unique tile), first 5 complimentary, $3 each thereafter.
- Full: "via a third party LTL carrier service. Pallets will be delivered curbside." + "We will ship the entire order together once all tiles are in stock."
- Pickup: free at LA warehouse, by appointment, "Monday through Friday, 8 am–3 pm" (confirm current hours with Alex).
- International / AK / HI: "should email our team at info@ziatile.com for a custom shipping quote."

### ## Installation Guide

```
[KEEP]
```

(The live installation guide is linked; the page reserves space for it.)

### ## Frequently Asked Questions

Minimum 6 questions. Required topics from §8.5 + Emanuel's pattern:
1. The colorway / what color it is
2. Application suitability for the main use case (bathroom / kitchen / pool — material-appropriate)
3. Pool/spa suitability (per material config)
4. Mixing with other colorways in the same collection
5. Variation across orders / batch consistency
6. **Comparison to sibling colorway** — pick the nearest colorway in the same collection and contrast them (Emanuel's aegean → Tidepool comparison is the model)

First sentence of each answer responds to the question directly. Include the contact line (info@ziatile.com + 310-844-1170) in installation-adjacent answers.

---

## Pre-submission

Run §12 Pre-Submission Checklist (Product Pages block). The pipeline gates this via material-guard, terminology-lint, contact-line-check, person-consistency, claims-grounding. Final score via voice-judge + koray-judge (gate ≥80).

## Reference

- Proven SKU draft: `clients/zia-tile/campaigns/01-product-collection-pages/drafts/product-pages/aegean-4x4.md`
- 4 other signed-off SKUs in the same folder: 2x6-rectangle-oscura, 8x9-hex-red-clay, absinthe-2x6-bejmat-zellige, absinthe-trapezoid
- STYLE-SYSTEM.md §8.5 (the 9-section spec these compress into 6 visible H2 sections + top block)
