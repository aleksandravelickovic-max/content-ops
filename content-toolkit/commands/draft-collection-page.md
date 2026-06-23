---
description: Draft a Zia material/category collection page from the approved template, grounded in the material config. Self-checks against material-guard and terminology rules before returning.
argument-hint: <client-slug> <material> [campaign-path]
---

Draft a collection page following `CLAUDE.md` and the client's collection template. The output is a finished collection page draft, not an analysis.

## Client context protocol (mandatory — execute before drafting)

1. **Identify the client and material** from `$ARGUMENTS`. The material must match a file in `clients/{client}/materials/`.
2. **Read, in this order:**
   - `clients/{client}/STYLE-SYSTEM.md` — canonical voice, terminology, technical accuracy.
   - `universal-rules/UNIVERSAL-RULES.md` — base standards.
   - `clients/{client}/materials/{material}.md` — the hard rules for freeze/thaw, pools/spas, sealing, variation language. These are non-negotiable.
   - `clients/{client}/page-templates/collection.md` — the section spine and collection-specific rules.
   - `clients/{client}/contact-block.md` — the contact line to inject.
   - The golden reference if it exists: `clients/{client}/campaigns/02-march-april-updates/drafts/collection-cotto.md`.
3. **Read source material** in `clients/{client}/raw/` (knowledge, research) for this material. Do not invent product facts. If a fact is missing, flag it, do not fill it.

## Input

`$ARGUMENTS`: `<client-slug> <material> [campaign-path]`. If `campaign-path` is given, write the output there; otherwise return inline and tell the user where it should be saved.

## Drafting rules

- Follow the collection template section order exactly.
- Apply the material config's freeze/thaw, pools/spas, sealing, and variation language verbatim. A material rule overrides any generic instinct.
- Use the contact block in the closing and the relevant FAQ answers.
- Voice bar: the client editorial benchmark (Zia: Architectural Digest / Wallpaper*). Authority through specificity, never adjectives.
- No invention: every product fact must come from STYLE-SYSTEM.md, the material config, or `raw/`. Flag gaps under `Flags:` at the top.
- No em dashes. No second person. Hold one grammatical person throughout.

## Self-check before returning (mandatory)

Before returning the draft, run these checks inline and fix anything they catch:
1. **material-guard logic**: every freeze/thaw, pool/spa, sealing, and variation claim matches `materials/{material}.md`. Any `verify`-confidence dimension is flagged for Alex, not asserted.
2. **terminology-lint logic**: no banned terms (§3.2); required terms correct (§3.1).
3. **contact-line logic**: email + phone present in closing + overage/installation FAQ.
4. **person-consistency logic**: one person held, no second person.
5. **Repetition guard** (§7.2): no phrase or adjective repeated across the page; "traditional" not twice in one passage.

## Output format

```
Flags:
- {missing inputs or unverifiable facts, or "None"}

{the full collection page draft in clean markdown, template section order}

---
## Self-check
- material-guard: {PASS | issues fixed}
- terminology-lint: {PASS | issues fixed}
- contact-line: {PASS}
- person-consistency: {PASS}
- repetition: {PASS}
- Verify-with-Alex: {list any draft/verify-confidence rules used, or "None"}
```

## Sidecar: Semantic terms (mandatory — runs after self-check)

After the self-check passes, generate a `{draft-slug}-semantic-terms.md` file alongside the draft. Write it to the same directory as the draft, replacing `.md` with `-semantic-terms.md` (e.g., `drafts/collection-zellige-semantic-terms.md`).

**Step 1 — Identify expected NLP terms** for this material using your knowledge of the tile/design semantic field and the SERP vocabulary for the primary keyword. Draw from:
- Material origin and provenance entities
- Process and craft vocabulary (firing, glazing, cleft, calibrated, etc.)
- Application contexts (floors, walls, exterior, wet areas, etc.)
- Installation and trade terms
- Finish, texture, and variation language
- Design style references and interior design vocabulary
- Long-tail buyer queries

**Step 2 — Scan the finished draft** to determine which expected terms are present (exact match or clear variant counts as present).

**Step 3 — Write the sidecar file** in this format:

```markdown
# Semantic / NLP Terms — {Material} Collection Page
Zia Tile | {date}

Terms marked ✓ are present in the draft.
Terms marked ○ are not yet covered — incorporate naturally where they fit.

## Material & Origin Entities
- ✓ / ○ {term}

## Technical & Process Terms
- ✓ / ○ {term}

## Application Contexts
- ✓ / ○ {term}

## Installation & Trade Terms
- ✓ / ○ {term}

## Design & Style References
- ✓ / ○ {term}

## Search Intent Phrases
- ✓ / ○ {phrase}
```

Sidecar rules:
- Include 25–40 terms total across all categories.
- Mark ✓ only if the term (or a clear variant) appears in the draft body.
- No editorial commentary — terms and status only.
- Do not include terms that are intentionally excluded by the material config (e.g., "porcelain," "vinyl," "wood look" on a natural stone page).
- If `campaign-path` is given, write the sidecar there. If no path was given and the draft was returned inline, note the sidecar path and output it inline as a second block after the draft.

## Constraints

- Produce a finished page, not a brief or outline.
- Do not output internal process language ("based on SERP," "reviewed sources").
- If the material config or STYLE-SYSTEM is missing, stop and say so.
