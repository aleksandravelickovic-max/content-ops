# 04 — GSC Performance Analysis

**Property:** `sc-domain:searchatlas.com` · **Pulled:** 2026-06-25 · **Source:** standalone GSC MCP (live, exact values)
All numbers are facts from GSC. Causes are split into **[evidence]** (supported by the data) and **[inference]** (my reading, not proven by GSC).

---

## 1. Headline: clicks are flat, impressions are deflating, and brand carries the site

| Window | Clicks | Δ | Impressions | Δ | Avg pos | CTR |
|---|---|---|---|---|---|---|
| 28d vs prior 28d | 13,919 | **−15.2%** | 4.97M | −12.5% | 27.1 (↑ from 31.8) | 0.28% |
| 90d vs prior 90d | 45,767 | **+1.6%** | 17.16M | **−37.9%** | 30.9 (↑ from 39.3) | 0.27% |
| 178d (H1-26 vs H2-25) | 90,061 | **−33.2%** | 43.9M | **−65.6%** | 35.1 | 0.21% |
| 365d YoY | 232,303 | **+151%** | 176.8M | +270% | 33.4 (↑ from 44.7) | 0.13% |

**What this means:**
- **YoY the site is far bigger** (+151% clicks) — a real 2025 growth surge, almost certainly from publishing/programmatic scale [inference: the 22,340-query footprint and machine-phrased "how does ahrefs X" long-tail point to scaled AI-assisted output].
- **But growth has reversed in 2026.** H1-2026 clicks are −33% vs H2-2025 and impressions −66%. The last 28 days are −15% clicks. The peak was late 2025.
- **Impressions are collapsing faster than clicks** (−38% over 90d while clicks held +1.6%, and average position *improved* 39.3→30.9). [evidence] This is the low-value long tail compressing — pages ranking at position 40–50 on head terms losing impressions without losing clicks they never earned. [inference] Likely a mix of the May/Mar/Dec 2026 Google core updates trimming thin AI-scaled pages and normal decay of over-extended programmatic content.
- **Net read:** the site is not in free-fall on clicks, but it is past its impression peak and the recent click trend is negative. The job for Q3 is to convert quality non-branded demand and stop the click bleed on commercial pages — not to chase more impressions.

## 2. Branded vs non-branded — the central tension

- **Branded queries dominate clicks.** "search atlas" (11,973) + "searchatlas" (2,891) = **14,864 clicks/90d from two queries alone** — ~32% of all 45,767. Adding navigational/brand variants (login, careers, pricing, otto seo 1,468, atlas brain, "manick bhan course" ~1,345, dozens of misspellings) puts branded at an **estimated 48–57% of all clicks** *(estimate — exact split needs full query export)*.
- **Non-branded converts a tiny fraction of a vast impression base.** The biggest non-branded head terms sit at the bottom of page 4–5: `rank-tracking-tools` 1.1M impr @ pos 48 (0% CTR), `seo-tools` 576k @ 50, `competitor-analysis-tools` 575k @ 35, `on-page-seo` 185k @ 45, `seo` 98k @ 48. [evidence] These contribute ~nothing in clicks despite enormous impressions.
- **Strategic implication:** Search Atlas owns its brand SERP and converts it well. The growth lever is **non-branded commercial and AI-search demand where SA already ranks 4–20**, not the head terms it ranks 35–50 for. Brand strength also means comparison/"vs" queries (semrush vs search atlas, ahrefs vs search atlas) already convert at 50–93% CTR — a defensible BOFU asset class to expand.

## 3. Quick wins — positions 4–15 with real impressions (90d)

The richest seam is **commercial "automation/agency/AI software" intent**, where SA ranks 6–14 but barely clicks:

| Query | Impr | Pos | Clicks | Read |
|---|---|---|---|---|
| seo automation platform | 6,027 | 6.3 | 21 | [evidence] Near page-one on core product intent. Title/snippet + product-page link. |
| automated seo software | 9,762 | 8.8 | 12 | High-intent; OTTO page already ranks. Strengthen. |
| seo automation / seo automation tools/software | 9,597 / 8,694 / 5,764 | 9.7–11.5 | 17–24 | Whole "automation" family within reach. |
| seo software for agencies / agency seo software | 11,184 / 9,126 | 13.6 / 10.2 | 24 / 20 | Agency intent — build white-label/agency hub. |
| ai seo software | 12,811 | 13.5 | 7 | Strategic 2026 term; weak CTR. |
| local citation builder / seo citation builder | 9,566 / 6,890 | 6.9 / 7.1 | 5 / 2 | Product page ranks; CTR near zero — snippet fix. |
| site explorer | 16,969 | 7.2 | 40 | Product term; CTR 0.24%. |
| google ai mode / ai mode google | 39,213 / 24,284 | 6.2 / 8.0 | 8 / 1 | Huge impressions, ~0 CTR. News-owned SERP (low feasibility for evergreen — see file 09). |
| automated internal links | 4,830 | 4.9 | 0 | Page-one, zero clicks — pure snippet problem. |
| schema markup generator | 5,820 | 9.6 | 3 | Product/tool intent. |

[inference] The pattern: SA ranks where it has product fit (automation, agency, citations, site explorer) but loses the click on a weak title/snippet. Many of these are **CTR problems, not ranking problems** — see §5.

## 4. Decline diagnosis (evidence vs inference)

GSC's own diagnosis field is used; my read is labeled [inference].

| Page | Δ clicks 90d | GSC diagnosis [evidence] | Likely cause [inference] | Action |
|---|---|---|---|---|
| /otto-seo/ | −574 | Impression decline | Demand cooling / core-update trim on flagship product page | Refresh, protect |
| /blog/ahrefs-review/ | −544 | Impression decline | Content decay + competitor freshness; 136k impr @ 0.12% CTR | Refresh (high value) |
| /da-checker/ | −214 | Impression decline | Free-tool query volatility | Refresh, reframe to Domain Power |
| /otto-google-ads/ | −180 | Impression decline | — | Refresh; ties to "every channel" pillar |
| /blog/perplexity-ai-alternatives/ | −178 | **Ranking loss** (7→11.7) | **Cannibalization** with /perplexityai-alternatives/ | Consolidate |
| /blog/holistic-seo/ | −100 | **Ranking loss** (9.3→19.5) | Content decay; lost page-one | Refresh |
| /white-label-seo-software/ | −100 | **Ranking loss** (26→32.7) | Thin vs entrenched white-label SERP | Expand into hub |
| /blog/best-ai-tools/ | −87 | Impression decline | Cannibalizes "google ai mode" | Reposition/monitor |
| /enterprise-agency/ | −83 | CTR collapse (pos stable) | Weak snippet | Reposition into agency hub |
| /blog/seo-vs-sco/ | −30 | **Ranking loss** (5.8→10.3) | AI-search cluster decay | Refresh |
| /llm-visibility/ | −26 | CTR collapse | Orphaned product page, weak snippet | Refresh + cluster links |
| /latest-updates/ | −23 | **Disappeared** from results | De-indexed / removed | Investigate (technical) |

**No AI-Overview-displacement claim is made** — GSC cannot confirm it, and SA's own AI-citation tracking for its domain is not wired up (file 02 §2). The displacement risk is real per the trend research (file 08, AIO −58% CTR) but is **inferred, not measured here**.

## 5. CTR opportunities — the fastest Q3 wins (title/meta only)

These pages already rank well; they lose clicks on the snippet. Estimated recoverable clicks from `ctr_opportunities` (90d):

| Page | Impr | Pos | CTR | Est. recoverable clicks |
|---|---|---|---|---|
| /features/ | 190,063 | 7.3 | 0.05% | **~7,515** |
| /case-studies/ | 108,802 | 7.2 | 0.03% | ~4,318 |
| /pricing/ | 248,717 | 11.7 | 0.49% | ~4,153 |
| /blog/google-ai-mode/ | 81,484 | 6.6 | 0.02% | ~4,140 |
| /blog/perplexityai-alternatives/ | 78,103 | 6.3 | 0.20% | ~3,826 |
| /blog/what-is-chatgpt/ | 101,252 | 8.5 | 0.04% | ~3,195 (low ICP) |
| /blog/ahrefs-features/ | 168,118 | 9.4 | 1.16% | ~2,763 |
| /blog/blog-setup/ | 31,110 | 5.4 | 0.11% | ~2,206 |
| /blog/chatgpt-vs-claude/ | 12,476 | 3.2 | 0.10% | ~1,359 (low ICP) |
| /blog/seobility-vs-semrush/ | 20,007 | 6.1 | 0.01% | ~1,018 |

[inference] Several blog pages show **0% CTR at positions 3–6** (buzzsumo-vs-ahrefs pos 5.5, automated-internal-links pos 4.9). That is not normal — it points to FAQ-anchor URLs and rich-result fragments absorbing impressions, or titles that don't match the query. A **site-wide title/meta + snippet audit on the top-30 high-impression / low-CTR pages is the single highest-ROI, lowest-effort Q3 workstream.** Caveat: `/features/`, `/about-us/`, `/careers/` "gaps" are partly navigational/brand noise — real recoverable upside is lower than the raw number for those three.

## 6. Geography & device

- **88% of clicks are desktop** (40,346 vs 5,266 mobile) — a professional/B2B audience. Content and CTAs can assume a desk, not a phone.
- **US is 53% of clicks** and the commercial core. India/Pakistan/Philippines show high CTR but on free-tool/course/how-to intent (low commercial value). [inference] Don't optimize the commercial portfolio for the high-CTR South-Asian long tail; it inflates click counts without pipeline.

## 7. What the data says to do in Q3 (carried into files 10–13)

1. **Fix snippets before writing anything new.** §5 alone is multiple thousands of clicks at near-zero effort.
2. **Consolidate cannibalized clusters** (file 06) — duplicate alternatives/review pages are splitting equity.
3. **Refresh decaying high-value commercial pages** (otto-seo, ahrefs-review, white-label, llm-visibility) before net-new.
4. **Build the AI-Search cluster properly** — it already ranks (aeo, geo, aio, agentic) and matches the 2026 demand shift; it just lacks a hub, internal links, and tool routing (file 07, file 14).
5. **Push the "automation / agency / AI software" commercial family** from page-2 to page-1 — best demand-to-feasibility ratio on the site.
