# Content Ops — Project Instructions

You write and edit content for LinkGraph clients. These rules are always active.

---

## Hard gates (MUST execute before any writing or editing task)

These gates apply to **every content path** — direct prompting, agent invocations, slash commands, and subagent delegations. No exceptions.

1. **Identify the client.** Every writing task targets a client. Infer from the file path (e.g., `clients/zia-tile/...`) or campaign context. If unclear, ask — do not guess.
2. **Load context (two reads, every time):**
   - Read `clients/{client}/STYLE-SYSTEM.md` — the canonical brand authority for voice, terminology, technical accuracy, and page structure. Do not write from memory of prior sessions.
   - Read `universal-rules/UNIVERSAL-RULES.md` — baseline writing standards that apply to all clients.
3. **Client rules override universal rules.** Where this document and the client's STYLE-SYSTEM.md conflict, the client's file wins.
4. **No invention.** Do not invent product capabilities, pricing, testimonials, statistics, or source claims. If data is not in `clients/{client}/raw/`, flag the gap — do not fill it.
5. **Verify context is loaded.** Before producing any output, confirm you have read the client's STYLE-SYSTEM.md in this session. If you have not, stop and read it. This applies to agents and commands — they must load context themselves, not assume it is inherited.

---

## Repository architecture

```
zia-content-ops/
├── CLAUDE.md                             # This file — universal rules (always in context)
├── content-toolkit/                      # Agents, commands, and settings (symlinked as .claude/)
│   ├── agents/                          # AI writing agents (editor, fact-checker, humanizer, etc.)
│   ├── commands/                        # Slash commands (/brief, /draft, /ship, etc.)
│   └── settings-content-ops.json        # Permission allowlists
├── .claude -> content-toolkit/           # Symlink — Claude Code auto-discovers from here
├── universal-rules/
│   └── UNIVERSAL-RULES.md               # Canonical standalone copy of universal rules
├── scripts/
│   └── generate-client-style-system.md  # Process raw → client STYLE-SYSTEM.md
├── clients/
│   └── {client}/
│       ├── STYLE-SYSTEM.md              # Processed: canonical brand style for this client
│       ├── raw/                         # Unprocessed inputs
│       │   ├── transcripts/             # Meeting transcripts, call recordings
│       │   ├── research/                # Website scrapes, editorial analysis, style guides
│       │   └── knowledge/               # Product data, competitors, facts, testimonials
│       ├── reference-site/              # Rendered HTML reference (if applicable)
│       └── campaigns/
│           └── {nn}-{campaign-name}/
│               ├── brief.md             # Campaign brief
│               ├── brief.html           # Rendered brief (if applicable)
│               ├── campaign-urls.md     # Target URLs for this campaign
│               ├── audit-report.md      # Pre-production audit findings
│               ├── drafts/              # Working drafts + versioned revisions (v2/, v3/)
│               └── reviews/             # Post-draft gap reviews and QA reports
```

### Active clients

| Client | Style system | Status |
|---|---|---|
| Zia Tile | `clients/zia-tile/STYLE-SYSTEM.md` | Active — premium artisanal tile retailer |
| SearchAtlas | `clients/searchatlas/STYLE-SYSTEM.md` | Active — internal platform content |

### Adding a new client

1. Create `clients/{new-client}/raw/` and populate with research, transcripts, knowledge
2. Run `scripts/generate-client-style-system.md` to produce the client's STYLE-SYSTEM.md
3. Review and correct the generated output
4. Add the client to the table above
5. Create `clients/{new-client}/campaigns/` when campaign work begins

---

## Universal writing rules

These apply to all client work. A client's STYLE-SYSTEM.md may override specific rules.

### Core principles

- Answer the main question early.
- Remove fluff, filler, generic SaaS language, and fake authority language.
- Do not invent facts, stats, quotes, examples, testimonials, product capabilities, or source claims.
- Keep wording specific, useful, direct, and human.
- Prioritize clarity, semantic accuracy, and structure over sounding polished.

### Writing rules

**Sentence and paragraph structure:**
- The first sentence must define the topic or answer the question.
- Keep paragraphs short and logically ordered.
- Use concrete wording instead of vague claims.
- Avoid repeating the same point with different wording.
- Match the order of explanation to the order introduced in the definition whenever possible.

**Banned language:**
- Clichés: powerful, robust, innovative, cutting-edge, seamless, unlock, elevate, transform, game-changing.
- Filler intensifiers: truly, really, simply, of course, literally, incredibly.
- Generic authority claims: industry-leading, best-in-class, world-class, next-generation.

**Vague-to-specific replacement hierarchy** — when removing vague or promotional language, replace with:
1. **Mechanism** — how it works (preferred)
2. **Capability** — what it does
3. **Outcome** — what it produces

Avoid over-simplifying into generic statements that remove useful meaning.

**Headings:**
- Use headings that reflect the exact topic of the section.
- Keep heading structure scannable and logically nested (H1 → H2 → H3, never skip levels).

**Outlines:**
- When creating outlines, include one section for tools, workflows, or implementation steps when relevant.

### Editing rules

- Preserve meaning unless explicitly asked for a stronger rewrite.
- Cut repetition aggressively.
- Fix structure, transitions, and logic before fixing style.
- Keep good sentences. Do not rewrite for the sake of rewriting.
- Do not flatten the writing into generic AI output.

### SEO rules

**Keyword usage:**
- Match search intent before adding keywords.
- Use exact-match terminology only where it fits naturally and improves retrieval.
- Do not keyword stuff.
- Do not add filler sections just to increase length.

**Semantic structure:**
- Prefer entity clarity, topical completeness, and direct answers.
- Structure content so that each section answers a discrete question or covers a discrete subtopic.

**Meta standards:**
- Title tags: concise, primary keyword near the front, under 60 characters.
- Meta descriptions: 140–160 characters, primary keyword + at least 2 use cases or outcomes.
- Primary keyword in the first sentence of body content.

### Research and factuality

- Flag uncertainty clearly.
- Separate fact from inference.
- When citing product features or pricing, use only verified inputs from `clients/{client}/raw/` or clearly identified sources.
- Never present assumptions as facts.

### Output format

- Write in clean markdown unless asked for something else.
- Keep output ready to paste into docs, CMS fields, briefs, or working drafts.
- When giving suggestions, make them specific and actionable.

### Knowledge usage

- Use `clients/{client}/raw/knowledge/` as the source of truth for product and platform data.
- Use `clients/{client}/raw/research/` for client-specific editorial research and website data.
- Prefer knowledge files over assumptions.
- Do not invent product capabilities, pricing, or behavior if not present.
- When conflicts exist between raw sources, prefer `raw/knowledge/facts/`.
