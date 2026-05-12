# Content Ops — Project Instructions

You write and edit content for LinkGraph clients and internal SearchAtlas content.

## Canonical references

- **Writing rules:** `style-system/STYLE-SYSTEM.md` — all stylistic, structural, and semantic SEO rules for content production. Apply to all work unless a client's brand voice explicitly overrides.
- **Client brand voice:** `clients/{client}/BRAND-VOICE.md` — client-specific voice, terminology, technical standards, and page structure rules.
- **Shared knowledge:** `knowledge/` — SearchAtlas platform data (products, competitors, facts, testimonials, proof). Shared across all clients.
- **Client knowledge:** `clients/{client}/research/` — client-specific research, website data, editorial research, meeting recaps.

## Active clients

| Client | Directory | Brand voice |
|---|---|---|
| Zia Tile | `clients/zia-tile/` | `clients/zia-tile/BRAND-VOICE.md` |
| SearchAtlas | `clients/searchatlas/` | (uses style-system defaults) |

## Campaign structure

Work products are organized by client and campaign:
```
clients/{client}/campaigns/{nn}-{campaign-name}/
  ├── brief.md
  ├── audit-report.md (if applicable)
  └── drafts/
```

## Rules of engagement

1. Always load the client's `BRAND-VOICE.md` before writing or editing client content.
2. Always load `style-system/STYLE-SYSTEM.md` for universal writing standards.
3. Use `knowledge/` as the source of truth for SearchAtlas product data — do not invent capabilities, pricing, or behavior.
4. Use `clients/{client}/research/` for client-specific data — do not invent product specs or capabilities.
5. When conflicts exist between style-system and brand-voice, **brand-voice wins** for that client.
