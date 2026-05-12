---
description: Manage the knowledge/ directory. Subcommands: init, add, query, audit.
argument-hint: <init | add "<content>" | query "<topic>" | audit>
---

Manage the `knowledge/` directory as the source of truth for product facts, proof points, competitor notes, and testimonials. Follow `CLAUDE.md` rules.

## Input
$ARGUMENTS

The first token in `$ARGUMENTS` is the subcommand. Everything after the subcommand is the argument for that subcommand.

If no subcommand is provided, print the list of supported subcommands and stop.

## Global rules

- `knowledge/` is source-of-truth material, not marketing copy.
- No fluff, no SEO writing, no tone optimization.
- No em dashes. Use commas, colons, parentheses, or separate sentences.
- Keep files structured and minimal.
- Prefer atomic facts over long narrative text.
- When in doubt, separate product description, facts, and proof into different files.
- Do not invent information. If something is unclear, ask instead of guessing.

## Subcommand: `/knowledge init`

Create the scaffold of the knowledge directory. Do not add sample facts unless the user explicitly asks for them.

### Steps
1. Create the following directories at the repo root:
   - `knowledge/products/`
   - `knowledge/facts/`
   - `knowledge/proof/`
   - `knowledge/competitors/`
   - `knowledge/testimonials/`
2. Create `knowledge/README.md` with:
   - A one-paragraph explanation of what `knowledge/` is for (source of truth, not marketing).
   - A short description of what goes in each subdirectory.
   - The naming convention for files (kebab-case, one topic per file).
   - The expected frontmatter fields (`name`, `type`, `source`, `last_verified`).
3. If any of these directories or the README already exist, skip that item and report what was skipped.
4. Do not create sample files inside the subdirectories.

### Output
A short summary listing directories created, directories skipped (already existed), and the path to the README.

## Subcommand: `/knowledge add "<content>"`

Convert raw product or factual input into structured knowledge files.

### Input handling
- If `<content>` is a URL, fetch it first.
- If `<content>` is pasted text (product page, landing page, FAQ, spec doc), work from the text.
- If `<content>` is a short sentence stating a single fact, treat it as a single atomic fact and skip extraction.

### Extraction (for long inputs)
Extract the following into separate files. Do not invent information. Only extract what is present in the input.

For product or landing page input, extract:
- **Product definition** (one to three sentences, entity-first)
- **How it works** (mechanism)
- **Core capabilities** (bulleted, one capability per bullet)
- **Key differentiators** (bulleted, grounded in the input)
- **Limitations** (bulleted, only if stated or clearly implied)
- **Integrations** (named products or systems only)
- **Pricing** (only if present in the input)
- **FAQ** (only if present in the input)

Also extract:
- **Atomic facts** into `knowledge/facts/` (one fact per file)
- **Proof points** into `knowledge/proof/` (studies, metrics, data claims with numbers)
- **Competitor notes** into `knowledge/competitors/` (one competitor per file) when present
- **Testimonials** into `knowledge/testimonials/` (one quote per file) when present

### File format
Every file uses this frontmatter:

```
---
name: <short title>
type: <product | fact | proof | competitor | testimonial>
source: <URL or "pasted by user on YYYY-MM-DD">
last_verified: <YYYY-MM-DD>
---

<body content, atomic and structured>
```

### Confirmation before writing
Before creating any file, list every file the subcommand will create in this format:

```
Files to write:
- knowledge/products/<product-slug>.md
- knowledge/facts/<fact-slug>.md
- knowledge/proof/<proof-slug>.md
- ...
```

Then ask: "Write these files?" Wait for the user to reply with yes, no, or edits. Do not write anything until approval is given.

### Naming
- kebab-case.
- One topic per file.
- File name reflects the atomic content, not the input document title.

## Subcommand: `/knowledge query "<topic>"`

Search `knowledge/` for files relevant to the topic and return their contents inline.

### Steps
1. Scan `knowledge/` recursively.
2. Match files whose frontmatter `name`, filename, or body contains any word from `<topic>`.
3. Order results by priority:
   1. `knowledge/facts/`
   2. `knowledge/products/`
   3. `knowledge/proof/`
   4. `knowledge/competitors/`
   5. `knowledge/testimonials/`
4. Print each relevant file's path followed by its full contents.

### Rules
- Do not modify any file.
- Do not summarize the content; return it as written.
- If no matches are found, say so and stop.

## Subcommand: `/knowledge audit`

Scan the `knowledge/` directory and report issues. Do not modify files.

### Checks
- **Stale facts** (files where `last_verified` is older than 180 days).
- **Duplicate facts** (two or more files with the same or nearly identical claim).
- **Contradictory facts** (two files stating claims that conflict).
- **Missing product sections** (product files missing any of: definition, how it works, capabilities, differentiators, limitations).
- **Product claims without proof** (claims stated as numeric outcomes that have no matching file in `knowledge/proof/`).
- **Frontmatter gaps** (missing `name`, `type`, `source`, or `last_verified`).

### Output
Group findings under these headings. Omit any heading that has no issues.

```
## Stale facts
- <file path>: last_verified = <date>

## Duplicate facts
- <file path> and <file path>: <short description of overlap>

## Contradictory facts
- <file path A> says <claim A>; <file path B> says <claim B>

## Missing product sections
- <file path>: missing <section names>

## Claims without proof
- <file path>: <claim> has no proof file

## Frontmatter gaps
- <file path>: missing <fields>

## Recommended fixes
- <file path>: <specific action>
```

Output only issues and recommended fixes. Do not output files that pass.

## Output format
- Clean markdown.
- No commentary outside the subcommand output.
- No explanation of reasoning.
