---
description: Decide promotion status for a v3 collection-page revision against STYLE-SYSTEM and the campaign audit-report. Optionally apply the promotion.
argument-hint: <v3-file-path> [--apply]
---

Decide whether a `drafts/v3/` revision is ready to replace its sibling in `drafts/`, and optionally apply the swap. Follow `CLAUDE.md`.

## Client context protocol (mandatory — execute before deciding)

1. **Identify the client** from the v3 file path. The path always matches `clients/{client}/campaigns/{NN}-*/drafts/v3/{file}.md`. Reject the request if it does not.
2. **Read `clients/{client}/STYLE-SYSTEM.md`** — canonical voice, terminology, banned phrases.
3. **Read `universal-rules/UNIVERSAL-RULES.md`** for base writing standards.
4. **Read the campaign's `audit-report.md`** at `clients/{client}/campaigns/{NN}-*/audit-report.md`. The v3 exists to resolve findings in that report — every Critical and Major finding must be addressed before promotion.

## Input

`$ARGUMENTS` is a path to a v3 file plus an optional `--apply` flag.

Valid path shape:
- `clients/{client}/campaigns/{NN}-*/drafts/v3/{file}.md`

If the path does not exist, stop and report the missing file.

## Process

1. **Resolve siblings.** Derive the corresponding `drafts/{file}.md` path by stripping the `v3/` segment. If the sibling does not exist, this is a net-new draft (not a promotion); stop and tell the user to use `/draft` or add the file to a campaign brief instead.
2. **Diff the files.** Read both files and identify every section the v3 changes, adds, or removes relative to the current draft.
3. **Run editor logic.** Apply the `editor` agent's checks against the v3:
   - Banned phrases from STYLE-SYSTEM.md and universal-rules
   - Terminology violations (required terms missing, banned terms present)
   - Voice / tone mismatch
   - Technical accuracy (freeze/thaw, sealing, slip-resistance, climate claims)
   - Page-structure rules from STYLE-SYSTEM.md §6.1
4. **Run audit compliance.** For each Critical and Major finding in `audit-report.md` that names this template (or "all 16"), state whether the v3 resolves it. Cite the audit-report section.
5. **Run final ship check.** Apply the `ship` command's QA dimensions: link QA, meta QA, schema QA, plagiarism risk, style-system compliance, publishability.
6. **Produce a verdict.** Choose exactly one:
   - **Approve and promote** — every Critical resolved, every Major resolved or explicitly justified, no banned-term violations, FAQ has real content (not placeholder).
   - **Approve pending FAQ** — every Critical resolved, every Major resolved, but FAQ section is still a placeholder. Promotion blocked until FAQ is filled.
   - **Hold** — at least one Critical or Major from audit-report is unresolved, or a STYLE-SYSTEM violation exists. List the remediation steps.
   - **Reject** — the v3 introduces regressions vs the current draft. List the regressions.

## Output format (when no `--apply` flag)

```
## Promotion decision: {Approve and promote | Approve pending FAQ | Hold | Reject}

### Client + scope
- Client: {client}
- Campaign: {NN-name}
- Template: {file}
- v3 path: {v3 path}
- Current draft: {drafts path}

### Audit-report compliance (Critical + Major only)
For each Critical or Major finding that applies to this template:
- [Finding ID, e.g. §4.2 inline sealing] — {Resolved | Unresolved | N/A}
  Evidence: {quoted line from v3 or short reason}

### STYLE-SYSTEM violations
- {None | List each: rule section + quoted line from v3}

### Editor findings (non-blocking)
- Section-level: {issues with concise fixes}
- Line edits: {Original → Suggested, max 5 most impactful}

### Ship QA
- Style-system compliance: Full | Minor violations | Major violations
- Plagiarism risk: Low | Medium | High (one-sentence reason)
- Publishability: Ready | After minor fixes | Not ready

### Remediation (only if Hold or Approve pending FAQ)
- {bullet list of concrete next steps}

### Next action
- {Approve and promote: "Run with --apply to swap files and regenerate HTML."}
- {Approve pending FAQ: "Fill FAQ section with 6 questions per audit-report §6.1, then re-run."}
- {Hold: "Resolve the items above and re-run."}
- {Reject: "Discard v3 or address the regressions before re-submitting."}
```

## Output format (when `--apply` flag is set)

`--apply` is honored only if the verdict is **Approve and promote**. For any other verdict, refuse and print the same output as the no-flag form with a note that --apply was ignored.

When honored:

1. Replace `drafts/{file}.md` with the contents of `drafts/v3/{file}.md`. Preserve the v3 file (do not delete) so the version is reviewable in git history.
2. Run `python scripts/build-html-before-after.py` from the repo root if the script exists and the campaign uses HTML previews; otherwise skip.
3. Output a confirmation:
   ```
   ## Promoted: {file}.md
   - Replaced: drafts/{file}.md (old version now lives in git history)
   - v3 preserved at: drafts/v3/{file}.md
   - HTML regenerated: {Yes (path) | Skipped (reason)}
   - Next step: open PR with `git checkout -b promote/{file} && git add . && git commit && git push`
   ```

## Constraints

- Do not invent audit findings that are not in the campaign's `audit-report.md`.
- Do not promote when FAQ is a placeholder ("Minimum N questions covering:..."). FAQ must contain actual questions per STYLE-SYSTEM.md §6.1.
- Do not rewrite content during promotion. Editor findings are advisory — the v3 ships as-is when approved.
- Do not use em dashes.
- Do not skip the audit-report compliance step. The whole point of `/promote-v3` is enforcing it.

## Failure modes

- **Path not under `drafts/v3/`**: refuse. This command only handles v3 promotions.
- **Sibling `drafts/{file}.md` missing**: refuse. Tell the user to use `/draft` for net-new pieces.
- **Campaign has no `audit-report.md`**: warn, then fall back to STYLE-SYSTEM-only evaluation. State the gap in the output.
- **STYLE-SYSTEM.md missing for client**: refuse. Onboard the client first via `scripts/generate-client-style-system.md`.
