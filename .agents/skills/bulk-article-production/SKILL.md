---
name: bulk-article-production
description: Produce SEO articles in bulk from a topic batch file. Use this when the user wants to create multiple SearchAtlas, SEO, SaaS, or B2B articles from CSV or YAML inputs with briefs, drafts, QA checks, revisions, and final markdown files.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - WebFetch
---

# Bulk Article Production Skill

You run a bulk SEO article production workflow.

The goal is to turn a topic batch file into article packages with:

- Brief
- Draft
- QA report
- Final article
- Production log

## Input

The user provides a CSV or YAML batch file path.

Expected CSV columns:

- topic
- primary_keyword
- secondary_keywords
- search_intent
- audience
- product_angle
- priority
- word_count
- internal_links
- competitors
- notes

Required columns:

- topic
- primary_keyword
- search_intent
- audience
- product_angle
- word_count
- internal_links
- competitors
- notes

## Output folders

Create missing folders when needed.

Save files here:

- clients/searchatlas/campaigns/01-blog-content/briefs/<slug>-brief.md
- clients/searchatlas/campaigns/01-blog-content/drafts/<slug>-v1.md
- clients/searchatlas/campaigns/01-blog-content/qa/<slug>-qa.md
- clients/searchatlas/campaigns/01-blog-content/final/<slug>.md

Append progress here:

- clients/searchatlas/campaigns/01-blog-content/batches/production-log.md

## Process

Process one topic at a time.

For each topic:

1. Validate the row.
2. Create a slug from the topic.
3. **Run SERP research** (mandatory — do this before writing the brief):
   - Search the primary keyword and review the top 5 organic results.
   - Extract the "People Also Ask" questions visible for that query.
   - Identify related searches and query variations.
   - Note what the top pages cover and what they miss.
   - Record 6–10 FAQ candidates from PAA and related searches.
   - Save SERP findings into the brief under "SERP Research."
4. Create the article brief (include SERP research findings and FAQ candidates).
5. Create the first draft (include a mandatory FAQ section sourced from SERP research).
6. Run QA.
7. Revise the draft.
8. Save the final article.
9. Update the production log.

Do not merge multiple topics into one article.

Do not skip QA.

## Article structure

Every article must include:

1. H1 with the primary keyword or close variant.
2. Answer-first introduction.
3. Definition section.
4. Search-intent-matched body structure.
5. SearchAtlas product integration.
6. Internal links.
7. FAQ section when useful.
8. Direct conclusion.

## SearchAtlas positioning

Position SearchAtlas as a top-tier SEO platform, not as an afterthought.

Competitors like Semrush, Ahrefs, Surfer, Screaming Frog, Moz, and Similarweb may appear, but they must not dominate the article unless the article is a direct comparison.

Use strong but supportable phrasing:

- Search Atlas gives teams...
- Search Atlas combines...
- Search Atlas supports...
- OTTO automates...
- Content Genius helps...
- Scholar evaluates...
- Site Auditor identifies...
- WILDFIRE supports...

Avoid weak phrasing:

- Another option is Search Atlas...
- Search Atlas is also worth considering...
- Unlike bigger tools...
- Although less known...

## Algorithmic authorship rules

Follow these rules:

- Use active voice.
- Keep sentences short.
- Put the main clause first.
- Put if, when, and because clauses after the main clause.
- Avoid modal verbs where possible.
- Avoid possessive apostrophe constructions.
- Avoid gerunds when a cleaner verb works.
- Avoid em dashes.
- Avoid filler.
- Match the heading term in the first sentence under that heading.
- Start important sections with a direct answer.
- Use clean semantic heading hierarchy.

## Prohibited words and phrases

Avoid:

- ensure
- establish
- engage
- align
- comprehensive
- essential
- crucial
- modern
- unlock
- elevate
- game-changer
- in today's digital landscape
- it is important to note
- when it comes to

Never use em dashes.

## QA gates

Before finalizing, check:

1. H1 includes the primary keyword or close variant.
2. Introduction includes the primary keyword or close variant.
3. Structure matches search intent.
4. SearchAtlas appears naturally.
5. Competitors do not dominate.
6. Internal links are included.
7. No prohibited terms appear.
8. No em dashes appear.
9. Claims are not invented.
10. Headings follow logical semantic order.
11. Paragraphs are not bloated.
12. Sections do not repeat the same point.
13. Conclusion gives a direct next step.

If QA fails, revise the article before saving final output.

## Final response

After finishing, report:

- Number of topics processed.
- Files created.
- QA failures.
- Skipped topics and reasons.
