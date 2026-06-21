# AI Search Discoverability — Briefable Set (Bottom-Funnel + Product-Led)

Origin: Sophia's directive (LLM Visibility tool heavily used but under-surfaced; own AEO/AI search discoverability).
Strategy basis: the definitional/glossary layer is saturated (~130 existing topics). This phase adds the **conversion and differentiation layer** that routes demand to the LLM Visibility tool.

All facts below are grounded in `clients/searchatlas/raw/knowledge/`. Each entry lists its source files and any gap that must be closed before drafting. No invention — gaps are flagged, not filled.

Rules carried in: one dedicated product section per article (article-balance rule); product-led pieces are the sanctioned exception where the tool can take center stage. Competitor claims use only documented data in `raw/knowledge/competitors/`.

---

## ⚠️ STATUS UPDATE (2026-06-19): much of this is ALREADY PUBLISHED — audit before briefing

Each Search Atlas research report has a companion blog post published the same day. Several pieces proposed below already exist on the blog and must NOT be re-briefed as net-new:

- **B2** (does DA affect AI citations) → https://searchatlas.com/blog/authority-metrics-in-the-age-of-llms-visibility-correlation-analysis/ (live, updated 2026-05-26). The B2 draft in `drafts/` is now a **non-shippable duplicate** — kept only as a refresh reference.
- **B3** (why platforms differ) → https://searchatlas.com/blog/how-gpt-results-differ-from-google-search-llm-serp-overlap-study/ (live).
- **B4 / SEO-to-GEO pillar** → covered by https://searchatlas.com/blog/geo/ (live).
- **A3** (AI-visibility tool comparison / Profound) → https://searchatlas.com/blog/best-profound-ai-alternatives/ (live).

**Required before any further briefing:** audit the existing searchatlas.com/blog AEO/GEO/AI-visibility cluster, map what is already published, and re-scope this set to genuine gaps only. The real opportunity per Sophia's directive is likely content→tool routing and discoverability, not net-new topics. See [[project_sa_research_library]].

## Group A — Bottom-funnel / commercial intent

### A1. Search Atlas vs Semrush for AI visibility
- **Primary keyword:** "search atlas vs semrush" / "semrush ai visibility"
- **Intent:** commercial comparison, decision-stage
- **Angle:** Semrush is audit-first analytics with no LLM visibility tracking; Search Atlas bundles LLM Visibility into Site Explorer and Report Builder (SEO + GEO + AEO dashboards).
- **Grounded facts:** `competitors/semrush.md` — "no built-in LLM Visibility or Topical Dominance linkage"; Report Builder = "cross-source SEO + GEO + AEO dynamic dashboards"; OTTO = live execution vs audit suggestions.
- **Product tie:** LLM Visibility (primary), Site Explorer, Report Builder.
- **Gap:** competitor file `last_verified: 2026-04-22`. Re-verify Semrush hasn't shipped an AI-visibility module before publishing.

### A2. Search Atlas vs Ahrefs for AI visibility
- **Primary keyword:** "search atlas vs ahrefs"
- **Intent:** commercial comparison
- **Angle:** Ahrefs is report-first (surfaces data); Search Atlas pairs data with execution and native LLM Visibility tracking.
- **Grounded facts:** `competitors/ahrefs.md` — "no Domain Power traffic-weighted authority," report-first positioning. Differentiator is built-in LLM Visibility + OTTO execution.
- **Product tie:** LLM Visibility, Domain Power, OTTO SEO.
- **Gap:** Do **not** claim Ahrefs lacks any AI feature it now has (e.g., Brand Radar is not in our file). Re-verify before publish. Only assert what the file supports.

### A3. AI visibility tools comparison: SEO suites vs content optimizers vs dedicated trackers
- **Primary keyword:** "ai visibility tool comparison" / "best llm visibility tools"
- **Intent:** commercial investigation, category map / listicle
- **Angle:** Map the landscape. Content optimizers (Surfer, Frase, Clearscope, MarketMuse, Scalenut) optimize content but don't track LLM visibility; SEO suites are adding it; dedicated trackers focus only on tracking. Search Atlas = suite with native LLM Visibility.
- **Grounded facts:** content-optimizer positioning in `competitors/{surfer-seo,frase,clearscope,marketmuse,scalenut}.md`; LLM Visibility capabilities in `products/llm-visibility.md`.
- **Product tie:** LLM Visibility.
- **GAP — BLOCKER:** the AI-visibility-native players (Profound, Otterly, Peec, Scrunch/Athena, etc.) are **not** in `raw/knowledge/competitors/`. A credible roundup must name them. **Requires new competitor research + knowledge files before drafting.** Do not invent their features.

### A4. What AI visibility tracking costs
- **Primary keyword:** "ai visibility tracking cost" / "llm visibility tool pricing"
- **Intent:** commercial, decision-stage
- **Angle:** Plain pricing breakdown for buyers comparing AI-visibility tooling, framed against the cost of building tracking manually.
- **Grounded facts:** `facts/search-atlas-pricing-range.md` ($99–$399/mo, custom enterprise, 7-day full-feature trial, no card); `facts/search-atlas-plan-details.md` (per-plan quotas).
- **Product tie:** plans/LLM Visibility access.
- **Gap:** none for SA pricing. If comparing competitor pricing, that data isn't in knowledge — omit or research first.

> Not included (already covered in existing topic list — avoid cannibalization): "How to choose the right AI visibility tracking tool," "Vendor evaluation checklist."

---

## Group B — Product-led

### B1. How to set up AI visibility tracking in Search Atlas (walkthrough)
- **Primary keyword:** "how to track brand visibility in ai search" / branded
- **Intent:** how-to / product onboarding — **the direct fix for "the tool is hard to find."**
- **Angle:** Step-by-step from zero to a populated visibility dashboard.
- **Grounded facts:** `products/llm-visibility.md` — tracks brand mentions, sentiment, visibility gaps across ChatGPT, Claude, Gemini, Perplexity; data views (visibility trends, share-of-voice, cross-platform ranking, sentiment, topic-level); cross-model scoring; competitor benchmarks.
- **Product tie:** LLM Visibility (center stage — sanctioned).
- **GAP:** exact UI/setup steps are not in knowledge. **Needs a product SME walkthrough or tool docs before drafting** — do not invent screens or button names.

### B2. Do authority metrics (DA/DR) predict AI citations? — original research
- **Primary keyword:** "do backlinks affect ai citations" / "domain authority ai search"
- **Intent:** informational with strong link/citation-bait value — **highest citation-magnet potential.**
- **Angle:** Original Search Atlas data: legacy authority metrics do not predict LLM citation behavior.
- **Grounded facts:** `proof/domain-power-llm-visibility-study.md` — 21,767 domains (DP/DR/DA vs LLM visibility) + 368,972-domain competition-tier subset; weak negative correlations; legacy authority doesn't predict citations; Domain Power recalibrated so LLM visibility, co-mention frequency, and response prominence are primary predictors.
- **Product tie:** Domain Power + LLM Visibility.
- **Gap:** none — fully grounded. Attribute to Manick Bhan / SA research team.

### B3. Why AI platforms show different results — and how to track each one (data-backed)
- **Primary keyword:** "why do different ai platforms show different results" (exists as info topic — **upgrade, don't duplicate**)
- **Intent:** informational → product
- **Angle:** Reframe the existing definitional topic with original overlap data, ending in per-platform tracking.
- **Grounded facts:** `proof/gpt-vs-search-study.md` — 18,377 matched LLM–SERP query pairs; Perplexity 25–30% domain / 20% URL overlap with SERPs; GPT and Gemini <15% domain / <10% URL; distinct retrieval behaviors require dedicated per-platform tracking.
- **Product tie:** LLM Visibility (cross-platform comparison view).
- **Gap:** coordinate with the existing topic so this replaces/enriches rather than competes.

### B4. State of AI Search Visibility — recurring research report (pillar)
- **Primary keyword:** "state of ai search" / "ai search visibility study"
- **Intent:** authority/citation asset; top of the cluster
- **Angle:** Bundle both studies into a flagship, datable report; refresh quarterly. The asset that gets *Search Atlas itself* cited by AI engines — meta-proof the tool works.
- **Grounded facts:** both proof studies above.
- **Product tie:** LLM Visibility + Domain Power.
- **Gap:** none to start; future editions need fresh data pulls.

### B5. How to run an AI visibility audit in Search Atlas (workflow)
- **Primary keyword:** "ai visibility audit"
- **Intent:** process / how-to → tool
- **Angle:** Product-led workflow version of the generic "AI auditing checklist" already on the list — distinct because it's the SA-tool workflow.
- **Grounded facts:** `products/llm-visibility.md` data views and capabilities.
- **Product tie:** LLM Visibility (center stage).
- **GAP:** same as B1 — needs tool walkthrough detail before drafting.

---

## Research library → blog translation (the backbone of this cluster)

Search Atlas has a **published research hub**. Several reports are already live. The content play for the product-led group is to translate each report into a practitioner-facing, search-optimized blog piece that ranks for queries the academic report does not target and links back to the full report. This is fully grounded (the data is owned and public) and lower-risk than producing new research.

| Published report | Translates to | Cluster piece |
|---|---|---|
| Relationship Between Domain Power, DR, DA and LLM Visibility Score in Citations | "Does domain authority affect AI citations?" | **B2** |
| How GPT Results Differ from Search Engine Results | "Why AI platforms show different results" | **B3** |
| A Comparative Evaluation of LLM Responses (Gemini, OpenAI, …) | per-platform citation behavior | B3 / new |
| From SEO to GEO: Quantifying Visibility Redistribution Across 61 Industries | flagship "State of AI Search Visibility" | **B4** pillar |
| The Limits of Schema Markup for AI Search | corrects the "schema fixes AEO" assumption (existing schema topics) | new |
| URL Freshness in LLM-Generated Answers | content-freshness-for-AI piece | new |
| How LLMs Rank Local Businesses ("near me") | local AEO / GBP visibility | new |
| Domain Industry Analysis in LLM Responses | industry/vertical AI visibility | feeds vertical pieces |
| From Links to Lift: Real-World SEO Impact of Domain Strength | Domain Power explainer | supports B2 |
| Do LLMs Retain or "Leak" Retrieved Knowledge | advanced / thought-leadership | later |

**Rule for all of these:** link the canonical report, match its findings exactly, and frame as "Search Atlas research found…" — never as new/unreleased research. Pull each live report URL before drafting; do not invent URLs.

## Grounding gaps to close before drafting (summary)

1. **AI-visibility-native competitor knowledge is missing** (Profound, Otterly, Peec, Scrunch/Athena, etc.). Blocks A3 and any honest roundup. Requires new research + `raw/knowledge/competitors/` files. **No invention.**
2. **Competitor files are dated 2026-04-22.** Re-verify Semrush/Ahrefs AI-visibility features before publishing A1/A2.
3. **LLM Visibility tool UI/setup steps not documented.** Blocks B1/B5 drafting until a product SME walkthrough or docs are available.

## Recommended brief order
1. **B2** (original research — fully grounded, highest value, no gaps)
2. **A1** (Semrush comparison — grounded, just needs re-verify)
3. **B1** (setup walkthrough — directly fixes Sophia's problem; unblock with SME first)
4. **B4** (research pillar) → then A2, A4, B3, B5; A3 last (blocked on competitor research).
