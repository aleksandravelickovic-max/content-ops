# 02 — June 2026 Content Optimization

**Goal:** Revise 8 of the 10 June 2026 Altify optimization deliverables per client feedback — fix mechanical/repetitive paragraph and subsection structure, add natural transitions and grounded product insight, and (for Op1) re-point the MaxAI page off brand-collision traffic onto the deal-management keyword cluster.
**Status:** 8/8 drafts written. Op2 (Sales Enablement Glossary) and Op9 (Acquiring a New Customer Glossary) were not revised — no client feedback was given on those two.

## Layout
- `campaign-urls.md` — target URLs, keywords, and which client feedback each piece addresses.
- `research/live-baseline/` — verbatim snapshot of each live page as scraped before revision (for diffing).
- `drafts/` — revised working markdown, `-v1` suffix per campaign-structure convention.

## Open items before publish
- **Op1 (MaxAI):** recommended title/H1/meta are a **Webflow dependency** — must be pasted manually into Webflow, not deployable via OTTO.
- Several drafts (Op1, Op5, Op6) contain `[VERIFY]`-flagged internal link targets where the exact live URL/slug could not be confirmed this session — check before publishing.
- Op1's baseline capture notes the live page has four different title variants across `<title>`, og:title, twitter:title, and schema.org — worth a CMS check independent of this optimization.
- Op5's baseline flagged a broken/truncated sentence on the *current live page* ("...which touchpoints are") — a pre-existing CMS bug, not something this optimization introduced; worth a bug report.
