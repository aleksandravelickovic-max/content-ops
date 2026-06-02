# Campaign 02 — March/April Updates

**Status:** Step 0 scaffold, worklists scoped to real artifacts in the repo
**Owner:** Aleksandra Velickovic
**Editorial pair:** Aleksandra + Emanuel
**Client review:** Jamie Greenspan
**Started:** 2026-05-13

---

## Scope

Two streams of work still open from the March/April 2026 cycle. Both target artifacts that already exist in [campaigns/01-product-collection-pages/](../01-product-collection-pages/) — nothing has to be re-collected from Google Docs.

| Stream | What | Worklist | Source-of-truth |
|---|---|---|---|
| **A — v3 promotions** | Promote signed-off `drafts/v3/` revisions to `drafts/` (or to live) | [v3-promotion-worklist.md](v3-promotion-worklist.md) | [drafts/v3/](../01-product-collection-pages/drafts/v3/) — 8 templates (09–16) |
| **C — audit-report.md gaps** | Apply [audit-report.md](../01-product-collection-pages/audit-report.md) findings to the 16 category templates in `drafts/` | [audit-report-gaps.md](audit-report-gaps.md) | [audit-report.md](../01-product-collection-pages/audit-report.md) — v2.0 Editorial Style Guide (April 2026) findings |

Stream B (new drafts) is **out of scope** for this campaign — confirmed 2026-05-13.

---

## Why these two

- **Stream A** exists because 8 templates (09–16) have a `v3/` revision but `drafts/` still holds the older version. Whichever v3s Jamie has cleared need to land in `drafts/`.
- **Stream C** exists because the May 12 Gemini patch (commit `2ee3699`) **did not touch any of the 16 templates** — it patched 35 files in `gdocs-content/` (24 collection pages, 11 product pages) only. The 16 category templates still need the audit-report.md restructuring: 9-section reorg, 25% overage option, inline sealing per use case, ⅛" slip-resistance spec, affirmative freeze/thaw prose, fixed heading hierarchy, verbatim shipping copy, "free pickup" rewording.

This is the largest discovery from Step 0: the May 12 audit fixed SKU drift, not the systemic template structure flagged in audit-report.md. Stream C is the actual unfinished work from the April v2.0 style guide.

---

## Workflow

1. **Step 0 (done):** scaffold in place, worklists scoped to real artifacts.
2. **Step 1 — populate the two worklists:**
   - Stream A: diff `drafts/{09..16}.md` vs. `drafts/v3/{09..16}.md`, mark each v3 as Approved / In Review / Rejected based on Jamie's signoff.
   - Stream C: enumerate audit-report.md findings (Critical / Major / Minor) per template, mark each as Outstanding / Patched / Not Applicable.
3. **Step 2 — execute:**
   - Stream A: `ao spawn` per approved v3 → promote to `drafts/`, regenerate before/after HTML, PR for editorial pair sign-off.
   - Stream C: `ao batch-spawn` per (template × finding) pair → LLM-as-judge against audit-report.md → PR.
4. **Merge gate:** Aleksandra + Emanuel sign off. Collection pages held until Jamie clears (per current account state, May 2026).

See [docs/sops/agentic-content-ops-watch-along.md](../../../../docs/sops/agentic-content-ops-watch-along.md) for the prompt patterns and [docs/sops/multi-agent-tab-system-setup.md](../../../../docs/sops/multi-agent-tab-system-setup.md) for the stack install.

---

## Key artifacts already in the repo

- **Content navigator:** [reports/content-navigator.html](../../../../reports/content-navigator.html) — 17MB browsable index of all Zia content. Use this to surface state instead of building new dashboards.
- **May 12 audit:** [reports/zia-tile-style-audit-2026-05-12.html](../../../../reports/zia-tile-style-audit-2026-05-12.html) — pre/post comparison of the 35 files patched.
- **April v2.0 audit:** [audit-report.md](../01-product-collection-pages/audit-report.md) — per-template findings scored Critical / Major / Minor. This is the spec for Stream C.
- **Jamie's feedback:** [reference-site/jamie-feedback.html](../../reference-site/jamie-feedback.html) — rendered feedback set.
- **Style guide:** [STYLE-SYSTEM.md](../../STYLE-SYSTEM.md) — canonical. Absorbed v3 of the style guide on 2026-05-12 (commit `95dcb46`).

---

## Open questions before Step 2 can start

- [ ] Has Jamie signed off on any of the 8 v3 revisions? Which ones? (Stream A blocker)
- [ ] Are any of the audit-report.md findings considered Won't Fix or Out of Scope by Jamie? (Stream C trims)
- [ ] Collection pages currently held at merge — is that still the rule for v3 promotions, or only for net-new content?
