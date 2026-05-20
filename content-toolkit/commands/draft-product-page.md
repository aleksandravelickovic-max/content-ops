---
description: Draft a single-SKU Zia product page from the approved 9-section template, inheriting the category usage chart and grounded in the material config.
argument-hint: <client-slug> <material> <sku-name> <format> [campaign-path]
---

Draft a product (SKU) page following `CLAUDE.md`, the client's product template, and the category-level usage chart. The output is a finished product page, not an analysis.

## Client context protocol (mandatory — execute before drafting)

1. **Identify client, material, SKU, and format** from `$ARGUMENTS`.
2. **Read, in this order:**
   - `clients/{client}/STYLE-SYSTEM.md`
   - `universal-rules/UNIVERSAL-RULES.md`
   - `clients/{client}/materials/{material}.md` — hard rules.
   - `clients/{client}/page-templates/product.md` — the 9-section spine (§8.5).
   - `clients/{client}/contact-block.md`
   - The golden reference if it exists: `clients/{client}/campaigns/02-march-april-updates/drafts/product-red-clay-8x8.md`.
   - The category collection page for this material, if one exists, to inherit the approved usage chart.
3. **Read SKU-specific source** in `clients/{client}/raw/` (colorway, dimensions, finish). Do not invent SKU facts.

## Critical rule: usage charts are category-level (§4.7)

Do NOT write usage bullets from scratch per SKU. Inherit the approved category usage chart for this material (from the collection page or the category template). Substitute only SKU-specific details: format dimensions, orientation, finish-specific notes. Structure, wording, and bullet order must be identical across all SKUs in the same category.

## Input

`$ARGUMENTS`: `<client-slug> <material> <sku-name> <format> [campaign-path]`.

## Drafting rules

- Produce all nine sections in the exact §8.5 order.
- Romance paragraph (section 1): tight, specific, leads with what makes THIS colorway/format distinctive. Correct adjective order (§8.1).
- Variation FAQ uses material-appropriate language (trio for zellige; tone/shape/edge/thickness for Cotto). Never cross materials.
- Inline sealing + slip-resistance spec inside the correct usage bullets only (§4.8 placement accuracy).
- Contact block in closing + overage FAQ + installation FAQ.
- Meta: title `[Product Name] [Format] | Zia Tile` (50-60 chars); description 140-160 chars with primary keyword + >=2 use cases (§10.3).
- No invention, no em dashes, no second person, one person held throughout.

## Self-check before returning (mandatory)

1. **material-guard logic**: all technical claims match `materials/{material}.md`.
2. **Usage chart parity**: chart matches the category template, only SKU details substituted.
3. **terminology-lint logic**: clean §3.1/§3.2.
4. **contact-line logic**: email + phone in closing + overage + installation FAQ.
5. **person-consistency logic**: one person, no second person.
6. **Nine sections present, in order.**

## Output format

```
Flags:
- {missing inputs or "None"}

{the full product page draft, 9 sections in order, with meta block at top or bottom}

---
## Self-check
- material-guard: {PASS | fixed}
- usage-chart parity: {PASS}
- terminology-lint: {PASS | fixed}
- contact-line: {PASS}
- person-consistency: {PASS}
- nine-sections: {PASS}
- Verify-with-Alex: {list or "None"}
```

## Constraints

- Finished page only. No outline, no process language.
- If the category usage chart cannot be located, ask for it (per §4.7, templates are maintained by Alex) rather than inventing one.
