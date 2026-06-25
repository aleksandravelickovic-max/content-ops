# 11 — Q3 2026 Content Portfolio

Balanced portfolio derived from the scorecard (file 10), sequenced refresh/consolidation-first per the brief. Each asset lists the spec fields in condensed form; the **top 10 (★) have full briefs in file 13**.

**Approved capacity (Aggressive):** 10 net-new long-form + 6 substantial refreshes + 12 light optimizations / month; 3 data-led assets / quarter. **Q3 ceiling: 30 net-new, 18 refreshes, 36 light, 3 data-led.**

**This plan uses:** 14 net-new long-form, 9 substantial refreshes, ~30 light optimizations, 3 data-led — **well inside capacity.** Headroom is deliberately reserved for (a) re-running failed QA pieces per IMPROVEMENT-LOOP.md, (b) the blocked assets (O22/O28) once unblocked, and (c) the per-SKU/programmatic expansion the pipeline supports. Padding to the ceiling with thin net-new would contradict the core finding (impression deflation from over-scaling) — see file 04.

---

## A. Refresh backlog (do first — recovers existing equity)

| ★ | Asset | Target URL | Primary query | Why | Action | Score | Month | Effort |
|---|---|---|---|---|---|---|---|---|
| | **CTR/snippet sprint** (top-30 high-impr/low-CTR) | /features, /pricing, /case-studies, /blog/google-ai-mode, /blog/ahrefs-features, +25 | mixed | ~25k+ recoverable clicks at near-zero effort (file 04 §5) | Rewrite title+meta+answer snippet; fix FAQ-anchor indexing | 79.6 | Jul | Light×30 |
| ★ | **Refresh LLM Visibility product page** | /llm-visibility/ | llm visibility | Orphaned at pos 26.8, decaying; conversion center of AEO cluster | Refresh + wire cluster links in + tool CTA | 76.8 | Jul | Refresh |
| ★ | **Refresh OTTO SEO page** | /otto-seo/ | otto seo / seo automation | −574 clicks; top product page | Refresh; align to rebrand voice; link from automation hub | 75.8 | Jul | Refresh |
| | **Refresh Ahrefs review** | /blog/ahrefs-review/ | ahrefs review | −544 clicks; 136k impr @ 0.12% CTR | Refresh + **re-verify Ahrefs facts** (file 02) before publish | 64.4 | Jul | Refresh |
| | Refresh white-label page → agency hub | /white-label-seo-software/ | white label seo | −100 ranking loss; anchors 200k+ impr family | Expand into hub (see C) | 74.2 | Aug | Refresh |
| | Refresh OTTO Google Ads | /otto-google-ads/ | otto google ads | −180 clicks; supports "every channel" pillar | Refresh; link to Smart Ads | 64.4 | Aug | Refresh |
| | Refresh DA checker | /da-checker/ | da pa checker | −214 clicks | Refresh; reframe to Domain Power | — | Aug | Refresh |
| | Refresh local pages | /local-seo, /local-seo-software, /google-my-business-management-software | local seo | decay; "GMB"→GBP naming risk | Refresh into local hub (see C) | 63.4 | Sep | Refresh×3 |
| | Refresh holistic-seo, seo-vs-sco | /blog/holistic-seo, /blog/seo-vs-sco | holistic seo / seo vs sco | ranking losses | Refresh; relink to AI-Search hub | 48–62 | Sep | Refresh×2 |

## B. Consolidation backlog (stop equity splitting)

| Asset | Canonical | Action | Score | Month | Effort |
|---|---|---|---|---|---|
| **Perplexity-alternatives dedup** | /blog/perplexityai-alternatives/ | Merge + 301 the /perplexity-ai-alternatives/ duplicate | 68.4 | Jul | Light |
| **Anthropic Claude review dedup** | /blog/anthropic-claude-review/ | Merge + 301 the -2- duplicate | — | Jul | Light |
| **DA cluster → Domain Power pillar** | /blog/domain-power/ | Consolidate 4 URLs into hub-and-spoke; interlink | 72.8 | Aug | Refresh |
| **Anchor-fragment indexing fix** | various | Canonicalize FAQ/anchor fragment URLs sitewide | 56.4 | Jul | Light |
| **De-index labs.searchatlas.com** | n/a | robots/noindex the leaking staging subdomain | 53.0 | Jul | Light (technical) |
| White-label reporting consolidation | /blog/white-label-seo-reporting-tools/ | Consolidate thin reporting pages; link to agency hub | — | Aug | Refresh |

## C. Net-new production

### Pillars / hubs (P0–P1)
| ★ | Asset | Primary query | Cluster | Product tie | Score | Month | Words |
|---|---|---|---|---|---|---|---|
| ★ | **AI Search Discoverability hub** | ai search visibility / aeo | AI-Search | LLM Visibility | 87.2 | Jul | 2,000–2,500 (pillar) |
| ★ | **SEO Automation hub** | seo automation software | SEO Automation | OTTO | 81.0 | Aug | 2,000–2,500 |
| ★ | **Agency / White-Label hub** | seo software for agencies | White-Label-Agency | All / white-label | 74.2 | Aug | 2,000–2,500 |
| | Local SEO hub | local seo software | Local-SEO | GBP Galactic / Local Citations | 63.4 | Sep | 1,800–2,200 |

### Supporting / AI-Search white space (P0–P1)
| ★ | Asset | Primary query | Differentiation / info gain | Score | Month | Words |
|---|---|---|---|---|---|---|
| ★ | **How to track LLM referral traffic (+ free Looker template)** | track llm traffic | The practical GA4/Looker how-to no high-DA brand owns; downloadable template | 87.4 | Jul | 1,800–2,200 |
| ★ | **Agentic SEO execution proof (OTTO before/after)** | agentic seo | Real OTTO execution + before/after data; Ahrefs only mocks "Agent A" | 83.4 | Jul | 1,800–2,400 |
| ★ | **AEO/GEO measurement benchmark (from proof studies)** | aeo geo measurement / ai citation | Original SA proof data; rivals lack case studies | 79.4 | Aug | 1,800–2,500 |
| ★ | **AEO vs GEO vs SEO — one workflow (glossary hub)** | aeo vs geo | Resolves acronym confusion; strong internal-link hub | 77.6 | Jul | 1,800–2,200 |
| | Platform-specific AEO tactics (ChatGPT/Perplexity/AI Mode) | aeo by platform | Per-platform citation differences competitors skip | 76.4 | Aug | 1,800–2,200 |
| ★ | **How B2B buyers shortlist software in 2026** | b2b ai buyer journey | Maps funnel→AI behavior; the AEO sales argument | 74.0 | Aug | 1,800–2,200 |
| | Agentic marketing pillar expansion | agentic marketing | Two-meanings clarity; flagship Coworker story | 71.8 | Aug | 1,800–2,200 |

### Product-led commercial (P1)
| ★ | Asset | Primary query | Score | Month | Words | Dependency |
|---|---|---|---|---|---|---|
| ★ | **AI SEO software commercial page** | ai seo software | 71.8 | Aug | 1,500–2,000 | — |
| | LLM Visibility setup walkthrough | how to track brand in ai | 71.6 | Sep | 1,500–2,000 | **BLOCKED: product SME/UI docs** |
| | Search Atlas Coworker content (start) | ai marketing coworker | 65.8 | Sep | 1,800–2,200 | — |

### Thought leadership / link-bait (P2)
| Asset | Primary query | Score | Month |
|---|---|---|---|
| ★ What ranking #1 is worth in 2026 (AIO CTR) | ai overview ctr | 66.8 | Aug |
| Zero-click new-KPI framework for agencies | zero-click search | 60.6 | Sep |
| Reddit/community SEO playbook | reddit b2b seo | 59.6 | Sep |

## D. Data-led assets (3/quarter)
| ★ | Asset | Type | Score | Month | Dependency |
|---|---|---|---|---|---|
| ★ | **State of AI Search Visibility report** | Flagship recurring research | 77.6 | Sep | Fresh data pull from proof studies |
| | AEO/GEO measurement benchmark (also in C) | Original research | 79.4 | Aug | proof studies (grounded) |
| | LLM referral-traffic Looker template (also in C) | Interactive/template | 87.4 | Jul | template build (design) |

## E. Distribution / repurposing
| Asset | Action | Month |
|---|---|---|
| Proof-study repurposing | Each owned report → search-optimized blog + LinkedIn + Reddit participation (community-SEO per file 08-T9) | ongoing |
| AI-Search hub assets | Excerpt to LinkedIn/X; pursue G2 + Reddit presence to lift LLM citation (file 08-T7/T9) | ongoing |

## F. Experimental (P3 / blocked)
| Asset | Status | Unblock condition |
|---|---|---|
| AI visibility tools comparison (Profound/Peec/Scrunch) | **BLOCKED** | New competitor research + `raw/knowledge/competitors/` files. No invention. |
| LLM Visibility setup walkthrough | **BLOCKED** | Product SME walkthrough / tool docs |
| Holistic-seo recovery | P3 | Capacity permitting in Sep |

---

## What we should NOT produce in Q3

1. **No new "Ahrefs/Semrush alternatives" roundups** — saturated high-DA tested-listicle layer; incumbents cross-recommend (file 09). Earn inclusion + own branded `/x-alternative` pages instead.
2. **No more AI-tools-reviews** (what-is-chatgpt, what-is-claude, what-is-gpt-4o) — off-ICP, high impressions but near-zero conversion. Harvest existing CTR via snippets only.
3. **No bare "google ai mode" or "answer/generative engine optimization" head-term plays** — Google/Wikipedia/arxiv/Profound own them. Compete on derivatives.
4. **No net-new foundational SEO head-term pages** (seo, on-page-seo, technical-seo as new) — impression-deflating, low feasibility. Refresh/repurpose only.
5. **No volume AI-generated content without expertise signals** — the May/Mar/Dec 2026 core updates penalize exactly this (file 08-T12); it is the likely cause of SA's own impression decline (file 04). Every piece needs information gain + named author/review.
6. **No padding to the 30-net-new ceiling.** The data says consolidate and deepen, not scale wider.
