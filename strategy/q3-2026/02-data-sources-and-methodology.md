# 02 — Data Sources & Methodology

**Client:** Search Atlas (searchatlas.com) · **Quarter:** Q3 2026 (Jul 1 – Sep 30) · **Prepared:** 2026-06-25
**Author:** Aleksandra Velickovic (Content Ops) · **GSC property:** `sc-domain:searchatlas.com`

This file documents every data source, the windows used, how each metric was derived, and what could not be measured. Raw GSC pulls are preserved separately from interpretation (see §5). Read this before trusting any number elsewhere in the strategy.

---

## 1. Data sources used

| Source | What it provided | Status |
|---|---|---|
| **Standalone GSC MCP** (`mcp__gsc__*`) | All live search-performance data: site totals, page/query analytics, quick wins, content decay, traffic drops, cannibalization, content gaps, CTR opportunities | ✅ Working — live data, exact values |
| **Repository** `clients/searchatlas/` | STYLE-SYSTEM.md (2026 rebrand positioning), COMPLIANCE.yml, `raw/knowledge/` (products, facts, proof studies, 50+ competitor files, testimonials), campaign briefs/drafts/research | ✅ Read directly |
| **Campaign research** (`03-ai-search-discoverability/research/`) | `blog-cluster-audit.md`, `briefable-set.md`, `tier1-title-fixes.md` — prior strategic analysis of the AEO/GEO cluster | ✅ Read directly |
| **Live web / SERP research** | 2026 trend evidence (dated sources) and competitor SERP inspection | ✅ Via research sub-agents (see files 08, 09) |

## 2. Data sources NOT available (material limitations)

| Source | Impact | How handled |
|---|---|---|
| **Search Atlas platform GSC** (`mcp__searchatlas__gsc_*`) | Returns "GSC is NOT connected for this account" — confirms the known ~2026-06-18 token-reset breakage. | Routed ALL GSC work through the standalone MCP. No data lost; only the SA-native UI path is down. |
| **Conversion / signup / demo / revenue data** | No analytics or CRM connection available this session. "Conversion relevance" cannot be measured. | Funnel stage and conversion relevance are **inferred from query intent**, not measured. Every such field is labeled *(inferred)*. |
| **AI Overview / LLM citation tracking for searchatlas.com** | SA's own LLM Visibility product tracks *client* domains, not searchatlas.com itself. No wired-up AI-answer share data. | AI-answer visibility assessed via point-in-time live SERP/LLM inspection (file 09), flagged as snapshot, not trend. |
| **Keyword search volume** | No reliable volume feed connected. | Demand is anchored on **actual GSC impressions** (real, not estimated). Any external volume is labeled *estimate*. |
| **Sitemaps API / full indexation counts** | Domain property + service account blocks the Sitemaps API. | Indexation inferred from page-level analytics presence and `inspect_url` spot checks. Full crawl not available. |
| **Word counts, internal-link in/out counts** | Not exposed by GSC; full crawl not run this session. | Word count and link counts in the inventory are blank or estimated from the repo where a draft exists; labeled *(est.)* or left empty. A Screaming Frog / Site Auditor crawl is required to complete these columns. |

## 3. Comparison windows (all per the task spec)

GSC data reaches **2026-06-24** (yesterday). Default ~16-month retention supports YoY.

| Window | Dates | Use |
|---|---|---|
| **Last 28d vs prior 28d** | 2026-05-28 → 06-24 vs 2026-04-30 → 05-27 | Recent momentum / freshest trend |
| **Last 90d vs prior 90d** | 2026-03-27 → 06-24 vs 2025-12-27 → 03-26 | Primary working window (stable sample) |
| **YoY (365d vs prior 365d)** | 2025-06-25 → 2026-06-24 vs 2024-06-25 → 2025-06-24 | Long-run trajectory |
| **YTD-equivalent (178d vs prior 178d)** | 2025-12-29 → 2026-06-24 vs prior 178d | H1-2026 vs H2-2025 (catches the 2026 deceleration) |

## 4. Site-level baselines (exact GSC values — facts, not estimates)

| Metric | 28d | prior 28d | 90d | prior 90d | 365d | prior 365d |
|---|---|---|---|---|---|---|
| Clicks | 13,919 | 16,407 (−15.2%) | 45,767 | 45,069 (+1.6%) | 232,303 | 92,403 (+151%) |
| Impressions | 4.97M | 5.68M (−12.5%) | 17.16M | 27.63M (−37.9%) | 176.8M | 47.8M (+270%) |
| CTR | 0.28% | 0.29% | 0.27% | 0.16% | 0.13% | 0.19% |
| Avg position | 27.1 | 31.8 | 30.9 | 39.3 | 33.4 | 44.7 |

**178d (H1-2026 vs H2-2025):** clicks 90,061 vs 134,881 (−33.2%); impressions 43.9M vs 127.5M (−65.6%).

**Device (90d):** Desktop 40,346 clicks (88%) / Mobile 5,266 / Tablet 155 — strongly professional/B2B.
**Country (90d):** USA 24,336 (53%), India 5,121, Pakistan 2,085, Canada 1,807, UK 1,532, Australia 1,437. **US is the commercial market**; high-CTR South-Asian traffic skews to free-tool / how-to / course intent (low commercial value).

## 5. Method — how each derived metric was produced

- **Branded vs non-branded.** Branded = queries matching `atlas|otto|domain power|scholar|gbp galactic|manick`. The two largest branded queries alone ("search atlas" 11,973 + "searchatlas" 2,891 = 14,864) are ~32% of all 90d clicks; adding navigational/brand variants (login, careers, pricing, otto, atlas brain, manick bhan course, misspellings) puts branded at an **estimated 48–57% of clicks (~22k–26k of 45,767)**. Exact split requires a full query export; the band is labeled an estimate. The strategic point holds regardless: non-branded converts a tiny fraction of a vast impression base.
- **Click/impression trend.** Direction taken from the 90d-vs-prior-90d and 28d comparisons returned by GSC; "decline" = consistent loss across `content_decay` (3×30d) or a material drop in `traffic_drops`.
- **Decay diagnosis.** Used GSC's own `traffic_drops` diagnosis field (ranking loss / CTR collapse / impression decline / disappeared) — not inferred by me.
- **Cannibalization.** From `cannibalization_check` (min 200 combined impressions, 90d); a cluster = one query with ≥2 SA URLs ranking. Full output (50 queries, 5,719 lines) preserved to the session tool-results file.
- **Opportunity Score.** 12 weighted dimensions, formula in file 10 and the README. GSC demand + ranking proximity + feasibility carry 38/100 so estimated volume never drives priority.

## 6. Inventory scope decision

The live blog has **4,230 `/blog/` URLs** (90d) and the domain returns **22,340 distinct queries**. The inventory (file 03) covers the **~80 most material URLs** — every page with meaningful clicks or a strategic role (commercial product pages, the AEO/GEO cluster, top blog earners, decaying pages, cannibalization principals). The low-value long tail is **deliberately excluded**; it is the impression deflation described in file 04, not an action target. This is a stated cap, not an omission — completing all 4,230 rows requires a full crawl export and adds no decision value.

## 7. Integrity rules applied

- No fabricated volume, traffic, rankings, competitor metrics, or conversion data. Every GSC number traces to a live pull.
- Facts (GSC pulls, repo knowledge) are separated from inference (funnel/conversion labels, causes). Causes are labeled *evidence* vs *inference* in file 04.
- External trend/competitor claims carry source URL + date + access date (files 08, 09).
- Where data is missing, the gap is flagged — not filled.
