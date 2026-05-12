# Content Ops — Project Instructions

You write and edit content for LinkGraph clients.

## Canonical references

- **Universal writing rules:** `style-system/STYLE-SYSTEM.md` — stylistic, structural, and semantic SEO rules applied to all work unless a client's style system explicitly overrides.
- **Client style system:** `clients/{client}/STYLE-SYSTEM.md` — client-specific voice, terminology, technical standards, page structure, and pre-submission checklist. Generated from raw materials via `scripts/generate-client-style-system.md`.
- **Client raw materials:** `clients/{client}/raw/` — unprocessed inputs (transcripts, research, website data, editorial analysis, knowledge bases). These feed into the client's STYLE-SYSTEM.md.
- **Client campaigns:** `clients/{client}/campaigns/{nn}-{name}/` — work products organized by campaign (briefs, drafts, reviews, audits).

## Client directory structure (universal)

Every client follows this layout:

```
clients/{client}/
├── STYLE-SYSTEM.md              # Processed output: canonical brand style
├── raw/                         # Unprocessed inputs
│   ├── transcripts/             # Meeting transcripts
│   ├── research/                # Website research, editorial voice, style guides
│   └── knowledge/               # Product data, competitors, facts (if applicable)
└── campaigns/
    └── {nn}-{campaign-name}/
        ├── brief.md
        ├── drafts/
        └── reviews/
```

## Active clients

| Client | Style system | Notes |
|---|---|---|
| Zia Tile | `clients/zia-tile/STYLE-SYSTEM.md` | Premium artisanal tile retailer. AD/Wallpaper* voice register. |
| SearchAtlas | `clients/searchatlas/STYLE-SYSTEM.md` | Internal platform content. Uses universal defaults + SA knowledge base. |

## Rules of engagement

1. Always load the client's `STYLE-SYSTEM.md` before writing or editing client content.
2. Always load `style-system/STYLE-SYSTEM.md` for universal writing standards.
3. Use `clients/{client}/raw/knowledge/` as the source of truth for product data — do not invent capabilities, pricing, or behavior.
4. When conflicts exist between universal and client style systems, **the client's style system wins**.
5. To regenerate a client's style system after adding new raw materials, run `scripts/generate-client-style-system.md`.
