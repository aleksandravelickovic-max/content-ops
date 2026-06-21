# 01 — Blog Content (AI CMO cluster)

**Goal:** SEO blog cluster around the "AI CMO" topic, produced in batches through the content pipeline.
**Status:** Batch `ai-cmo-batch-01` complete (8/8 topics, all passed QA after revision — see `batches/production-log.md`).

## Layout
- `briefs/` — one brief per piece (`*-brief.md`).
- `drafts/` — working markdown, versioned (`-v1`, `-v2`).
- `final/` — approved markdown, no version suffix.
- `html/` — rendered HTML for delivery (mirrors `final/`).
- `batches/` — batch input CSV + `production-log.md`.
- `research/` — supporting docs (e.g. DPR editorial guidelines).
- `registry.json` — auto-generated; do not hand-edit.
