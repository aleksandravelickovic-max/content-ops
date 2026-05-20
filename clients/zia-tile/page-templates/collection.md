# Collection page template — Zia Tile

Skeleton for a material/category collection page. Load the matching `materials/{material}.md` before writing. The golden reference is `campaigns/02-march-april-updates/drafts/collection-cotto.md`, and a verified pipeline example is `campaigns/01-product-collection-pages/runs/collection-cotto-allende/draft.md`.

Collection pages are SHORTER than product pages. They do NOT use the nine-section product spine. The approved structure is: frontmatter, H1, an "Our Take on [Material]" opener, a `[PRODUCT LIST]` placeholder (the grid renders dynamically), then an FAQ block. Product/SKU pages use the full nine sections (see `product.md`).

---

## Frontmatter (match the golden reference)

```
---
url: https://ziatile.com/collections/{slug}
meta_title: "{...} | Zia Tile"
meta_description: "{140-160 chars, primary keyword + >=2 use cases}"
keywords: [...]
person: first | third   # then HOLD it for the whole page
source: {STYLE-SYSTEM sections + material config used}
---
```

## 1. H1
The collection name (e.g., `# Cotto Allende`). Capitalization must match ziatile.com exactly (§7.4).

## 2. Opening copy — "Our Take on [Material]" (§7.1)
- Establish what the material is, where it comes from, and what makes it distinctive, in Zia's voice.
- Two short paragraphs is the norm: (1) what it is + origin + the defining detail, (2) the range (colorways/shapes/finishes) + the key application or care fact per the material config.
- Lead with the material/place, not a process sequence (§2.5).
- Do NOT read like a product spec. No "charming," no standalone "wholly unique," no filler closers ("well-suited for any climate, with sealing before and after grouting" — Jamie deleted this).

## 3. `[PRODUCT LIST]`
Literal placeholder. The live page renders the product grid; do not hand-write product cards.

## 4. Frequently Asked Questions (§7.3)
Cover, at minimum:
- Where the material comes from (origin/heritage)
- Colorways, shapes, and formats (grounded in STYLE-SYSTEM / raw — never invented)
- How it is made (material-appropriate; no kiln type per §4.10)
- Care / sealing (per the material's `sealing_profile`; separate Cotto and Cotto Allende, never combined)
- The Cotto vs Cotto Allende distinction with the pool/spa + freeze/thaw rule, where relevant (§8.3 wording)
- A comparison FAQ where useful (e.g., Cotto vs zellige)
- Quantity / overage (15-20% + 20-25%), with the contact line
- Installation, with the contact line and a link to the install guide

FAQ rules:
- First sentence of each answer responds to the question directly (extractable).
- Match the language of Zia's actual installation guides; do not paraphrase from memory.
- Cross-reference every climate/application claim against the material config + PDP usage charts.
- Contact CTA (email + phone) in the overage and installation answers (§4.6).

---

## Repetition guard (§7.2)
Run a word-frequency check before handoff:
- "Charming unglazed pieces add an earthy aesthetic" appeared twice — cut the second.
- "Traditional" twice in the same passage — switch the second use to "classic range."
- Any adjective/descriptor repeated across the page.

## Capitalization (§7.4)
Match ziatile.com exactly: Cotto, Cotto Allende, Adobe, Fired Earth, Red Clay, Blanco, Madera, Oscura capitalized. "terra cotta" lowercase as the general material.

## Pre-submission
Run §12 Pre-Submission Checklist (Collection Pages block). The pipeline gates this via material-guard, terminology-lint, contact-line-check, person-consistency, claims-grounding, voice-judge, koray-judge.
