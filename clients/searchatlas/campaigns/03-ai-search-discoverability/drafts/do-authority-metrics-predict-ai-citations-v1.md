<!-- DRAFT FLAGS (not for publication body):
- Internal knowledge (products/domain-power.md) says the study recalibrated Domain Power; the public report does not. Recalibration claims omitted from study sections.
- Product section describes LLM Visibility at capability level (raw/knowledge/products/llm-visibility.md); no in-product UI/steps asserted.
- Internal-link slots: only the canonical research report URL supplied. Add a live LLM Visibility tool page URL at publish.
- Length: body ~1,650 words after FAQ. Below the 1,800-2,500 target; not padded per CLAUDE.md no-filler rule. Flagging for editor decision.
-->

# Do Domain Authority Metrics Predict AI Citations?

Domain authority metrics, Moz's Domain Authority (DA) and Ahrefs' Domain Rating (DR), score a site's backlink-based ranking strength. They do not reliably predict whether ChatGPT, Perplexity, Gemini, or Claude will cite a page. A Search Atlas analysis of 21,767 domains found slightly negative correlations between these metrics and AI visibility. The gap matters because the signals that earn backlinks are not the signals that earn AI citations.

## Do domain authority metrics predict AI citations?

Domain authority metrics do not predict AI citations. Across 21,767 domains carrying DA, DR, and Domain Power scores, Search Atlas found slightly negative correlations between authority and both AI visibility and win rate. Higher authority did not raise the odds of a citation; in the data, it tracked with a small decline.

Domain Power is Search Atlas's authority metric, weighted by SERP-sourced traffic and keyword reach rather than raw link counts. All three metrics, DA, DR, and Domain Power, behaved the same way against AI visibility: no positive signal.

For teams that allocate budget by DA or DR, this means the metric they trust most says little about whether AI engines will cite them.

## What the data shows: DA, DR, and Domain Power vs LLM citations

The data shows no positive relationship between authority metrics and AI citations across any of the three scores. The pattern held for visibility (whether a domain appears in AI answers) and for win rate (how often it is the cited source when it does appear).

### The 21,767-domain correlation finding

The study analyzed 21,767 unique domains carrying DR, DP, and DA metrics, with data collected between August 25 and October 24, 2025. Search Atlas research, led by founder Manick Bhan, found slightly negative correlations between all three authority metrics and LLM visibility. A separate set of 368,972 unique domains with visibility scores of 50 to 100% supported the same conclusion at scale.

The direction is the point: not a weak positive link, but a small negative one. Authority and AI citation move slightly in opposite directions, which removes authority as a usable predictor.

### Why win rates decline across every authority range

Win rates declined across every authority band, not only at the top. A domain in a high DA range was no more likely to be the cited source than one in a lower band, and often slightly less likely. This rules out a threshold effect where authority starts to matter past a certain score.

For practitioners, this closes off the assumption that pushing DA or DR higher will convert into more citations at any point on the scale.

## Why high-authority sites still appear to win (the competition-tier effect)

High-authority sites often appear to win because of low competition in the answer, not their authority. Visibility falls as the number of co-mentioned domains in an AI response rises: answers citing one or two domains hold consistently higher visibility than answers competing against six or more.

Two platform patterns show the effect. Google held close to 100% visibility when it was the sole cited domain. YouTube kept 90 to 100% visibility across low-to-mid competition, where one to five domains appeared.

A recognizable brand tends to surface in sparse-citation answers, which reads like an authority advantage but is a competition advantage. The lever is how crowded the answer is, not how strong the domain is. Raising DA will not help when the query returns a crowded, multi-domain answer.

## Why legacy authority metrics fail to predict AI citations

Legacy authority metrics fail because AI engines select sources by relevance, not authority. The study describes the behavior as relevance-driven rather than authority-driven: an engine assembles an answer from passages that fit the query, then weights which domains stay visible by how few others are competing in that response.

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

Platforms retrieve differently, so a domain cited on one engine can be absent on another. Citation is therefore a per-platform, per-query outcome, not a single domain-wide score.

## What to track instead of DA/DR

Track AI visibility signals directly instead of authority proxies. The following sequence replaces a DA or DR target with measures tied to how engines actually cite.

1. **Measure cross-platform visibility per query.** Check whether your domain appears in answers on ChatGPT, Perplexity, Gemini, and Claude for your target prompts. This tells you where you are absent, which a DA score cannot.
2. **Track share of voice against co-mentioned domains.** Record which competitors appear in the same answers and how often. Share of voice within the answer set, not domain authority, reflects your real position.
3. **Count co-mention competition for each prompt.** Note how many domains a typical answer cites for the query. Prompts that return one or two sources are higher-value targets than crowded ones.
4. **Monitor sentiment by platform.** Read how each engine frames your brand, since a citation paired with negative framing changes its value. Sentiment varies by model, so track it per platform.
5. **Re-check on a weekly cadence.** Re-run the same prompts weekly, because AI answers shift faster than search rankings. A citation captured once is not a citation held.

Each measure ties to a citation outcome you can act on, which a static authority score does not provide.

## How Search Atlas measures AI citation behavior

Search Atlas measures AI citation behavior through its LLM Visibility tool, which identifies brand mentions, tracks sentiment shifts, and surfaces visibility gaps across ChatGPT, Claude, Gemini, and Perplexity. It reports visibility trends, share-of-voice metrics, cross-platform ranking comparisons, sentiment patterns, and topic-level performance, with cross-model scoring and competitor benchmarks in one view.

Because the tool scores visibility per platform and groups citation sources and co-mentioned competitors, it tracks the signals the data identifies as predictive, relevance and competition, rather than the authority metrics that do not predict citations. The full dataset and method are documented in the Search Atlas study on the [relationship between Domain Power, Domain Rating, Domain Authority, and LLM visibility](https://searchatlas.com/research/relationship-between-domain-power-domain-rating-domain-authority-and-llm-visibility-score-in-citations/).

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

Platforms retrieve sources differently, so a domain cited on one engine can be absent on another. Citation is a per-platform outcome rather than a single domain-wide score.
