# Stream A — v3 Promotion Worklist

Promote signed-off `drafts/v3/` revisions to `drafts/`. Each row below maps to one v3 file that exists in the repo. The work is: decide signoff status, then promote.

**Rule:** don't promote a v3 unless Jamie has signed off. v3 files with no signoff record stay in `drafts/v3/` until reviewed.

---

## Worklist

| # | Template | v3 file | drafts/ file | Diff command | Signoff status | Worker |
|---|---|---|---|---|---|---|
| 1 | Glass Mosaics | [drafts/v3/09-glass-mosaics.md](../01-product-collection-pages/drafts/v3/09-glass-mosaics.md) | [drafts/09-glass-mosaics.md](../01-product-collection-pages/drafts/09-glass-mosaics.md) | `diff drafts/09-glass-mosaics.md drafts/v3/09-glass-mosaics.md` | Unreviewed / In Review / Approved / Rejected | — |
| 2 | Terrazzo | [drafts/v3/10-terrazzo.md](../01-product-collection-pages/drafts/v3/10-terrazzo.md) | [drafts/10-terrazzo.md](../01-product-collection-pages/drafts/10-terrazzo.md) | `diff drafts/10-terrazzo.md drafts/v3/10-terrazzo.md` | Unreviewed | — |
| 3 | Marble Solids | [drafts/v3/11-marble-solids.md](../01-product-collection-pages/drafts/v3/11-marble-solids.md) | [drafts/11-marble-solids.md](../01-product-collection-pages/drafts/11-marble-solids.md) | `diff drafts/11-marble-solids.md drafts/v3/11-marble-solids.md` | Unreviewed | — |
| 4 | Marble Patterns | [drafts/v3/12-marble-patterns.md](../01-product-collection-pages/drafts/v3/12-marble-patterns.md) | [drafts/12-marble-patterns.md](../01-product-collection-pages/drafts/12-marble-patterns.md) | `diff drafts/12-marble-patterns.md drafts/v3/12-marble-patterns.md` | Unreviewed | — |
| 5 | Cantera | [drafts/v3/13-cantera.md](../01-product-collection-pages/drafts/v3/13-cantera.md) | [drafts/13-cantera.md](../01-product-collection-pages/drafts/13-cantera.md) | `diff drafts/13-cantera.md drafts/v3/13-cantera.md` | Unreviewed | — |
| 6 | Limestone | [drafts/v3/14-limestone.md](../01-product-collection-pages/drafts/v3/14-limestone.md) | [drafts/14-limestone.md](../01-product-collection-pages/drafts/14-limestone.md) | `diff drafts/14-limestone.md drafts/v3/14-limestone.md` | Unreviewed | — |
| 7 | Cement | [drafts/v3/15-cement.md](../01-product-collection-pages/drafts/v3/15-cement.md) | [drafts/15-cement.md](../01-product-collection-pages/drafts/15-cement.md) | `diff drafts/15-cement.md drafts/v3/15-cement.md` | Unreviewed | — |
| 8 | Roman Mosaics | [drafts/v3/16-roman-mosaics.md](../01-product-collection-pages/drafts/v3/16-roman-mosaics.md) | [drafts/16-roman-mosaics.md](../01-product-collection-pages/drafts/16-roman-mosaics.md) | `diff drafts/16-roman-mosaics.md drafts/v3/16-roman-mosaics.md` | Unreviewed | — |

Per current account state (May 2026): **Roman Mosaics → Marble, Field Trip Japan → Ceramics** reorg is pending. Confirm with Jamie before promoting 16-roman-mosaics.md.

---

## Templates without a v3 revision

Templates 01–08 do not have a `drafts/v3/` version. If they need a revision pass, they should be added to a future campaign — not this one. Templates 01–08:

- 01-zellige, 02-zellige-mosaic, 03-unglazed-natural-zellige, 04-unglazed-natural-zellige-mosaic
- 05-ceramics-matte, 06-field-trip-japan
- 07-cotto, 08-cotto-allende

`blog-04-cotto.md` (Blog Post 4 — Cotto, the test case) lives alongside the 16 templates and is tracked separately under Aleksandra + Emanuel editorial sign-off.

---

## Per-row workflow (once signoff is recorded)

1. **Approved:** `ao spawn` worker → replace `drafts/{NN}-{name}.md` with `drafts/v3/{NN}-{name}.md` contents → regenerate `html/revised/` via [build-html-before-after.py](../../../../scripts/build-html-before-after.py) → open PR.
2. **Rejected:** delete `drafts/v3/{NN}-{name}.md`, log Jamie's reason in this file's row.
3. **In Review:** leave both files in place, no PR.

---

## Out of scope

- Templates 01–08 (no v3 exists yet).
- Net-new SKU pages (those go in a separate campaign).
- Audit-report.md structural fixes — those are Stream C, applied to `drafts/` only.
