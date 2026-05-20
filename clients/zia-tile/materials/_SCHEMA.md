# Material configs — schema

Machine-readable rule files, one per Zia material. The `material-guard` agent loads the file matching the piece's material and checks the draft against the hard rules in frontmatter. The prose body carries nuance and exact approved wording.

These files are derived from `../STYLE-SYSTEM.md` and the audited v3 drafts in `../campaigns/01-product-collection-pages/drafts/`. They do not replace STYLE-SYSTEM.md; they make its material-specific rules mechanically checkable. Where the two disagree, STYLE-SYSTEM.md wins and this file must be corrected.

## Frontmatter fields

| Field | Values | Meaning |
|---|---|---|
| `material` | kebab-case slug | Matches the filename. |
| `display_name` | string | How the material is named in copy (capitalization matters). |
| `glazed` | true / false / n/a | Drives sealing + variation language. |
| `origin` | string | Source region, for "How It's Made" grounding. |
| `freeze_thaw` | `suitable` / `not_suitable` / `verify` | Exterior freeze/thaw rule. `verify` means confirm with Alex before asserting. |
| `pools_spas` | `suitable` / `not_suitable` / `suitable_with_sealing` / `verify` | Full-submersion rule. |
| `variation_trio_applies` | true / false | Whether "chips, pits, and crazing" applies. Glazed-fired-clay only. |
| `variation_language` | list | Approved variation nouns for this material. |
| `sealing_profile` | slug | Which sealing instruction set applies. |
| `confidence` | `high` / `draft` / `verify` | `high` = STYLE-SYSTEM explicit; `draft` = from an audited v3 draft; `verify` = unconfirmed. |
| `source` | string | Exact STYLE-SYSTEM sections or draft paths the rules come from. |

## Hard-rule semantics for material-guard

- A draft is a **violation** if it asserts a usage the config marks `not_suitable` (e.g., a Cotto page that approves pools).
- A draft is a **warning** if it touches a `verify` field without flagging it for Alex.
- A draft is a **violation** if it uses variation language the config forbids (e.g., "crazing" on an unglazed Cotto page when `variation_trio_applies: false`).
- `material-guard` never rewrites. It reports violations with the STYLE-SYSTEM citation and the corrected rule.

## Confidence policy

- `high`: rule is stated explicitly in STYLE-SYSTEM.md §4.1, §11, or §12. Enforce hard.
- `draft`: rule is taken from an audited v3 draft because STYLE-SYSTEM.md is silent. Enforce, but the report notes the source and recommends confirming with Alex on first use per material.
- `verify`: no authoritative source. material-guard flags any draft that asserts this dimension and tells the writer to confirm with Alex. Never auto-pass.
