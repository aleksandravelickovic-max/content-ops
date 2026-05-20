# Content pipeline runbook

How to produce and verify Zia content agentically with this toolkit. Built 2026-05-19. The reference client is Zia Tile; the same shape ports to other clients once they have the per-client infrastructure.

## The model

Three tiers, cheapest first:
- **Opus** orchestrates (`/run-piece`, `/sku-multiplier`).
- **Sonnet** writes and judges (drafters, `voice-judge`, `koray-judge`, `claims-grounding`).
- **Haiku** runs the mechanical enforcers (`material-guard`, `terminology-lint`, `contact-line-check`, `person-consistency`).

Enforcers run before judges: a piece that fails a cheap mechanical check never reaches a scored judge.

## Per-client setup (already done for Zia)

```
clients/zia-tile/
├── STYLE-SYSTEM.md          # canonical authority (unchanged)
├── COMPLIANCE.yml           # fail-closed banned terms + technical guards
├── contact-block.md         # required contact line
├── materials/               # one config per material (the freeze/thaw/pool/sealing truth)
│   ├── _SCHEMA.md
│   ├── cotto.md  cotto-allende.md  zellige.md  unglazed-zellige.md
│   ├── cement.md  marble.md  roman-mosaics.md  terrazzo.md
│   └── glass-mosaics.md  limestone.md  ceramics.md  cantera.md
└── page-templates/
    ├── collection.md        # opener + [PRODUCT LIST] + FAQ
    ├── product.md           # 9-section §8.5 spine
    └── blog.md              # AD/Wallpaper editorial
```

To onboard another client, replicate this shape: write its STYLE-SYSTEM.md, its COMPLIANCE.yml, its contact-block.md, one material config per material it sells, and its page templates.

## The eleven stages (`/run-piece`)

| # | Stage | Tier | Gate |
|---|---|---|---|
| 1 | `/brief` | sonnet | advisory |
| 2 | `/draft-{type}` | sonnet | advisory (self-checks) |
| 3 | `material-guard` | haiku | critical |
| 4 | `terminology-lint` | haiku | critical |
| 5 | `claims-grounding` | sonnet | critical |
| 6 | `person-consistency` | haiku | critical |
| 7 | `contact-line-check` | haiku | critical |
| 8 | `/humanize` | sonnet | advisory |
| 9 | `/ship` | sonnet | critical |
| 10 | `voice-judge` | sonnet | gate >=80 |
| 11 | `koray-judge` | sonnet | gate >=80 |

Any critical failure halts and writes `BLOCKED.md`. Success writes the draft + `RUN-SUMMARY.md` + `state.json` under `campaigns/{campaign}/runs/{slug}/`.

## Common workflows

**One new collection page**
```
/run-piece zia-tile collection cotto-allende "Cotto Allende collection page"
```

**One new product/SKU page**
```
/draft-product-page zia-tile cotto "Red Clay" 8x8
```

**Promote a v3 revision (Stream A)**
```
/promote-v3 clients/zia-tile/campaigns/01-product-collection-pages/drafts/v3/10-terrazzo.md
/promote-v3 clients/zia-tile/campaigns/01-product-collection-pages/drafts/v3/10-terrazzo.md --apply
```

**Apply audit-report findings (Stream C)**
```
/audit-fix clients/zia-tile/campaigns/01-product-collection-pages/drafts/01-zellige.md
```

**Scale one collection into SKUs (max 5 per batch)**
```
/sku-multiplier zia-tile cotto clients/zia-tile/campaigns/01-product-collection-pages
```

**Review a backlog without opening each file**
```
/batch-review clients/zia-tile/campaigns/01-product-collection-pages/drafts/
```

## Try it tomorrow (team test plan)

1. **Discovery check.** From `content-ops/`, run `claude` and confirm `/run-piece`, `/promote-v3`, `/draft-collection-page` autocomplete, and that `material-guard` etc. are listed as agents.
2. **Read a worked example.** Open `clients/zia-tile/campaigns/01-product-collection-pages/runs/collection-cotto-allende/` — `draft.md` is a pipeline-produced collection page, `RUN-SUMMARY.md` shows the gate scores (voice 86, koray 84).
3. **Run the gate on something real.** Pick a v3 file and run `/promote-v3 <path>` (no `--apply`). It returns an audit-report compliance verdict.
4. **Try a fresh piece.** `/run-piece zia-tile collection terrazzo "Terrazzo collection page"` and watch the stages. Confirm it halts if you inject an error (e.g., add "approved for pools" to a Cotto draft and run `material-guard` — it must BLOCK).
5. **Batch-review the 16 templates.** `/batch-review clients/zia-tile/campaigns/01-product-collection-pages/drafts/` for a backlog-wide gate matrix.

## Guarantees and limits

- **No invention.** Material rules come from STYLE-SYSTEM + audited drafts. Unconfirmed rules are `verify`-gated and surfaced for Alex, never asserted.
- **material-guard is the safety net** for the Cotto vs Cotto Allende trap (opposite pool + freeze/thaw rules). It treats a wrong material rule as a critical, QA-failing error.
- The gates do not replace editorial review. Aleksandra + Emanuel pair review and Jamie sign-off still apply; the gates raise the floor so review starts from a clean draft.
