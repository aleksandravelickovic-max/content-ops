# QA Report — SEO Automation Software

Audited: 2026-06-26. Word count: 2,269 (within 2,200–2,800). All issues found were fixed in article.md before sign-off.

## Issues found and fixed
1. **Possessive apostrophe — "Aira's 2025 State of SEO survey."** Contract says avoid possessive apostrophes. FIXED → "The 2025 State of SEO survey from Aira."
2. **Possessive apostrophe — "the brand's own statement."** FIXED → "an official statement from the brand."
3. **Borderline antithesis cadence — "speeds up a person rather than replacing the step."** Reads close to the banned not-X-but-Y rhythm. FIXED → "speeds up a person and leaves the apply step manual." (Two remaining "rather than" uses are plain comparatives, not antithesis; left as-is.)

No other issues required a fix.

## Dimension audit

| Dimension | Result | Notes |
|---|---|---|
| Banned words (delve, leverage, harness, robust, seamless, elevate, unlock, supercharge, game-changing, cutting-edge, best-in-class, navigate, realm, landscape, tapestry, boasts, testament, pivotal, ever-evolving, foster, empower, streamline, holistic, synergy, ensure, establish, engage, align, comprehensive, essential, crucial) | PASS | grep -niE returned zero matches. "best SEO automation tools" appears once inside a quoted SERP phrase referring to competitor list titles, not as a claim. |
| Filler phrases ("in today's world", "when it comes to", "it's worth noting", "dive in") | PASS | None present. |
| Em dashes | PASS | Zero em dashes (grep count 0). Used commas/periods. |
| Antithesis (not X but Y / doesn't just X) | PASS | No antithesis constructions. Two "rather than" comparatives reviewed and cleared. |
| Reflexive triads | PASS | Lists are uneven or functional (capability lists), not three parallel adjectives for cadence. |
| Setup-payoff scaffolding / -ing editorial tails | PASS | No "Here's the thing", "The result?", or "..., making it" tails. |
| Modal verbs minimized / active voice | PASS | Active voice throughout; modals limited to FAQ where "can" is the user's literal question. |
| Main clause before if/when/because | PASS | Conditional clauses follow the main clause. |
| Heading first-sentence mirror + bolded | PASS | Each H2 opens with a bolded sentence repeating the heading term (What is, two categories, automate, keep human, autonomous execution, choose, OTTO SEO). |
| Gerunds in headings | PASS | No -ing headings. |
| Heading hierarchy (H1→H2→H3, no skips) | PASS | One H1, H2 sections, H3 only inside FAQ. |
| List grammar (numeric for process, bullets for types; parallel) | PASS | Numbered: guardrails, choose-framework. Bulleted: task types, capabilities, keep-human. Parallel grammar held. |
| Naming — "Search Atlas" two words | PASS | Always "Search Atlas." |
| Naming — Search Atlas never called a "tool" | PASS | "tool" used only for the generic category/search term and for Slack/Teams/ClickUp ("the tools a team already uses"); never for Search Atlas or OTTO. |
| OTTO as a skill, not co-equal brand | PASS | "OTTO SEO, a skill of Search Atlas." Confined to one dedicated section + CTA + FAQ examples. |
| GBP not GMB; Domain Power not DA | PASS | "Google Business Profile" used; no GMB. No DA/domain-authority reference (metric not invoked here). |
| Primary query in opening paragraph | PASS | "SEO automation software" is the first phrase of the article. |
| Product accuracy vs. knowledge files | PASS | Pixel/any-CMS, learns from KG + GSC, on/technical/local/off-page capabilities, controls, 90% labor saved, months-in-minutes, first AI autopilot agent, pricing $99/$199/$399, 7-day free trial no card, Coworker on Slack/Teams/ClickUp — all trace to otto-seo.md, otto-seo-*.md facts, search-atlas-plan-details.md, atlas-coworker.md. No invented capability. |
| Autonomy framed WITH human controls | PASS | Every autonomy mention sits beside review-before-deploy, selective deploy, rollback, change logs, audit trails. "Autonomous does not mean unsupervised" stated explicitly. |
| Meta title < 60 chars | PASS | 54 chars. |
| Meta description 140–160 chars | PASS | 141 chars; contains primary keyword + two outcomes (what to automate / keep human, safety). |
| Internal links present, descriptive anchors, no para-initial link | PASS | 7 internal links (OTTO page, seo-automation-workflows, building-agentic-seo-workflow, automated-technical-seo-fixes, agentic-seo, ai-marketing-coworker, white-label-seo-platform). All descriptive anchors; none starts a paragraph. |
| Cannibalization vs. existing posts | PASS | Targets category/selection intent; cross-links the two workflow how-tos as follow-ups; no step-by-step workflow content duplicated. Documented in research.md. |
| Competitor imitation (self-ranking listicle) | PASS | No "best tools, us #1" list. Category explainer + decision framework instead. Competitors named only for SERP/category context. |
| External evidence dated + attributed; no invented stats | PASS | Aira 2025, Botify Q4 2024, MCP 2025–2026, market projection — all in sources.md with dates and reliability notes. [VERIFY] flags on the exact Aira %, the enterprise-78% figure (not used in body), and the market-size projection. Body uses hedged framing ("most," "a large share," "one projection"). |
| Schema | PASS | Article + FAQPage specified in metadata.md; 5 FAQ Q&A with question-form H3s for AEO. |
| Length 2,200–2,800 | PASS | 2,269 words. |

## [VERIFY] flags carried forward
- Exact Aira "86%" figure — body uses "most / a large majority," safe to publish; confirm number before adding a hard percentage.
- AI SEO market-size projection ($1.2B→$4.5B) — single-source; body frames as "one projection."
- Enterprise "78% use AI for keyword research" — referenced in research.md only, not in the article body.

## Verdict
**PASS** on all audited dimensions. Article is publication-ready.
