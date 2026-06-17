---
description: Research and generate a semantic & NLP terms reference doc for a Zia Tile article.
argument-hint: <client-slug> <article-slug> <primary-keyword> [<keyword2> <keyword3>]
model: sonnet
---

Generate a semantic and NLP terms reference document for a content piece. Run this before finishing any article. The primary output is a **do-not-remove list** — terms already in the draft that carry semantic weight and must survive editing. Secondary sections cover gaps and intentional omissions.

## Input

`$ARGUMENTS`: `<client-slug> <article-slug> <primary-keyword> [<keyword2> <keyword3>]`

- `client-slug` — e.g. `zia-tile`
- `article-slug` — matches the draft filename or URL slug, e.g. `herringbone-tile-pattern`
- `primary-keyword` — the main target keyword, e.g. `herringbone tile`
- `keyword2`, `keyword3` — optional secondary keywords

## What this command does

1. **Reads the draft** at `clients/{client}/campaigns/**/drafts/**/{article-slug}*.md`. If no draft is found, produce the doc without cross-reference and note it.
2. **Searches the SERP** for the primary keyword (plus secondary keywords if provided) using WebSearch. Block pinterest.com, instagram.com, youtube.com.
3. **Fetches the top 3–4 ranking pages** using WebFetch. Target comprehensive guides, not product pages or forums. Run fetches in parallel.
4. **Extracts NLP terms** from the fetched pages: technical terms, material names, installation terms, layout terms, room applications, tools, measurements, and recurring concepts.
5. **Cross-references** extracted terms against the draft — marking each as present, thin, or missing.
6. **Writes the output** to `clients/{client}/semantic-terms/{article-slug}.md`.

## Output format

```markdown
---
article: {article-slug}
url: {client-domain}/blogs/...
primary_keyword: {primary-keyword}
keywords: {all keywords}
grader_score: {score if available, else "not run"}
source: SERP research ({domains fetched})
---

# Semantic & NLP Terms — {Article Title}

*Internal reference. Do not remove the terms in Section 1 during editing.*

---

## Do not remove — these terms are present and carry semantic weight

These terms appear in the draft and match what ranking pages cover for this topic.
Editing and rewriting is fine. Removing these terms entirely reduces topical coverage.

{bulleted list, grouped by category: pattern/layout | installation | materials | room applications | maintenance}

---

## Missing or thin — consider adding before publishing

| Term | Gap | Where it could fit |
|---|---|---|
| {term} | Not mentioned / thin | {section name in the draft} |

---

## Not applicable for {client} — intentional omissions

These terms appear on SERP pages but should not be added.

| Term | Reason |
|---|---|
| {term} | {one-line reason, e.g. "Zia does not carry porcelain"} |

---

## Related search terms

Useful for heading variations and FAQ expansion only — do not force into body copy.

{bulleted list}
```

## Rules

- **Section 1 is the deliverable.** The do-not-remove list is what the editor needs before every editing session. Make it complete and grouped so it is scannable at a glance.
- **No invention.** Only include terms that actually appear on the fetched SERP pages. Do not add terms from general SEO knowledge or assumption.
- **Flag intentional omissions clearly.** For Zia, terms like "porcelain," "vinyl," "wood tile" belong in Section 3 — they appear on ranking pages but Zia does not carry these materials.
- **Keep gap notes tight.** One line per gap. Name the specific section of the draft where the term could be added.
- **Do not rewrite the draft.** This command produces a reference doc only. All editing decisions belong to the editor.
- If the draft does not exist yet, omit Sections 1 and 2 and note: *"Draft not yet available — cross-reference pending."*

## Output location

`clients/{client}/semantic-terms/{article-slug}.md`

Create `clients/{client}/semantic-terms/` if it does not exist.

## When to run

- **In the pipeline:** `/run-piece` calls this as stage 16 (after `/render-html`). Output is referenced in `RUN-SUMMARY.md`.
- **Standalone:** Run for any article drafted outside the pipeline, or before any editorial revision session.

```
/semantic-terms zia-tile herringbone-tile-pattern "herringbone tile" "herringbone pattern" "herringbone floor tile"
```
