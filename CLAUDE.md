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

This repo has two distinct halves: **content** (client writing, campaigns, style systems) and **app** (the review portal). They are designed to be separable — the app reads content via a configurable `CONTENT_ROOT` path and can eventually live in its own repo.

### Content (this repo's primary purpose)

```
zia-content-ops/
├── CLAUDE.md                             # This file — project rules (always in context)
├── README.md / README.html               # Project overview (HTML version for stakeholders)
├── content-toolkit/                      # Agents, commands, and settings (symlinked as .claude/)
│   ├── agents/                          # AI writing agents (editor, fact-checker, humanizer, etc.)
│   ├── commands/                        # Slash commands (/brief, /draft, /ship, etc.)
│   ├── settings-content-ops.json        # Permission allowlists
│   ├── codebase-map.md                  # Auto-generated — do not edit
│   └── codebase-map-meta.json           # Auto-generated — do not edit
├── .claude -> content-toolkit/           # Symlink — Claude Code auto-discovers from here
├── universal-rules/
│   └── UNIVERSAL-RULES.md               # Canonical standalone copy of universal rules
├── scripts/                             # Content build tools (not app code)
│   ├── generate-client-style-system.md  # LLM prompt/procedure — not an executable script
│   ├── build-content-navigator.py       # Generates content-navigator.html + registry.json files
│   └── build-html-before-after.py       # Generates before/after HTML comparisons from drafts
├── reports/                             # Generated output from build scripts
│   ├── content-navigator.html           # Standalone content browser (no server needed)
│   ├── SPEC-client-annotations.md       # Annotation system specification
│   └── *.html                           # Audit reports, comparisons
├── clients/
│   └── {client}/
│       ├── STYLE-SYSTEM.md              # Processed: canonical brand style for this client
│       ├── registry.json                # Auto-generated content index for this client
│       ├── raw/                         # Unprocessed inputs (subdirs created as needed)
│       │   ├── transcripts/             # Meeting transcripts, call recordings
│       │   ├── research/                # Website scrapes, editorial analysis, style guides
│       │   └── knowledge/               # Product data, competitors, facts, testimonials
│       ├── reference-site/              # Rendered HTML reference (if applicable)
│       └── campaigns/
│           └── {nn}-{campaign-name}/
│               ├── brief.md             # Campaign brief (or briefs/ directory for multi-brief campaigns)
│               ├── brief.html           # Rendered brief (if applicable)
│               ├── campaign-urls.md     # Target URLs for this campaign
│               ├── audit-report.md      # Pre-production audit findings
│               ├── registry.json        # Auto-generated content index for this campaign
│               ├── gdocs-content/       # Google Docs exports (collection-pages/, product-pages/)
│               ├── drafts/              # Working drafts + versioned revisions (v2/, v3/)
│               └── html/               # Before/after HTML comparisons (original/ + revised/)
```

### App — Content Review Portal (`portal/`)

A standalone FastAPI application for shareable content review with commenting. Designed to be hosted independently — reads content from the filesystem via `CONTENT_ROOT` env var.

```
portal/
├── Dockerfile                           # Python 3.12-slim, uvicorn
├── docker-compose.yml                   # Postgres + app, mounts ../clients as read-only volume
├── requirements.txt                     # Python dependencies (fastapi, sqlalchemy, etc.)
├── manage.py                            # CLI: init-db, create/list/revoke share links, list comments
├── env-example.txt                      # Template for .env
├── app/
│   ├── main.py                          # FastAPI app setup, routes, static files
│   ├── config.py                        # Env-based config (DATABASE_URL, CONTENT_ROOT, secrets)
│   ├── database.py                      # Async SQLAlchemy (Postgres in prod, SQLite for dev)
│   ├── models.py                        # ShareLink, Comment models
│   ├── content.py                       # Reads campaign content from filesystem via registry.json
│   ├── routes/
│   │   ├── admin.py                     # Dashboard, share link management, comment moderation
│   │   ├── review.py                    # Client-facing review pages (accessed via share links)
│   │   └── api.py                       # JSON API for comments (create, resolve)
│   ├── static/
│   │   ├── styles.css                   # Portal layout and styling
│   │   ├── app.js                       # Comment UI, review interactions
│   │   ├── annotation.css               # Inline annotation highlighting and sidebar
│   │   └── annotation.js               # Text selection → annotation creation, highlight rendering
│   └── templates/
│       ├── base.html                    # Jinja2 base template
│       ├── auth/
│       │   └── login.html               # Admin login page
│       ├── admin/
│       │   ├── dashboard.html           # Admin overview — share links, stats
│       │   └── comments.html            # Comment moderation view
│       └── review/
│           ├── campaign.html            # Campaign-level content listing
│           └── content.html             # Single content piece with annotation sidebar
```

**Running the portal:**
- Dev: `cd portal && uvicorn app.main:app --reload` (uses SQLite, reads `../clients`)
- Prod: `cd portal && docker compose up` (uses Postgres, mounts `../clients` read-only)
- Key env vars: `CONTENT_ROOT`, `DATABASE_URL`, `ADMIN_PASSWORD`, `SECRET_KEY`, `BASE_URL`

**Content ↔ App boundary:** The portal never writes to content files. It reads them via `CONTENT_ROOT` (defaults to `../clients`). In Docker, `../clients` is mounted as a read-only volume. This means the portal can be moved to its own repo and pointed at any content directory.

### Active clients

| Client | Style system | Status |
|---|---|---|
| Zia Tile | `clients/zia-tile/STYLE-SYSTEM.md` | Active — premium artisanal tile retailer |
| SearchAtlas | `clients/searchatlas/STYLE-SYSTEM.md` | Active — internal platform content |
| Altify | `clients/altify/STYLE-SYSTEM.md` | Active — enterprise account planning AI platform (Salesforce-native) |
| 5Gstore | `clients/5gstore/STYLE-SYSTEM.md` | Active — specialized 4G/5G networking equipment retailer |

### Adding a new client

1. Create `clients/{new-client}/raw/` and populate with research, transcripts, knowledge
2. Follow the LLM prompt in `scripts/generate-client-style-system.md` to produce the client's STYLE-SYSTEM.md
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
