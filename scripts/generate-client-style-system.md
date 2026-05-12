# Generate Client Style System

Slash command and script for processing raw client materials into a canonical STYLE-SYSTEM.md.

## Usage

```
/generate-style-system <client-name>
```

Or run directly:
```
claude -p "$(cat scripts/generate-client-style-system.md)" --arg client=zia-tile
```

## Process

Given a client directory at `clients/{client}/`, this script:

1. **Reads all raw materials** in `clients/{client}/raw/` — transcripts, research, website data, editorial research, style guides, meeting notes, channel recaps
2. **Reads the universal style system** at `universal-rules/UNIVERSAL-RULES.md` as the base writing rules
3. **Extracts and synthesizes** the following into a single canonical output:

### What gets extracted from raw materials

| Section | Source priority |
|---|---|
| Brand & audience | Website research → transcripts → channel recaps |
| Voice & tone | Editorial voice research → style guides → transcript feedback |
| Terminology (required + banned) | Style guides → client feedback in transcripts → website copy patterns |
| Technical accuracy standards | Installation guides → product specs → client corrections |
| Specificity rules | Client feedback → style guide revisions → audit findings |
| Page structure | Style guides → audit reports → client-approved templates |
| SEO standards | Style guides → keyword research → website meta patterns |
| Product/collection reference | Website research → product specs |
| Pre-submission checklist | Compiled from all rules above |

### Synthesis rules

- **Client corrections override everything.** If a transcript or channel message shows the client rejecting a pattern, that rejection is law.
- **Specifics over abstractions.** Extract exact terminology, exact banned words, exact required phrases — not summaries of them.
- **Include verbatim copy blocks** where the client has mandated exact wording (e.g., shipping copy, sealing disclaimers).
- **Flag unresolved conflicts.** If two raw sources disagree and no client correction settles it, add a `⚠ UNRESOLVED` flag with both positions.
- **Date-stamp the output.** Include `Generated: YYYY-MM-DD` and list which raw files were consumed.

4. **Writes the output** to `clients/{client}/STYLE-SYSTEM.md`

## Output format

The generated STYLE-SYSTEM.md follows this structure:

```markdown
# {Client Name} — Style System

Generated: {date}
Sources: {list of raw files consumed}
Base rules: universal-rules/UNIVERSAL-RULES.md

## 1. Brand & Audience
## 2. Voice & Tone
## 3. Terminology
### 3.1 Required terms
### 3.2 Strict avoidance list
## 4. Accuracy & Technical Standards
## 5. Specificity Rules
## 6. Page Structure
## 7. SEO Standards
## 8. Product/Collection Reference
## 9. Pre-Submission Checklist
```

## Adding a new client

1. Create `clients/{new-client}/raw/` and populate with research, transcripts, style guides, website data
2. Run `/generate-style-system {new-client}`
3. Review the generated STYLE-SYSTEM.md and correct any extraction errors
4. Create `clients/{new-client}/campaigns/` when campaign work begins
