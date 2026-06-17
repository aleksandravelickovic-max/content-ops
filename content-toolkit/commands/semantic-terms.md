---
description: Research and generate a semantic & NLP terms reference doc for a Zia Tile article.
argument-hint: <client-slug> <article-slug> <primary-keyword> [<keyword2> <keyword3>]
model: sonnet
---

Generate a semantic and NLP terms reference document for a content piece. The output is an internal editing reference — not publishable copy. It tells the editor which terms ranking pages use so they can maintain topical coverage without guessing.

## Input

`$ARGUMENTS`: `<client-slug> <article-slug> <primary-keyword> [<keyword2> <keyword3>]`

- `client-slug` — e.g. `zia-tile`
- `article-slug` — matches the draft filename or URL slug, e.g. `herringbone-tile-pattern`
- `primary-keyword` — the main target keyword, e.g. `herringbone tile`
- `keyword2`, `keyword3` — optional secondary keywords

## What this command does

1. **Searches the SERP** for the primary keyword (plus secondary keywords if provided) using WebSearch. Filter out pinterest.com, instagram.com, youtube.com.
2. **Fetches the top 3–4 ranking pages** using WebFetch. Target comprehensive guides, not product pages or forums. Run fetches in parallel.
3. **Extracts NLP terms** from each page: technical terms, material names, installation terms, layout terms, room applications, tools, measurements, and recurring concepts.
4. **Cross-references** the extracted terms against the existing draft at `clients/{client}/campaigns/**/drafts/**/{article-slug}*.md` if it exists. If no draft is found, skip the cross-reference and note it.
5. **Writes the output** to `clients/{client}/semantic-terms/{article-slug}.md`.

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

*Internal reference only. Use during editing to maintain topical coverage without reducing visibility.*

---

## Present — well covered

{bulleted list of terms already present in the draft}

---

## Missing or thin — check before publishing

| Term | Gap | Editorial note |
|---|---|---|
| {term} | Not mentioned / thin | {one-line note on where it could fit} |

---

## Not applicable for {client} — intentional omissions

{list of terms that appear on SERP but are irrelevant to this client's product range, with a one-line reason}

---

## Related search terms

{list from CG information retrieval or SERP PAA boxes — useful for heading variations and FAQ expansion}
```

## Rules

- **No invention.** Only include terms that actually appear on the fetched SERP pages. Do not add terms from general SEO knowledge.
- **Flag intentional omissions clearly.** For Zia, terms like "porcelain," "vinyl," "wood tile" belong in the intentional omissions section — they appear on ranking pages but Zia does not carry these materials.
- **Keep editorial notes tight.** One line per gap. Name the specific section of the draft where the term could be added if the draft exists.
- **Do not rewrite the draft.** This command produces a reference doc only. All editing decisions belong to the editor.
- If the draft does not exist yet, produce the terms doc without the cross-reference columns and note: *"Draft not yet available — cross-reference pending."*

## Output location

`clients/{client}/semantic-terms/{article-slug}.md`

If `clients/{client}/semantic-terms/` does not exist, create it.

## Integration with the pipeline

`/run-piece` calls this as stage 16 (after `/render-html`). The output file is referenced in `RUN-SUMMARY.md`. You can also run it standalone for any article that was drafted outside the pipeline:

```
/semantic-terms zia-tile herringbone-tile-pattern "herringbone tile" "herringbone pattern" "herringbone floor tile"
```
