# Search Atlas — Q3 2026 Content Strategy

Evidence-based content production strategy for searchatlas.com, July–September 2026.
**Prepared:** 2026-06-25 · **Author:** Aleksandra Velickovic (Content Ops) · **Status:** ready for stakeholder review.

---

## Main strategic recommendation

**Consolidate and route; don't scale wider.** Search Atlas's organic footprint is huge but past its peak — H1-2026 clicks are −33% vs H2-2025 and impressions are deflating as the low-value long tail collapses. Branded queries carry ~half of all clicks. The Q3 wins are: (1) a snippet/CTR sprint that recovers thousands of clicks at near-zero effort, (2) consolidating duplicate/cannibalizing pages, and (3) building one real **AI Search Discoverability cluster** (hub + internal links + tool routing) on top of content SA already ranks for — the durable 2026 demand shift where SA owns a product (LLM Visibility) but the content is orphaned. Full rationale in `01-executive-summary.md`.

## How to navigate the deliverables

**Start here:** `01-executive-summary.md` → then the file matching your question.

| # | File | What it answers |
|---|---|---|
| 01 | `01-executive-summary.md` | The recommendation, why, what we'll do, decisions needed, first 30 days |
| 02 | `02-data-sources-and-methodology.md` | Where every number comes from; comparison windows; limitations |
| 03 | `03-content-inventory.csv` | The ~80 most material URLs with GSC metrics + one action each |
| 04 | `04-gsc-performance-analysis.md` | Page + query diagnosis (flat clicks, impression deflation, branded share) |
| 05 | `05-content-decay-and-quick-wins.csv` | Decaying pages, quick wins (pos 4–15), CTR fixes — prioritized |
| 06 | `06-cannibalization-map.csv` | Competing-URL clusters + canonical/merge/redirect plan |
| 07 | `07-topic-cluster-and-gap-analysis.md` | Cluster map, missing pillars, orphans, BOFU gaps, where NOT to build |
| 08 | `08-2026-trends-research.md` | 13 dated, sourced 2026 trends with confidence + flagged claims |
| 09 | `09-competitor-serp-analysis.csv` | Live SERP shape + competitor matrix + compete/don't-compete calls |
| 10 | `10-opportunity-scorecard.csv` | 33 opportunities scored on 12 weighted dimensions → priority |
| 11 | `11-q3-content-portfolio.md` | The portfolio split into refresh/consolidation/net-new/experimental + capacity reconciliation + "what NOT to produce" |
| 12 | `12-q3-editorial-calendar.csv` | Week-by-week (W1–W14) calendar with production stages, SMEs, risks |
| 13 | `13-top-10-content-briefs.md` | Full briefs for the 10 highest-priority assets |
| 14 | `14-internal-linking-plan.csv` | 25+ specific link moves (cluster mesh, tool routing, mis-link removal) |
| 15 | `15-measurement-framework.md` | Baselines, Q3 targets, what's measurable vs needs tracking |

## Methodology (summary)

1. **Audit** — confirmed GSC access (standalone MCP works; SA-platform GSC disconnected), mapped repo sources, set windows (28d/90d/178d/365d).
2. **Inventory & diagnose** — full page/query pulls + GSC's `quick_wins`, `content_decay`, `traffic_drops`, `cannibalization_check`, `content_gaps`, `ctr_opportunities`.
3. **Research** — live web/SERP research on 2026 trends and competitor pages (dated sources, confidence-flagged).
4. **Score & sequence** — 12-dimension weighted model → priority bands → portfolio → calendar → briefs → linking → measurement.

Raw GSC pulls are preserved in the session tool-results directory, separate from interpretation. No published content was modified.

## The scoring model

Each opportunity is scored 1–5 on 12 dimensions, weighted to a 0–100 Opportunity Score: `Σ (score/5 × weight)`.

| Weight | Dimension | Weight | Dimension |
|---|---|---|---|
| 14 | GSC demand (impressions) | 8 | Topical authority contribution |
| 13 | Ranking proximity | 7 | Information-gain potential |
| 11 | Competitive feasibility | 6 | AI-answer citation potential |
| 10 | Commercial intent | 5 | Internal-linking value |
| 10 | Product relevance | 4 | Topic relevance |
| 9 | Strategic relevance (2026) | 3 | Content-freshness requirement |

GSC demand + ranking proximity + feasibility carry **38/100 by design**, so real GSC data — never estimated keyword volume — drives priority. **Bands:** P0 ≥80 · P1 70–79 · P2 58–69 · P3 45–57 · Reject <45. **Fast-track exception:** low-effort, high-certainty cleanups (consolidations, technical fixes, the snippet sprint) are promoted to P0/P1 above their score band; each is labeled in file 10.

## Important assumptions

- **Capacity = Aggressive** (stakeholder-confirmed): 10 net-new + 6 refresh + 12 light /month + 3 data-led/quarter. The plan deliberately uses less.
- searchatlas.com is a **large, mature** property (4,230 blog URLs, 22,340 queries); the repo holds only recent campaign work. The inventory covers the ~80 material URLs, not the full long tail (a stated cap).
- Production runs through the existing content pipeline (Content Genius / parallel-pieces) with the QA gates and IMPROVEMENT-LOOP for failures.

## Data limitations (carried into every file)

- **No conversion/signup/revenue data** — funnel and conversion relevance are *inferred from intent*, not measured.
- **No AI-citation tracking for searchatlas.com** — assessed via point-in-time SERP/LLM inspection only.
- **No reliable keyword volume** — demand anchored on real GSC impressions; external volume labeled estimate.
- **No full crawl** — word counts and internal-link counts are blank/estimated.
- **Sitemaps API unavailable** (domain property + service account).
- Several external trend stats are **flagged** (file 08 §"Flagged claims") — do not publish without further sourcing.

## Decisions that require stakeholder approval

1. Endorse "consolidate, don't scale" (publish fewer net-new than capacity allows).
2. Unblock: (a) product SME for the LLM Visibility setup walkthrough; (b) competitor research on Profound/Peec/Scrunch for the AI-visibility tools comparison (no invention until then).
3. Approve an LLM Visibility project **for searchatlas.com itself** to make AI-citation measurable.
4. Confirm canonical naming ("LLM Visibility" vs "QUEST"; "Search Atlas Coworker" vs "Atlas Brain").
5. Engineering ticket: de-index `labs.searchatlas.com` staging subdomain + fix FAQ-anchor URL indexing.

## Quality controls applied

Every recommended topic was checked against the existing inventory and the prior campaign audit/briefable-set to avoid duplicating live content (e.g., the DA-vs-AI-citations research already exists as a live companion post — flagged as a refresh, not net-new). Competitor pages were verified live (2026-06-25). External claims carry source URLs + dates + confidence. Facts, estimates, and inferences are labeled throughout. Every P0/P1 asset has a product, business, or authority rationale. The portfolio volume fits the stated capacity with headroom. Refreshes and consolidations are sequenced before net-new. A "What we should not produce" section and a "Decisions needed" section are included.
