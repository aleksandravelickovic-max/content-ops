# 01 — Product & Collection Pages

**Goal:** Rewrite Zia Tile collection pages and product (SKU) pages from approved templates, with before/after HTML for client review.
**Status:** Largest campaign; collection pages held pending Jamie's review, product pages in progress.

## Layout
- `brief.md` / `brief.html` — campaign brief.
- `campaign-urls.md` — target URLs.
- `audit-report.md` — pre-production audit findings.
- `drafts/` — collection-page markdown (numbered) + `drafts/product-pages/` (SKU pages) + `drafts/v3/` (deep revisions).
- `gdocs-content/` — Google Docs exports. **Two layers, kept separate on purpose:**
  - `collection-pages/`, `product-pages/` — processed markdown.
  - `collection-pages-fresh/`, `product-pages-fresh/` — raw `.txt` exports (source).
- `html/` — `index.html` plus `original/` and `revised/` for the before/after review view.
- `runs/` — pipeline state files.
- `_build/` — one-off patch/util scripts (`patch-revised-pages*.py`, etc.) — excluded from registry.
- `registry.json` — auto-generated; do not hand-edit.

> The registry generator (`scripts/build-content-navigator.py`) has Zia-specific logic keyed to the `01-product-collection-pages` path and the `html/original|revised` + `gdocs-content` layout. Do not rename these without updating the script.
