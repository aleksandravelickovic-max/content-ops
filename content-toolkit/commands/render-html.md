---
description: Render a final MD draft into clean semantic HTML for Google Doc / CMS delivery.
argument-hint: <path-to-draft.md> [--title <title>]
model: haiku
---

Convert a pipeline-produced Markdown draft into the final HTML delivery artifact. HTML is the canonical delivery format from 2026-05-27 onward — uploading MD to Google Drive for auto-conversion is deprecated because the heading mapping is inconsistent and the convert step burns tokens on every re-upload.

This command is mechanical (no LLM judgment) and runs on **haiku** because it's a deterministic shell-out to `scripts/render-html.py`. It does not modify the source MD.

## Input

`$ARGUMENTS`: `<path-to-draft.md> [--title <title>]`

- `path-to-draft.md` — required. The final draft produced by `/run-piece` (typically `clients/{client}/campaigns/{campaign}/drafts/{slug}.md`).
- `--title` — optional. Override the `<title>` and the leading `<h1>`. Defaults to the document's first `# Heading`, or the file stem if no H1 is present.

## What it does

1. Reads the MD file.
2. Strips the leading YAML frontmatter block (operational metadata — `url`, `meta_title`, `source`, etc. — never publishable copy).
3. Runs `python scripts/render-html.py <path>` to produce `<same-path>.html`.
4. Reports the output path.

## What the renderer guarantees

- Semantic structure preserved: `# → <h1>`, `## → <h2>`, `### → <h3>` with stable anchor IDs.
- Lists, tables, fenced code, emphasis, and image tags pass through with `markdown.extensions.extra`.
- Smart quotes (smartypants) so the Google Doc import looks editorial, not raw.
- A `<meta name="source-md">` tag in `<head>` records the MD path for chain of custody.
- A `<meta name="rendered-at">` timestamp for the run.

## What it does NOT do

- Inline CSS. The HTML is structural only; the Google Doc import applies its own styles.
- Re-flow paragraphs, "clean up" the MD, or any LLM edits.
- Upload to Drive. That's `/export-gdrive` (PR-C).

## Example

```
/render-html clients/zia-tile/campaigns/01-product-collection-pages/runs/collection-cotto-allende/draft.md
```

Produces `clients/zia-tile/campaigns/01-product-collection-pages/runs/collection-cotto-allende/draft.html`.

## Integration with `/run-piece`

`/run-piece` calls this as stage 12 after all gates pass and the final draft is written. You rarely need to invoke it directly — only when re-rendering a piece whose MD was edited manually after the pipeline already produced an `.html`.

## Constraints

- Do not edit the MD. If the MD needs changes, fix the source then re-run.
- Do not strip non-frontmatter HR rules (`---` in the body). The frontmatter stripper only acts on a `---` block that opens the file.
- If `scripts/render-html.py` is missing or `markdown` (the Python lib) is not installed, report the dependency gap and stop. Do not invent an HTML output.
