# 07 — Topic Cluster & Gap Analysis

Maps the live searchatlas.com content into clusters (from GSC + repo), then identifies missing pillars, weak depth, orphans, BOFU gaps, and product capabilities with no search coverage. Cluster signals are GSC facts; structural judgments are labeled [inference].

---

## 1. Cluster map (live site)

| Cluster | Representative URLs | Health | Commercial fit | Core problem |
|---|---|---|---|---|
| **AI-Search (AEO/GEO/AIO/LLM-visibility/agentic)** | /blog/aeo, /geo, /aio, /aeo-traditional-seo, /aeo-aio-geo, /seo-vs-sco, /agentic-seo, /agentic-marketing, /vibe-seo, /ai-overviews, /track-llm-traffic, /track-traffic-google-gemini, /dense-vs-sparse-retrieval, /llm-visibility (product) | Deep info coverage (20+ posts), several decaying | **High** — matches the 2026 demand shift and SA's LLM Visibility product | **No hub, orphaned, no tool routing.** The marquee opportunity. |
| **Competitor-Comparison (alternatives / vs / reviews)** | /blog/ahrefs-features (top earner 1,944), /ahrefs-review, /ahrefs-cons, /searchatlas-vs-ahrefs, /search-atlas-vs-semrush, /perplexity(ai)-alternatives, /similarweb-alternatives, /brightedge-review, dozens more | SA's strongest cluster; heavy cannibalization + duplicates | **High** — BOFU, brand already wins "vs" queries at 50–93% CTR | Consolidation needed (file 06); branded /x-vs/ pages thin vs non-branded "alternatives" intent |
| **Product / Commercial** | /otto-seo, /content-genius, /site-explorer, /local-citations, /otto-google-ads, /da-checker, /backlink-analyzer, /pricing, /features, /case-studies | Many decaying; severe CTR starvation (file 04 §5) | **High** — BOFU | Snippets lose the click at good positions; some pages orphaned |
| **SEO Automation** | "seo automation (platform/software/tools)" family — currently served by homepage + /otto-seo | Ranks pos 6–11 but weak CTR; no dedicated hub | **High** — best demand-to-feasibility ratio on the site | No owned hub page for the automation category |
| **White-Label / Agency** | /white-label-seo-software (decaying), /enterprise-agency, "seo software for agencies", "white label seo *" (20+ queries, 200k+ impr) | Ranking pos 20–65; staging subdomain leaking into index | **High** — agency ICP | Thin coverage of a large, high-intent query family; no agency hub |
| **Local-SEO** | /local-seo, /local-citations, /local-seo-software, /google-my-business-management-software, /blog/local-citation-services | Mixed; several decaying | **High** — commercial | No local hub; "GMB" naming risk (STYLE-SYSTEM: use GBP) |
| **SEO-Education (foundational)** | /blog/technical-seo, /on-page-seo, /off-page-seo, /keyword-difficulty, /seo-content, /topical-authority, /backlinks, /seo | Broad; head-term heavy at pos 35–50; impression-deflating | **Low–medium** — TOFU | Low feasibility on head terms; refresh/repurpose, don't expand |
| **AI-Tools-Reviews (tangential)** | /blog/what-is-chatgpt, /what-is-claude, /what-is-gpt-4o, /chatgpt-vs-claude, /chatgpt-alternatives, /best-ai-tools | High impressions, very low CTR | **Low** — off-ICP | Harvest CTR via snippet fixes; **do not invest further** |

## 2. Missing pillars (build in Q3)

| Pillar | Why | Evidence | Priority |
|---|---|---|---|
| **AI Search Discoverability hub** | The AEO/GEO cluster has 20+ posts but no pillar tying them together or routing to the LLM Visibility product. Campaign audit (`blog-cluster-audit.md`) already diagnosed this. | /geo 46.9k impr @ 35, /aeo @ 23.7, /llm-visibility product decaying & orphaned; trend file 08 confirms AEO is the durable 2026 shift | **P0** |
| **Agency / White-Label hub** | A 200k+ impression query family ranks pos 20–65 with no consolidating hub; agency is a primary ICP. | "seo software for agencies" 11k impr @ 13.6; white-label family; /white-label-seo-software decaying | **P1** |
| **SEO Automation hub** | Best demand-to-feasibility ratio; SA ranks pos 6–11 across the family but with no owned category page. | quick-wins: automation family 5k–10k impr @ 6–11 | **P1** |
| **Domain Power pillar** | Owns a proprietary entity and consolidates the cannibalized DA cluster; backed by original research. | DA cluster ~170k impr split across 4 URLs; proof study exists | **P2** |
| **Local SEO hub** | Local pages decaying and uncoordinated; commercial fit is strong. | local cluster decay (file 05) | **P2** |

## 3. Weak cluster depth & orphans

- **AI-Search is deep but flat** — many sibling posts, no hierarchy, cross-linked to the *wrong* cluster (AI-CMO) per the campaign audit. [evidence: blog-cluster-audit.md §2]
- **/llm-visibility/ product page is orphaned** at pos 26.8 and decaying — the natural conversion destination for the entire AEO cluster receives no internal links from it. [evidence: file 04 §4]
- **Comparison cluster has duplicate orphans** — perplexity-alt ×2, claude-review ×2 (file 06).
- **Anchor-fragment "orphans"** — FAQ/anchor URLs indexed separately across paid-seo, buzzsumo-vs-ahrefs, automated-internal-linking, advanced-seo-course, seo-citations (file 06). Equity leak.

## 4. Clusters with informational coverage but no BOFU path

| Cluster | Has info content | Missing BOFU | Fix |
|---|---|---|---|
| AI-Search | 20+ explainers | Route to LLM Visibility product + a product walkthrough | Hub + tool CTAs (file 14) |
| SEO Automation | scattered mentions | A category/automation landing that converts to OTTO | Automation hub → OTTO |
| Agentic SEO | /blog/agentic-seo (conceptual) | Proof that OTTO *executes* (vs competitors who only describe) | Agentic-execution piece with OTTO before/after (brief #4) |

## 5. Product capabilities with little or no search coverage (content debt)

[inference, cross-referenced with `raw/knowledge/products/`]

| Capability | Search coverage today | Opportunity |
|---|---|---|
| **Search Atlas Coworker** (the agentic workspace agent — Slack/Teams/ClickUp) | Almost none beyond /agentic-marketing; "search atlas mcp" emerging (pos 16.7) | The flagship rebrand story has near-zero content. Net-new cluster: "AI marketing coworker", "marketing automation in Slack". |
| **Smart Ads** (Google + Meta ads execution) | Only /otto-google-ads (decaying) | "Every channel" pillar is thin on paid. Demand-gen/PPC-automation content. |
| **Scholar** (12-dimension content grading) | None | Content-quality / AI-content-grading angle ties to the May-2026 core-update "information gain" theme (file 08, trend 7.1). |
| **Website Studio** (site building) | /blog/blog-setup only | Low priority; niche. |
| **Report Builder** (cross-source SEO+GEO+AEO dashboards) | None | Supports the AI-visibility comparison wedge vs Semrush. |

## 6. White space confirmed by live SERP research (file 09)

These are gaps **competitors left open**, not just things SA lacks:

1. **"How to track LLM referral traffic" (practical GA4/Looker how-to)** — incumbents are weak/new domains; no high-DA SEO brand owns the step-by-step. SA can win with a credible brand + a downloadable Looker template. **[Highest white-space fit.]**
2. **Agentic SEO with reproducible artifacts + real execution proof** — only Ahrefs shipped a hands-on workflow (mock "Agent A"); SA actually ships execution (OTTO) and can show real before/after.
3. **Original AEO/GEO measurement data** — every ranking AEO/GEO guide lacks case studies/benchmarks; SA has proof studies (`raw/knowledge/proof/`) to translate.
4. **Platform-specific AEO tactics** (ChatGPT vs Perplexity vs AI Mode) and **AEO failure modes / brand safety** — named weaknesses in Profound and Semrush pages.

## 7. Where NOT to build (low feasibility / poor fit)

- Bare head terms **"answer engine optimization" / "generative engine optimization"** — Wikipedia + arxiv (GEO) and high-DA generalists + Profound (AEO) own them. Compete on derivative how-to/measurement queries instead.
- **"google ai mode"** as evergreen — Google owns positions 1–2; the rest is news velocity (file 09).
- **"local citation builder"** as a content roundup — BrightLocal/Whitespark own the category; defend the product page only.
- **Net-new "best Ahrefs/Semrush alternatives" roundups** — saturated high-DA tested-listicle layer; earn inclusion + own the branded `/x-alternative` page instead.
- **More AI-tools-reviews** (what-is-chatgpt etc.) — off-ICP; harvest CTR, don't expand.
- **More foundational SEO head-term pages** — impression-deflating, low feasibility.
