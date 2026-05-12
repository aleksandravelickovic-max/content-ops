---
description: Run the final QA pass before publishing: links, metadata, schema, and plagiarism-risk checks.
argument-hint: <draft text, page, or file path>
---

Run a final pre-publish QA pass on the content below, following `CLAUDE.md`.

## Input
$ARGUMENTS

## Goals
- Catch issues that block publishing.
- Check the content as final output, not as a draft in progress.
- Flag only real problems, not stylistic preferences.
- Keep the review practical and decision-oriented.

## Checks

### 1. Link QA
Check all links that appear in the content.

Review for:
- broken or malformed links
- placeholder links
- irrelevant links
- repeated links with no purpose
- anchor text that does not match the destination context
- internal links that are not contextually justified
- paragraphs that open with links

If no links are present, say so.

### 2. Meta QA
Check whether the page has the required metadata or enough information to create it.

Review for:
- title tag quality
- meta description quality
- H1 alignment with topic
- mismatch between title, H1, and page intent
- title or description wording that is vague, bloated, duplicated, or clickbait

If title tag or meta description is missing, generate a clean recommendation.

### 3. Schema QA
Check whether the content supports schema and whether the schema type fits the page.

Review for:
- best-fit schema type based on page intent and structure
- whether the visible content supports that schema
- missing required fields implied by the schema type
- mismatch between page type and likely schema type
- over-markup risk or unsupported schema claims

If schema is appropriate, recommend only the schema types clearly supported by the content.

### 4. Plagiarism-risk check
Check for signs that the content is too close to common SERP phrasing or likely source phrasing.

Review for:
- overly standard definitions
- repeated industry clichés
- tool descriptions that sound templated
- sentence structures that feel copied or overfamiliar
- list items that read like lightly rewritten competitor content

Do not make a legal claim. Flag only editorial plagiarism risk or originality risk.

### 5. Final publishability check
Check whether the page is ready to publish as-is.

Review for:
- unresolved flags or placeholders
- sections that feel incomplete
- obvious repetition
- formatting issues
- inconsistent heading hierarchy
- weak or generic sections that still need rewriting

## Output format

### Ship decision
Choose one:
- **Ready to ship**
- **Ship after minor fixes**
- **Not ready to ship**

### Critical fixes
List only issues that must be fixed before publishing.
If none, say `None`.

### Minor fixes
List worthwhile improvements that are not blockers.
If none, say `None`.

### Recommended metadata
Include only if missing or weak:
- **Title tag:**
- **Meta description:**

### Recommended schema
Include:
- **Schema type:**
- **Why it fits:**
- **Missing fields or risks:** only if relevant

### Plagiarism-risk notes
- State whether editorial plagiarism risk is low, medium, or high.
- Give a short reason.

### Final notes
- Keep this short.
- Include only actionable publish-stage notes.

## Constraints
- Do not rewrite the full article.
- Do not give generic SEO advice.
- Do not use em dashes.
- Do not use internal process language such as "based on SERP review" or "reviewed sources."
- Focus on ship-stage issues only.
