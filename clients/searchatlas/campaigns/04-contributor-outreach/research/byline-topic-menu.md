# Contributor Byline Hand-Off — Search Atlas

Hand-off for the martech contributor outreach (25 email-reachable pubs). This is the source material and topic menu for vendor-neutral expert bylines. Use it to write the per-pub pitches.

## Byline guardrails (read first)

- **No Search Atlas promotion.** No product names, no "we built," no CTAs. These are expert articles, not ads. Premium editors reject vendor copy on sight.
- **Lead with original data.** Every topic below is anchored to a real Search Atlas study (sample size + finding). The data is the credibility — it's what earns the byline. Cite the finding; the byline author is the expert reading the data, not a vendor selling.
- **Author = a Search Atlas analyst/expert**, attributed as a practitioner. The brand can appear in the bio line only (most pubs allow one), never in the body.
- **One study per article.** Don't stack. Each piece makes one data-backed argument.

## Source material (the studies these articles draw from)

All published at `https://searchatlas.com/research/`. Full text in the repo:

| Study | Sample | Headline finding | File |
|---|---|---|---|
| LLM visibility / domain power | 21,767 domains | DA/DR do **not** predict whether LLMs cite you; LLM citation is relevance-driven | `raw/knowledge/proof/domain-power-llm-visibility-study.md` |
| GPT vs Google search | 18,377 matched query pairs | ChatGPT/Gemini/Perplexity pull from measurably different sources than Google SERPs | `raw/knowledge/proof/gpt-vs-search-study.md` |
| Links to lift | 350,159 backlinks / 13,002 pages | Strategic placement drove +275% impressions, +150% ranking keywords, +14% clicks | `raw/knowledge/proof/domain-power-study.md` |
| Automated technical SEO | 39,876 sites | Schema fixes +150.5% impressions; heading fixes +114.3%; median +146 long-term impressions/site | `raw/knowledge/proof/otto-seo-fixes-study.md` |
| Local ranking dynamics | 7,718 businesses / 676 sectors | Distance-to-searcher dominates local ranking variance; weight differs sharply by sector | `raw/knowledge/proof/gbp-galactic-study.md` |
| Ad automation | tens of thousands of campaigns | Automated ads hit 6.8% CTR vs 5.9% manual; −9% CPC | `raw/knowledge/proof/smart-ads-study.md` |
| Crawl frequency / topical signals | LLM visibility dataset | Crawl frequency + topical signals drive LLM citation; entity weighting matters | `raw/knowledge/proof/scholar-study.md` |

## Topic menu (vendor-neutral, data-anchored)

| # | Working title | Anchored study | One-line angle |
|---|---|---|---|
| T1 | Why domain authority doesn't predict whether AI cites you | LLM visibility | 21,767 domains show DA/DR are weak signals for LLM citation — relevance wins |
| T2 | What 18,000 queries reveal about AI search vs Google | GPT vs Google | AI engines and Google surface different sources; one SEO strategy won't cover both |
| T3 | What link placement actually moves (and what it doesn't) | Links to lift | 350K backlinks measured: where placement helped impressions vs where it didn't |
| T4 | The technical SEO fixes that actually move impressions | Automated technical SEO | Across 39,876 sites, which fixes paid off most — ranked by measured lift |
| T5 | What really drives local pack rankings, by sector | Local ranking dynamics | Distance dominates, but the weight swings by industry — data across 676 sectors |
| T6 | Does ad automation beat manual campaign management? | Ad automation | CTR and CPC data comparing automated vs manual paid search |
| T7 | How to get your content crawled and cited by LLMs | Crawl frequency | Crawl cadence + topical signals that correlate with LLM citation |
| T8 | GEO/AEO: structuring content so AI engines cite it | T1+T2+T7 synthesis | Practitioner guide to answer-engine optimization, grounded in the citation data |
| T9 | How to measure your brand's visibility inside AI answers | LLM visibility | A measurement framework for tracking presence in ChatGPT/Gemini/Perplexity answers |

## Pub → topic mapping (named pubs from the message)

Colleague: apply the same logic to the remaining pubs in `searchatlas_martech_contacts.csv` — match the topic to the pub's audience.

**Verified-high tier**
- MarketingProfs → T3, T8
- CMSWire → T4, T8
- Search Engine Land → T1, T2, T4, T5 (most flexible — pick the freshest)
- MarTech.org → T1, T6, T7
- G2 → T1, T9
- CustomerThink → T9, T8

**Medium-confidence tier**
- Search Engine Journal → T1, T2, T3, T5
- Adweek → T6 (paid/brand angle)
- Marketing Dive → T6, T2
- Content Marketing Institute → T8, T9
- B2B Marketing → T8, T9
- Marketing AI Institute → T1, T2, T7
- ClickZ → T2, T6
- Unite.AI → T1, T2, T7

**Form-only (separate manual-submit batch, not in the mail-merge)**
- jeffbullas.com, socialmediatoday.com, unboundb2b.com → T8/T9 (general practitioner angles)

## What's still open
- Map the remaining email-reachable pubs (full list in the CSV) to topics above.
- Verify the 13 medium-confidence emails before sending (`dpr_verify_contacts`).
- Confirm author/bio attribution allowed per pub (CSV submission rules column).
