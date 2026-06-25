# 15 — Measurement Framework

How Q3 success is measured. Baselines are exact GSC values (90d ending 2026-06-24). Targets are deltas measured at quarter end (Sep 30, then a clean read ~Oct 8 to clear any late-Sep core-update noise — file 08-T12). Metrics are split into **directly measurable today** vs **requires additional tracking** (per the data limitations in file 02).

> **Measurement caveat:** searchatlas.com sits in an impression-deflation trend (file 04). Raw impression growth is the wrong headline metric for Q3 — chasing it repeats the mistake that caused the decline. Q3 is judged on **non-branded clicks, page-one keyword count, CTR recovery, and cluster-level visibility**, not gross impressions.

---

## 1. Leading indicators (production — owner: Content lead)

| Metric | Baseline | Q3 target | Source | Cadence |
|---|---|---|---|---|
| Net-new long-form published | — | 14 (of 30 capacity) | Editorial calendar / registry.json | Weekly |
| Substantial refreshes completed | — | 9 | Calendar | Weekly |
| Light optimizations (CTR/snippet) | — | ~30 (top-30 pages) | Calendar | Weekly |
| Consolidations completed (merges+301s) | 0 | 6 | file 06 | Monthly |
| Internal links added/repointed | ~0 cluster mesh | 25+ moves (file 14) | file 14 / crawl | Monthly |
| Data-led assets shipped | 0 | 3 | Calendar | Quarterly |
| Indexation of new/changed URLs | — | 100% of published within 2 wks | GSC `inspect_url` / Coverage | Weekly |

## 2. Lagging indicators — directly measurable in GSC

| Metric | Baseline (90d) | Q3 target | Source | Interpretation |
|---|---|---|---|---|
| **Total clicks** | 45,767 | +8–12% (≈49,000–51,000) | GSC site_snapshot | Modest; the win is mix-shift to non-branded, not gross volume |
| **Non-branded clicks** | ~22,900 (est. ~50%) | **+20–25%** | GSC (query filter) | The real growth metric; brand is already saturated |
| **Avg position** | 30.9 | ≤ 28 | GSC | Continued improvement as long tail trims + clusters rank |
| **Site CTR** | 0.27% | ≥ 0.40% | GSC | Driven by the snippet sprint (§file 05) |
| **Page-one keywords (pos ≤10)** | baseline TBD at kickoff | +15% | GSC query export | Quick-wins (pos 4–15) crossing to page one |
| **Top-3 keywords** | baseline TBD at kickoff | +10% | GSC query export | Commercial + AI-search terms |
| **AI-Search cluster clicks** (aeo/geo/aio/agentic/llm-visibility/track-*) | baseline at kickoff via topic_cluster_performance | **+30%** | GSC `topic_cluster_performance` | Marquee cluster; hub + linking + tool routing |
| **Automation cluster position** (automation/agency family) | pos 6–14 | majority ≤ 8 | GSC | Quick-win family to page one |
| **CTR-fixed pages recovered clicks** | per file 05 | ≥ 8,000 recovered clicks (conservative vs ~25k modeled) | GSC before/after | Tracks the snippet sprint specifically |
| **Decaying pages stabilized** | 8 priority pages declining | ≥ 6 of 8 flat-or-up | GSC traffic_drops | Refresh effectiveness |
| **Cannibalization clusters resolved** | per file 06 | 6 clusters single-canonical | GSC cannibalization_check | Post-consolidation re-check |

> **Baselines marked "TBD at kickoff"** require a one-time full query export on Jul 1 (page-one and top-3 counts aren't in the snapshots already pulled). Capture them in week 1.

## 3. Lagging indicators — require additional tracking (NOT measurable today)

| Metric | Why not measurable now | What to set up |
|---|---|---|
| **Signup / demo / trial contribution** | No analytics/CRM connection this session (file 02) | Wire GA4 + CRM; tag content-assisted signups. Until then, conversion is **inferred from intent**, not reported. |
| **Assisted conversions / pipeline** | Same | GA4 attribution + UTM on CTAs |
| **AI Overview presence / SA citations** | SA's LLMV tracks client domains, not searchatlas.com | Stand up an LLM Visibility project **for searchatlas.com itself** (the `llmv_*` tools) — high-value, low-effort; makes the State-of-AI-Search asset self-referential proof |
| **AI-answer mentions/citations of SA** | Same | Same LLMV-for-own-domain setup; track share of voice vs Profound/Semrush |
| **Featured snippet / PAA capture** | Not in the GSC pulls run | Add SERP-feature tracking (SA Keyword Rank Tracker or `krt_*` tools) |
| **LLM referral traffic (ChatGPT/Perplexity)** | Invisible in default GA4 | The GA4 channel-group + Looker template from Brief 2 — dogfood it on searchatlas.com |

## 4. Reporting cadence & ownership

| Report | Cadence | Owner | Audience |
|---|---|---|---|
| Production tracker (leading) | Weekly | Content lead | Internal team |
| GSC performance (lagging, directly measurable) | Monthly | Content lead | Justin Rondeau / Sophia / Mihai |
| Cluster + cannibalization re-check | Monthly | Content lead | Internal |
| Quarter-end review (all KPIs + State-of-AI-Search) | End Q3 (clean read ~Oct 8) | Content lead | Leadership |

## 5. Interpretation notes

- **Don't celebrate impression growth.** Given the deflation trend, rising impressions could mean low-value long tail returning. Judge on non-branded clicks and page-one keywords.
- **Wait a week after any late-Sep core update** before reading Q3 results (Google's own guidance, file 08-T12).
- **Branded vs non-branded must be reported separately** every month — brand strength can mask flat non-branded performance.
- **Attribute cautiously.** Without conversion tracking, do not claim pipeline impact; report ranking/traffic outcomes and label conversion as inferred until §3 tracking is live.
- **Cluster-level over page-level for AI-Search** — the hub strategy succeeds if the *cluster* rises, even if individual page positions move unevenly.
