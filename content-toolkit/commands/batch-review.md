---
description: Run the QA gates across many drafts and produce one aggregated report. Surfaces backlog-wide patterns (FAQ placeholders, banned terms, material errors) without opening each file by hand.
argument-hint: <glob-or-dir> [--gates material,terminology,contact,person,voice,koray]
---

Run the review gates over a set of drafts and aggregate the findings. This gives visibility across a backlog (e.g., the 130 March/April pieces) without manual file-by-file review. Follow `CLAUDE.md`.

## Input

`$ARGUMENTS`: a directory or glob of draft files, plus an optional `--gates` list. Default gates: material-guard, terminology-lint, contact-line-check, person-consistency. Add `voice` and `koray` only when explicitly requested (they are slower and scored).

## Client context protocol (mandatory)

1. **Identify the client** from the draft paths (all must be under one `clients/{client}/`).
2. Load `STYLE-SYSTEM.md`, the relevant `materials/*.md` (inferred per file), `contact-block.md`, and `COMPLIANCE.yml` once, then reuse across all drafts.

## Process

1. Enumerate the target drafts. Skip locked/auto-generated files (registry.json, html/).
2. For each draft, infer the material from the filename and run the selected gates (the same logic the individual agents use).
3. Aggregate results into per-gate tallies and a per-file matrix.

## Output format

```
## Batch review: {N} drafts — {client}

### Per-file matrix
| File | material-guard | terminology | contact | person | voice | koray |
|---|---|---|---|---|---|---|
| {file} | PASS | 2 banned | PASS | 1 switch | 84 | 81 |
| ...

### Aggregate patterns
- Material errors (critical): {count} across {files}
- Banned-term hits: {count} total; most common: "{term}" ({n} files)
- Missing contact line: {count} files
- Person switches / second-person: {count} files
- FAQ placeholders remaining: {count} files
- Drafts below voice/koray gate (<80): {list, if those gates ran}

### Priority queue (worst first)
1. {file} — {the single most critical issue}
2. ...

### Clean (ready to promote/ship)
- {files that passed all selected gates}
```

## Constraints

- Read-only. batch-review never modifies drafts.
- Be exhaustive on critical material errors; those are factual and block.
- Default to the four mechanical gates; only run voice/koray when asked (cost).
- Do not use em dashes.
