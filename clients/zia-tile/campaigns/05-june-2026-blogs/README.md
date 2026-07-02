# Campaign 05 — June 2026 Blogs

**Goal:** Produce the June 2026 blog batch from the LG Team tracker (8 In Progress topics; Marble and Hand-Painted Ceramics skipped as On Hold).

**Status:** Post-editorial QA pass complete — awaiting Emanuel/final delivery review before any delivery.

**Input:** `batches/june-blogs-batch-01.csv` (built from the tracker table, 2026-07-02).

## Structure

- `batches/` — batch CSV + production log
- `briefs/` — one brief per piece, with SERP research and FAQ candidates
- `drafts/` — working markdown, `-v1` suffix
- `qa/` — QA report per piece (COMPLIANCE.yml + STYLE-SYSTEM §12 checklist)
- `qa/post-editorial-batch-qa-2026-07-02.md` — Aleksandra feedback pass covering keyword metadata, FAQ count, overage wording, product-level links, and final mechanical scans
- `final/` — revised, QA-passed markdown, no suffix
- `html/` — rendered HTML exports regenerated from the revised finals

## Target URLs

| Piece | Target |
|---|---|
| Fireplace tile | ziatile.com/collections/zellige + /collections/cement-tile |
| Glass mosaic tile | ziatile.com/collections/glass-mosaics |
| Tile grout guide | ziatile.com/pages/installation-guides |
| Limestone tile | ziatile.com/collections/limestone-tile |
| Mosaic tile | ziatile.com/collections/roman-mosaics (verify live) |
| Commercial cement | ziatile.com/collections/cement-tile |
| Zellige color guide | ziatile.com/collections/zellige |
| Outdoor tile | ziatile.com/pages/outdoor-collection |

## Rules of the run

- Every piece grounded in `clients/zia-tile/STYLE-SYSTEM.md`, `COMPLIANCE.yml`, `page-templates/blog.md`, and the relevant `materials/{material}.md` config.
- Mandatory live-site check of the target collection page before writing.
- No invented colorways, formats, or suitability claims. Zellige colorways are gated `verify`.
- Contact line (info@ziatile.com + 310-844-1170) in closing and relevant FAQ answers.
