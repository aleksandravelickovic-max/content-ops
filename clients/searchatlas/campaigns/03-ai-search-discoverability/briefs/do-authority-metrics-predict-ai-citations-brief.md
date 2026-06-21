# Brief: Do Authority Metrics (DA/DR) Predict AI Citations?

**Client:** SearchAtlas · **Campaign:** 03-ai-search-discoverability · **Piece:** B2
**Primary keyword:** does domain authority affect AI citations
**Secondary:** domain authority AI search, do backlinks matter for AI citations, DA/DR vs LLM citations
**Target length:** 1,900–2,400 words (per SA article-balance rule)
**Type:** research-derived explainer — the practitioner-facing, search-optimized translation of an existing published study (NOT new research)
**Canonical report:** "Relationship Between Domain Power, Domain Rating, Domain Authority and LLM Visibility Score in Citations" — https://searchatlas.com/research/relationship-between-domain-power-domain-rating-domain-authority-and-llm-visibility-score-in-citations/ · by Manick Bhan (Founder, CEO/CTO) · published 2025-11-10. This blog piece summarizes it for search demand and links to the full report.
**SERP verified:** 2026-06-19 (re-verify within 7 days of publish — this SERP shifts weekly)

### Verified report figures (use these exact — confirmed against live report 2026-06-19)
- **21,767** unique domains analyzed with DR, DP, and DA metrics.
- **368,972** unique domains assessed with visibility scores of 50–100%.
- Data collection window: **August 25 – October 24, 2025**.
- Headline: "Domain Power, Domain Rating, and Domain Authority are **not strong predictors** of LLM Visibility" — **slightly/weak negative correlations** with both visibility and win rate.
- Mechanism (verbatim framing): LLMs are **relevance-driven, not authority-driven**. Visibility **falls as the number of co-mentioned domains rises** — responses citing 1–2 domains hold consistently higher visibility than those competing against 6+.
- Platform examples: Google ≈100% visibility when the sole cited domain; YouTube 90–100% across low-to-mid competition (1–5 domains).
- **Do NOT state the study recalibrated Domain Power.** The recalibration appears only in internal knowledge (`products/domain-power.md`), not in the public report. If used, attribute it to the product, not the study — keep it out of the study claims.

---

### 1. Definition-first angle

Domain authority metrics (Moz DA, Ahrefs DR) show a weak-to-negative correlation with whether AI engines cite a page, so they do not reliably predict AI citations — a finding from a Search Atlas analysis of 21,767 domains.

### 2. Search intent breakdown

The reader is an SEO or marketing practitioner deciding whether the authority metrics they have optimized for years still matter now that ChatGPT, Perplexity, and Gemini drive discovery. They are not after a definition of backlinks — they want a defensible yes/no on whether chasing DA/DR is worth the budget, and what to track instead. The job-to-be-done: reallocate effort with evidence, and justify that decision to a manager.

### 3. Content angle

This piece wins on first-party data and mechanism — the two things the live SERP lacks. The data is already published as a Search Atlas research report; this blog version makes it rank for practitioner queries the academic report does not target, and links to the full report as the citable source.

- **First-party data gap (SERP-wide):** Every ranking page runs on fragmented third-party numbers. Ahrefs samples 1,000 domains; ZipTie aggregates ~11 outside studies (Evertune, Yext, Princeton GEO paper) without its own; Yoast cites no data at all. Search Atlas's 21,767-domain correlation study (plus a 368,972-domain competition-tier subset) is larger and more direct than anything ranking. Evidence: ahrefs.com/blog/llm-citations, ziptie.dev, yoast.com.
- **Contradiction the SERP leaves unresolved (partial gap):** Ahrefs claims DR correlation is "indirect but strong" and finds a DR 80–100 citation preference; ZipTie/Evertune claim the opposite — most-cited pages have *fewer* backlinks. No page reconciles these. Our data resolves it: the correlation is weak-negative overall, and the deciding factor is **competition — visibility falls as the number of co-mentioned domains rises** (responses citing 1–2 domains hold higher visibility than those against 6+), which explains why a high-authority site sometimes appears to win. Evidence: ahrefs.com/blog/llm-citations vs ziptie.dev.
- **Mechanism gap (SERP-wide):** ZipTie states the inverse-backlink fact but admits no explanation; its "authority confidence" framework is circular. We explain *why* legacy authority fails to predict citations: LLMs are **relevance-driven, not authority-driven**, so contextual relevance and co-mention competition predict citation, not link-based authority.

Do not write this as another "citations vs backlinks" definitional post — Yoast and keyword.com already own that intent. Lead with the study.

### 4. Proposed structure

- **Do domain authority metrics predict AI citations?**
  → does domain authority affect AI citations
- **What the data shows: DA, DR, and Domain Power vs LLM citations**
  → do backlinks matter for AI citations
  - The 21,767-domain correlation finding
    → is there a correlation between domain authority and AI citations
  - Why win rates decline across every authority range
    → do high authority sites get cited more by AI
- **Why high-authority sites still appear to win (the competition-tier effect)**
  → why do some high DA sites get cited by AI
- **Why legacy authority metrics fail to predict AI citations**
  → why does domain authority not work for AI search
  - What backlinks measure vs what retrieval rewards
    → difference between backlinks and AI citations
  - What actually predicts citation: visibility signals, co-mentions, response prominence
    → what predicts AI citations
- **What to track instead of DA/DR**
  → how to measure AI citation potential
- **How Search Atlas measures AI citation behavior**
  → how to track domain authority and AI visibility together

### 5. Key questions to answer

- Does domain authority affect whether AI engines cite a page?
- Is there a measurable correlation between DA/DR and AI citations?
- Do pages with more backlinks get cited more often by ChatGPT or Perplexity?
- Why do some high-DA sites still get cited if authority does not predict citations?
- What signals actually predict AI citation if not domain authority?
- Should SEO teams stop optimizing for domain authority?

### 6. Entity coverage

- **Domain Authority (DA)** — Moz link-based metric; name the owner, do not use as a generic term.
- **Domain Rating (DR)** — Ahrefs link-based metric.
- **Domain Power** — SearchAtlas proprietary metric; never "domain authority." Recalibrated to weight LLM visibility signals.
- **LLM citation** — a source reference inside an AI-generated answer.
- **Brand mention** — unlinked reference; distinguish from citation and backlink.
- **Retrieval-augmented generation (RAG)** — the mechanism by which engines select sources; explains the disconnect from link authority.
- **LLM Visibility tool** — SearchAtlas product; the tracking answer in the product section only.
- **ChatGPT, Perplexity, Gemini, Claude** — the four platforms the study and tool cover.
- **Manick Bhan** — study author; attribution carries authority.

### 7. Practical section

**H2: What to track instead of DA/DR.** The reader leaves with a concrete shift: stop using DA/DR as a citation proxy, and start tracking cross-platform visibility, share of voice, co-mention frequency, and sentiment per platform. This is the one place the LLM Visibility tool appears — show it measuring citation sources and competitor benchmarks across ChatGPT, Perplexity, Gemini, and Claude. Keep product to this single section (article-balance rule).

### 8. Risks to avoid

- **Overclaiming causation.** The study found correlation, not a causal model. Say "weak negative correlation," not "backlinks hurt citations."
- **Contradicting our own data.** Do not import the SERP's "DR 80–100 gets cited more" claim as fact — our data shows the opposite trend; cite it only as the misconception we are correcting.
- **Inventing study details.** Use only what is in `raw/knowledge/proof/domain-power-llm-visibility-study.md` (sample sizes, findings, product impact). No invented percentages or per-platform breakdowns.
- **"Domain authority" for our metric.** It is Domain Power. DA = Moz, DR = Ahrefs.
- **Drifting into a generic backlinks explainer.** The definitional intent is already owned; this is a data piece.
- **Stale framing.** Date the piece and the data; the SERP and platform behavior move weekly.
- **Re-presenting published research as new.** The study is already public. Frame as "Search Atlas research found…" and link the report; do not imply a fresh/unreleased study.
- **Contradicting the published report.** Findings, sample sizes, and conclusions must match the live report exactly — it is the citable canonical version.

### 9. Answer surface opportunities

- **Definition:** "Domain authority metrics show a weak-to-negative correlation with AI citations, based on a 21,767-domain Search Atlas study" — built to be extracted whole.
- **Q&A pairs:** "Does domain authority affect AI citations?" / "Do backlinks matter for AI citations?" — each section opens with the direct answer for snippet and AI-answer capture.
- **Comparison statement:** "Backlinks measure link endorsement; AI citations reward retrievable, co-mentioned content — the two diverge." Resolves the citations-vs-backlinks query the SERP keeps asking.
- **Stat block:** the 21,767- and 368,972-domain figures and the "declining win rates across all authority ranges" finding — original numbers competitors cannot match, the kind AI engines cite to a named source.

---

### Grounding sources
- `clients/searchatlas/raw/knowledge/proof/domain-power-llm-visibility-study.md` (primary data)
- `clients/searchatlas/raw/knowledge/proof/gpt-vs-search-study.md` (supporting: per-platform divergence)
- `clients/searchatlas/raw/knowledge/products/llm-visibility.md` (product section)
- `clients/searchatlas/raw/knowledge/products/domain-power.md` (Domain Power recalibration)
- SERP reviewed 2026-06-19: ziptie.dev, yoast.com, ahrefs.com/blog/llm-citations, tryprofound.com, keyword.com
