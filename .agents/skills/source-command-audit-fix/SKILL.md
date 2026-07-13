---
name: "source-command-audit-fix"
description: "Apply the campaign audit-report.md findings to a single template, fixing each Critical and Major finding in place. Reports each fix mapped to its finding ID."
---

# source-command-audit-fix

Use this skill when the user asks to run the migrated source command `audit-fix`.

## Command Template

Apply audit-report findings to a template (Stream C work). Follow `AGENTS.md`. Without `--apply` you produce the corrected draft plus a findings map; with `--apply` you write the corrected file in place.

## Client context protocol (mandatory)

1. **Identify the client and template** from the path.
2. **Read, in this order:**
   - `clients/{client}/STYLE-SYSTEM.md`
   - `clients/{client}/campaigns/{NN}-*/audit-report.md` — the spec. Find every finding that names this template (or "all 16 unless noted").
   - `clients/{client}/materials/{material}.md` — the material rules for this template (infer the material from the filename).
   - `clients/{client}/contact-block.md`
   - The template itself.

## Process

1. **Enumerate findings.** List every Critical, Major, and Minor finding from audit-report.md that applies to this template, by ID/section. Use both the top-line "apply to all" findings and the per-doc section for this template.
2. **Apply each fix.** For each finding, make the minimal correction that resolves it:
   - Structural (9-section reorg, heading hierarchy) — restructure without losing content.
   - Verbatim wording (§8.2 shipping, §4.2 sealing) — replace with the exact approved text.
   - Additions (25% overage option, inline slip-resistance ⅛", affirmative freeze/thaw prose) — insert in the correct section.
   - Terminology (grout joints, drop "wholly unique," strip "Reference for usage") — replace per STYLE-SYSTEM.
   - FAQ placeholder — if the finding requires real questions, generate the minimum 6 per §6.1; otherwise leave a clearly marked placeholder and flag it.
3. **Cross-check with material-guard.** After fixing, confirm no freeze/thaw, pool, or sealing claim contradicts the material config. A fix that introduces a material error is itself a failure.
4. **Map fixes to findings.** Every change must trace to a finding ID. Do not make changes the audit-report did not call for (no scope creep).

## Output format (no `--apply`)

```
## Audit-fix: {template} — {N findings addressed}

### Findings map
- {finding ID / section}: {what was wrong} -> {what changed}
- ... (Critical first, then Major, then Minor)

### Could not fix (needs input)
- {finding}: {why — e.g., FAQ needs SKU-specific content, or an open question for Alex}

### material-guard recheck
{PASS | issues}

---
## Corrected draft
{full corrected template in clean markdown}
```

## Output format (`--apply`)

Write the corrected content to the template path, then output the findings map + a confirmation:
```
## Applied: {template}
- {N} findings resolved (Critical {n}, Major {n}, Minor {n})
- {M} findings need input (listed)
- material-guard: {PASS | issues}
- Next: regenerate HTML via scripts/build-html-before-after.py if the campaign uses previews; open PR.
```

## Constraints

- Do not invent audit findings. Only fix what audit-report.md lists for this template.
- Do not introduce material-rule errors while fixing structure.
- Preserve all locked content ([KEEP], [Locked], [CART MODULE]) unless a finding explicitly targets it.
- Do not use em dashes.
- Do not scope-creep into rewrites the audit did not request.
