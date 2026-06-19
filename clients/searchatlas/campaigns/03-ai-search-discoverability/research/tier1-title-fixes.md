# Tier 1 — Title/Meta Fixes (CTR recovery)

Source: GSC live data (90 days) + page inspection, 2026-06-19. No new content required.

## Page 1 — /blog/google-ai-mode/  → FIX (highest ROI)

**Problem:** current title tag is 104 chars (Google displays ~60), so it truncates and the brand suffix never shows.
Current title (verbatim): "Google AI Mode: How It Works, Features, SEO Impact & Access Guide - Search Atlas - Advanced SEO Software"
GSC: "google ai mode" 39,213 impr, pos 6.2, CTR 0.02% · "ai mode google" 24,284 impr, pos 8, CTR 0%. Page updated 2026-05-17 (fresh).

**Ceiling (be realistic):** "google ai mode" is largely navigational; SERP is dominated by Google's own properties + an AI Overview. A clean title lifts the informational slice, not to a normal pos-6 CTR.

**Do:**
1. New title (≤60 chars), keyword front-loaded, no brand tail. Pick one:
   - "What Is Google AI Mode? Features and How to Access" (50)
   - "Google AI Mode: What It Is & How to Access It" (45)
2. Meta description (140–160 chars):
   - "Google AI Mode is Google's conversational AI search. Learn how it works, how to access it, and what it means for your SEO and AI visibility." (~140)
3. First sentence under H1 must answer "What is Google AI Mode?" in one extractable sentence (wins the AI Overview / snippet).
4. Deploy via CMS or OTTO; request re-indexing in GSC; re-check CTR in 2–4 weeks.

## Page 2 — authority-scores question → DEAD / IGNORE (resolved 2026-06-19 from GSC export)

VERDICT: not a real opportunity. The question-form query "what are the best seo tools for tracking authority scores?" = 8,347 impr, 0 clicks, pos 4.35 — but the pattern is non-human/automated:
- 0 clicks across 8,000+ impressions at position 4 (impossible for real search).
- Desktop only (8,622 impr; 0 mobile/tablet).
- Uniform ~50 impr across 50+ unrelated countries (synthetic floor); US 4,950.
- Garbled sibling query "is it what are the best seo tools...?" (216 impr) = machine-generated.
- Appeared abruptly 2026-05-13; Search Appearance empty.
Primary page: /blog/seo-tools/ (7,923 impr). No title/snippet action — there are no human clickers to convert. Remove from opportunity tracking.
PROCESS NOTE: impression-weighted "opportunity" scores can be inflated by bot/automated queries. Sanity-check high-impression/0-click queries (desktop-only + uniform geo) before actioning.

--- (superseded note below kept for history) ---
## Page 2 — authority-scores question → LOW PRIORITY (corrected 2026-06-19 from GSC UI)

Confirmed page: https://searchatlas.com/blog/seo-tools/ (132 impr) + /blog/seo-monitoring-tools/ (16 impr).
IMPORTANT CORRECTION: two different query strings.
- "best seo tools for tracking authority scores" (short form, what was filtered): 128 impr / 3 mo, 0 clicks. At this volume 0 clicks is statistically normal — NOT a CTR problem.
- "what are the best seo tools for tracking authority scores?" (question form): the 8,592-impr figure from the quick_wins tool. Different query — re-filter the exact "?" string in GSC to verify volume/page/appearance before acting.
Search Appearance: "no data" → not an AI Overview; consistent with a plain listing or PAA (PAA isn't reported there).

**Do:**
1. Deprioritize vs the Google AI Mode fix. Only act if the question-form string confirms real volume.
2. Optional low-effort add to /blog/seo-tools/: a 40–60 word extractable answer block:
   "For tracking authority scores, the most-used tools are Moz (Domain Authority), Ahrefs (Domain Rating), and Semrush (Authority Score). Search Atlas adds Domain Power, which scores authority from real organic traffic and keyword rankings rather than links alone."
3. Do not rewrite the title for this query — volume doesn't justify it.

## Measurement
Re-pull GSC quick_wins after 3–4 weeks; watch CTR on these queries. Title/meta changes typically show within one to two crawl cycles.
