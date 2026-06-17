---
description: Research semantic and NLP terms before drafting, then produce a protected-terms doc for the editor after.
argument-hint: <client-slug> <article-slug> <primary-keyword> [<keyword2> <keyword3>] [--pre-draft | --post-draft]
model: sonnet
---

Runs in two phases depending on where it sits in the pipeline.

- `--pre-draft` (stage 0): SERP research before writing begins. Extracts NLP and semantic terms from top-ranking pages and saves them as drafting guidance so the writer knows which terms to incorporate.
- `--post-draft` (stage 16, default): Cross-references the finished article against the pre-draft terms list, then produces a clean protected-terms doc for the editor. The editor doc lists only what is in the article — no gap analysis, no editorial notes.

---

## Input

`$ARGUMENTS`: `<client-slug> <article-slug> <primary-keyword> [<keyword2> <keyword3>] [--pre-draft | --post-draft]`

- `client-slug` — e.g. `zia-tile`
- `article-slug` — matches the draft filename or URL slug, e.g. `herringbone-tile-pattern`
- `primary-keyword` — the main target keyword, e.g. `herringbone tile`
- `keyword2`, `keyword3` — optional secondary keywords
- `--pre-draft` — run phase 1 only
- `--post-draft` — run phase 2 only (default when called from stage 16)

---

## Phase 1 — Pre-draft research (`--pre-draft`)

Run this before the brief is written.

1. **Search the SERP** for the primary keyword (plus secondary keywords) using WebSearch. Block pinterest.com, instagram.com, youtube.com.
2. **Fetch the top 3–4 ranking pages** using WebFetch in parallel. Target comprehensive guides, not product pages or forums.
3. **Extract NLP and semantic terms** from each page: technical terms, material names, installation terms, layout terms, room applications, tools, measurements, and recurring concepts. Only include terms that appear on the fetched pages — no invention.
4. **Identify intentional omissions** — terms that appear on SERP pages but are not applicable to this client's product range. For Zia, this includes porcelain, vinyl, travertine, wood, and wood look tile.
5. **Write `nlp-guidance.md`** to the run directory as drafting input for the writer.

### nlp-guidance.md format

```markdown
# NLP & Semantic Terms — Drafting Guidance
# {Article Title}

These terms appear across top-ranking pages for "{primary keyword}".
Incorporate them naturally into the draft. Do not force them — use where they fit.

## Terms to incorporate

**{category}**
- {term}
- {term}

## Do not include — not applicable for {client}

- {term} — {one-line reason}
```

---

## Phase 2 — Post-draft protected-terms doc (`--post-draft`)

Run this after the article passes all pipeline gates and before delivery to the editor.

1. **Read the finished draft** at `clients/{client}/campaigns/**/drafts/**/{article-slug}*.md`.
2. **Read `nlp-guidance.md`** from the run directory.
3. **Cross-reference**: identify which terms from the guidance doc are present in the finished article.
4. **Write two files:**
   - `clients/{client}/semantic-terms/{article-slug}.md` — the editor-facing protected-terms doc (format below)
   - Append the path to `RUN-SUMMARY.md`

### Editor-facing protected-terms doc format

```markdown
# Protected Terms — {Article Title}

These terms are in the article. Do not remove or replace them during editing.
They are present because they match what search engines and ranking pages expect for this topic.

**{category}**
- {term}
- {term}

**{category}**
- {term}
```

Rules for this doc:
- **No gap analysis.** No missing terms, no editorial notes, no recommendations.
- **No intentional omissions section.** That is internal only and lives in `nlp-guidance.md`.
- **Grouped by category** so it is scannable: pattern/layout — installation — materials — room applications — grout and finish — design concepts.
- **Clean enough to hand directly to the editor.** No internal process language.

---

## Output locations

| File | Purpose |
|---|---|
| `runs/{slug}/nlp-guidance.md` | Drafting input — writer reads this before and during writing |
| `clients/{client}/semantic-terms/{article-slug}.md` | Editor doc — Brittany's do-not-change list |

Create `clients/{client}/semantic-terms/` if it does not exist.

---

## Integration with the pipeline

`/run-piece` calls this command at two points:

- **Stage 0** (before brief): `--pre-draft` — produces `nlp-guidance.md`
- **Stage 16** (after render-html): `--post-draft` — produces the editor protected-terms doc

Standalone usage:

```
# Before drafting
/semantic-terms zia-tile herringbone-tile-pattern "herringbone tile" "herringbone pattern" "herringbone floor tile" --pre-draft

# After drafting
/semantic-terms zia-tile herringbone-tile-pattern "herringbone tile" "herringbone pattern" "herringbone floor tile" --post-draft
```
