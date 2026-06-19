**Title tag:** Does Domain Authority Affect AI Citations? | Search Atlas
**Meta description:** Domain authority doesn't predict AI citations. A Search Atlas study of 21,767 domains shows why DA and DR fail, and what to track for ChatGPT and Perplexity instead.

# Do Domain Authority Metrics Predict AI Citations?

*By the Search Atlas research team. Based on the study "Relationship Between Domain Power, Domain Rating, Domain Authority and LLM Visibility Score in Citations" by Manick Bhan.*

Domain authority metrics, Moz's Domain Authority (DA) and Ahrefs' Domain Rating (DR), score a site's backlink-based ranking strength. They do not reliably predict whether ChatGPT, Perplexity, Gemini, or Claude will cite a page. A Search Atlas analysis of 21,767 domains found slightly negative correlations between these metrics and AI visibility. The gap matters because the signals that earn backlinks are not the signals that earn AI citations.

## Do domain authority metrics predict AI citations?

Domain authority metrics do not predict AI citations. Across 21,767 domains carrying DA, DR, and Domain Power scores, higher authority did not raise the odds of a citation; it tracked with a small decline in both AI visibility (whether a domain appears in AI answers) and win rate (how often a domain is the cited source when it does appear).

Domain Power is Search Atlas's authority metric, a single score that aggregates organic traffic, keyword performance, and backlink trust rather than raw link volume alone. All three metrics, DA, DR, and Domain Power, behaved the same way against AI visibility: no positive signal.

For teams that allocate budget by DA or DR, the metric they trust most says little about whether AI engines will cite them.

## What the data shows: DA, DR, and Domain Power vs LLM citations

The data shows no positive relationship between authority metrics and AI citations across any of the three scores. The correlations were slightly negative for both visibility and win rate, and the effect held at scale rather than appearing only in a small sample.

### The 21,767-domain correlation finding

The study analyzed 21,767 unique domains carrying DR, DP, and DA metrics, with data collected between August 25 and October 24, 2025. All three authority metrics showed slightly negative correlations with LLM visibility. A separate set of 368,972 unique domains with visibility scores of 50 to 100% supported the same conclusion at scale.

The direction is what disqualifies authority as a predictor: not a weak positive link, but a small negative one. Authority and AI citation move slightly in opposite directions.

### Why win rates decline across every authority range

Win rates declined across every authority band, not only at the top. A domain in a high DA range was no more likely to be the cited source than one in a lower band, and often slightly less likely. This rules out a threshold effect where authority starts to matter past a certain score.

Pushing DA or DR higher therefore does not convert into more citations at any point on the scale.

## Why high-authority sites still appear to win (the competition-tier effect)

High-authority sites often appear to win because of low competition in the answer, not their authority. Visibility falls as co-mention competition rises, meaning the number of other domains cited in the same AI answer: responses citing one or two domains hold consistently higher visibility than responses competing against six or more.

Two platform patterns show the effect, per the study's platform-level breakdown. Google held close to 100% visibility when it was the sole cited domain. YouTube kept 90 to 100% visibility across low-to-mid competition, where one to five domains appeared.

A recognizable brand tends to surface in sparse-citation answers, which reads like an authority advantage but is a competition advantage. The lever is how crowded the answer is, not how strong the domain is. Raising DA will not help when the query returns a crowded, multi-domain answer.

## Why legacy authority metrics fail to predict AI citations

AI engines select sources by relevance, not authority, which is why backlink-based scores miss. An engine assembles an answer from passages that fit the query, then weights which domains stay visible by how few others compete in that response. The study describes this behavior as relevance-driven rather than authority-driven.

Backlink-based scores were built for a different mechanism. They estimate how a page ranks in a list of results, where link trust accumulates across the whole domain. AI answers do not return a list; they return a synthesized response drawn from a small set of relevant passages.

### What backlinks measure vs what retrieval rewards

Backlinks measure endorsement across domains; AI retrieval rewards contextual relevance and co-mention within a single answer.

| Signal | What backlinks measure | What AI retrieval rewards |
|---|---|---|
| Unit | Links from other domains | Fit of a passage to the query |
| Authority basis | Aggregate link trust over a domain | Contextual relevance plus co-mention frequency |
| Competition | Domain against domain in a ranked list | Domains co-cited inside one answer |
| What you act on | Earning more and better links | Being the clearest relevant source for the prompt |

The two systems reward different work, so a strong backlink profile does not carry over into citation odds.

### What actually predicts citation: visibility signals, co-mentions, response prominence

Contextual relevance and low co-mention competition predict citation, not link authority. A page is cited when its content matches the query closely and when the answer it lands in cites few competing domains. Prominence within that answer, whether the domain is one of one or one of eight, then drives how often it holds visibility.

Platforms retrieve differently, so a domain cited on one engine can be absent on another. Citation is a per-platform, per-query outcome, not a single domain-wide score.

## What to track instead of DA/DR

Track AI visibility signals directly instead of authority proxies. The following sequence replaces a DA or DR target with measures tied to how engines actually cite.

1. **Measure cross-platform visibility per query.** Check whether your domain appears in answers on ChatGPT, Perplexity, Gemini, and Claude for your target prompts. This shows where you are absent and which prompts to act on first.
2. **Track share of voice against co-mentioned domains.** Record which competitors appear in the same answers and how often. Share of voice within the answer set reflects your real position better than any domain score.
3. **Count co-mention competition for each prompt.** Note how many domains a typical answer cites for the query. Prompts that return one or two sources are higher-value targets than crowded ones.
4. **Monitor sentiment by platform.** Read how each engine frames your brand, since a citation paired with negative framing changes its value. Sentiment varies by model, so record it per platform.
5. **Re-check on a weekly cadence.** Re-run the same prompts weekly, because AI answers shift faster than search rankings. A citation captured once is not a citation held.

Each step produces a citation outcome you can act on the same week you measure it.

## How Search Atlas measures AI citation behavior

Search Atlas measures AI citation behavior through its LLM Visibility tool, which tracks how often a brand is cited across ChatGPT, Claude, Gemini, and Perplexity and its share of voice against the competitors cited alongside it. It scores visibility per platform, so the per-platform variance described above appears as separate readings rather than one blended number.

The tool groups the domains co-cited alongside a brand, which turns co-mention competition, the factor the study identifies as decisive, into a share-of-voice figure against named competitors. Sentiment tracking shows how each engine frames the brand, and topic-level views show which subjects a brand is cited for. The full dataset and method are documented in the Search Atlas study on the [relationship between Domain Power, Domain Rating, Domain Authority, and LLM visibility](https://searchatlas.com/research/relationship-between-domain-power-domain-rating-domain-authority-and-llm-visibility-score-in-citations/).

## Frequently asked questions

### Should I stop building backlinks for AI search?

No. Backlinks still build search ranking and crawl access, but they do not raise AI citation odds on their own. Treat them as ranking infrastructure, not a citation lever.

### Can a low-authority site get cited by AI?

Yes. Because engines select sources by relevance and co-mention competition, a low-DA page that matches the query closely can be cited ahead of a high-authority site.

### Does a higher Domain Rating improve ChatGPT or Perplexity citations?

No measurable improvement. The 21,767-domain analysis found slightly negative correlations between DR and AI visibility, so raising DR does not predict more citations.

### How is AI visibility different from search ranking?

Search ranking places a domain in a list of results; AI visibility is whether and how often a domain is cited inside a synthesized answer. AI visibility is scored per platform and per query, not as one domain-wide number.

### Why do citations vary between AI platforms?

Each platform pulls from different sources and indexes, so the same query can return different citations on ChatGPT, Perplexity, and Gemini. Track each engine separately rather than assuming one result represents all of them.
