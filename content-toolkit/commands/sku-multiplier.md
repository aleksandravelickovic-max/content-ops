---
description: Generate multiple SKU product pages from one approved category collection page, inheriting the usage chart and varying only colorway/format details.
argument-hint: <client-slug> <material> <campaign-path> [--skus "name:format, name:format, ..."]
model: opus
---

Multiply one approved category page into many SKU pages. This is the scale lever for Zia's 200 PDPs/month. Each SKU page inherits the category usage chart verbatim and varies only SKU-specific details. Follow `CLAUDE.md`.

## Client context protocol (mandatory)

1. **Identify** client, material, campaign from `$ARGUMENTS`.
2. **Read:**
   - `clients/{client}/STYLE-SYSTEM.md`
   - `clients/{client}/materials/{material}.md`
   - `clients/{client}/page-templates/product.md`
   - The approved category collection page for this material (the source of the usage chart).
   - `clients/{client}/raw/` for SKU-specific facts (colorways, formats, dimensions).
   - `clients/{client}/contact-block.md`

## SKU list

- If `--skus` is provided, use that list (`colorway:format` pairs).
- Otherwise, derive the SKU list from the material's colorways and formats in STYLE-SYSTEM.md / raw/ (e.g., Cotto §5.2 colorways x §5.3 shapes). If the catalog is ambiguous, list the SKUs you intend to generate and ask before proceeding (do not invent SKUs).

## Critical rule: category usage chart is inherited, not rewritten (§4.7)

Every generated SKU page reuses the exact category usage chart (structure, wording, bullet order). Only these vary per SKU:
- Romance paragraph (colorway/format specific)
- Format dimensions and orientation
- Finish-specific notes
- Variation FAQ specifics (within the material's variation language)
- Meta title/description (per SKU name + format)

If two SKUs would produce identical usage charts with different freeze/thaw or pool rules, that is a material error: stop and recheck the material config.

## Process

For each SKU:
1. Generate the page via `/draft-product-page` logic, inheriting the category chart.
2. Run the mechanical enforcers inline (material-guard, terminology-lint, contact-line-check, person-consistency).
3. Write to `{campaign-path}/drafts/product-{colorway}-{format}.md`.
4. Record pass/fail per SKU.

After all SKUs:
- Write a `MULTIPLIER-SUMMARY.md` listing each SKU, its file, gate status, and any verify-with-Alex items.

## Velocity breaker

Generate at most 5 SKUs per batch. For larger sets, generate 5, write the summary, and tell the user to re-run for the next batch (mirrors the enterprise `sseo` rate pattern). This keeps review tractable and avoids runaway generation.

## Output format

```
## SKU multiplier: {material} — {N} SKUs generated

| SKU | File | material-guard | terminology | contact | person |
|---|---|---|---|---|---|
| {colorway} {format} | drafts/product-...md | PASS | PASS | PASS | PASS |
| ...

### Verify-with-Alex (shared across SKUs)
- {material verify-confidence items, or None}

### Next
- Review against the category page. Re-run for the next batch of 5 if more SKUs remain.
```

## Constraints

- Inherit the usage chart. Never write per-SKU charts from scratch.
- Do not invent colorways, formats, or dimensions not in STYLE-SYSTEM.md or raw/.
- Max 5 SKUs per run.
- Do not use em dashes.
