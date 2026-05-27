# `_approved/` — Living reference library

Client-approved exemplars per content type. The QA agents (`voice-judge`, `koray-judge`, `claims-grounding`) cross-check generated drafts against the exemplars in this folder. When a piece passes Jamie + Aleksandra editorial review, drop the final approved version here so the next batch has a higher floor.

## Structure

```
_approved/
├── blog/             # client-approved blog posts (Andresa's domain)
├── product/          # client-approved product / SKU pages
└── collection/       # client-approved collection pages
```

Each subfolder contains the canonical files only — one approved exemplar per material or topic.

## Naming

`{material}-{slug}.{ext}` — e.g. `cotto-allende-romance-paragraph.md`, `zellige-installation-and-finishing.html`, `terrazzo-collection-page.md`.

Use `.html` once a piece has been rendered to its final delivery format (per the HTML-direct decision from 2026-05-27). Until then, `.md` is fine — promote the `.html` version when the GDrive export step is wired.

## How agents use it

- **`voice-judge`** — when scoring a fresh draft for voice register, samples 1-2 approved files of the same content-type as the calibration band. If the new draft reads further from the approved register than the approved files read from each other, that's a flag.
- **`koray-judge`** — same pattern for semantic SEO structure.
- **`claims-grounding`** — when a borderline factual claim appears in a fresh draft, checks whether the same claim appears verbatim in an approved file. If yes, the claim is grounded by prior approval; surface the source. If no, the standard grounding rules apply.

Agents must NOT copy-paste from approved files. The point is calibration, not reuse. A draft that closely mirrors an approved exemplar fails the originality check.

## What to add and when

| When | Add | Why |
|---|---|---|
| Jamie signs off a blog post | `blog/{material}-{topic-slug}.md` (or `.html` once rendered) | Andresa's calibration set |
| Aleksandra approves a product page after Emanuel's run | `product/{material}-{sku}.md` | Locks the §8.5 spine for that material |
| A collection page closes review | `collection/{material}-collection.md` | Calibrates `/draft-collection-page` |

## What NOT to add

- Drafts in flight. Approved means human-approved, not gate-passed.
- Pieces that needed major edits after gate-pass. The approved version is what shipped, not what the pipeline produced.
- Anything from the v3 audit drafts — those live in `campaigns/01-product-collection-pages/drafts/v3/`. Move into `_approved/` only after Jamie's published-site sign-off.

## Provenance

Every file in `_approved/` should include a leading HTML comment or YAML frontmatter line:

```
<!-- approved: 2026-05-27 by Jamie Greenspan; source: campaigns/01-product-collection-pages/runs/collection-cotto-allende -->
```

This is the chain of custody — agents and humans alike can trust the file because the approval trail is in the file.
