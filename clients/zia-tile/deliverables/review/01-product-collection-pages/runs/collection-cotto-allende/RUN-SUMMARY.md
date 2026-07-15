# Run summary: collection-cotto-allende

Pipeline verification run produced by exercising the full `/run-piece` flow by hand on 2026-05-19. Proves the Onda 1+2 gates + Onda 3 drafter produce a publishable Zia collection page.

- **Client / type / material:** zia-tile / collection / cotto-allende
- **Output:** [draft.md](./draft.md)
- **Stages:** all 11 passed
- **Voice score:** 86/100 (PASS, gate >=80)
- **Koray score:** 84/100 (PASS, gate >=80)
- **Model tiers (intended):** opus (orchestrator), sonnet (draft + judges), haiku (mechanical enforcers)

## Gate results

| Stage | Gate | Result | Note |
|---|---|---|---|
| material-guard | critical | PASS | Cotto vs Cotto Allende assignment correct (pools yes, freeze/thaw no); sealing not combined; no zellige-trio misuse |
| terminology-lint | critical | PASS | No banned terms; "eighteen" written out; no "sub-line"; "terra cotta" lowercase |
| claims-grounding | critical | PASS | Colorways, shapes, finishes trace to STYLE-SYSTEM §5.4; no kiln type; no light-exposure patina |
| person-consistency | critical | PASS | First person held; no second person in answers |
| contact-line-check | critical | PASS | info@ziatile.com + 310-844-1170 in install FAQ and overage FAQ |
| ship QA | critical | PASS after fix | One minor finding fixed: install-guide link added as markdown |
| voice-judge | gate >=80 | 86 | Strong specificity and lead; functional FAQ closer keeps it below "exceptional" |
| koray-judge | gate >=80 | 84 | Internal-link depth was the weakest dimension; fixed by adding the install-guide link |

## What this verifies for the team

1. The material config (`materials/cotto-allende.md`) correctly drove the hardest Zia trap (Cotto vs Cotto Allende pools/freeze-thaw/sealing) without error.
2. The mechanical enforcers (haiku) catch factual + terminology + contact + person issues before the scored judges run.
3. The scored judges (sonnet) gate at >=80 and surface the weakest dimension with a concrete fix.
4. The draft matches the approved golden-reference pattern (collection-cotto.md): frontmatter, "Our Take on [Material]" opener, [PRODUCT LIST] placeholder, FAQ block with the Cotto vs Cotto Allende framing.

## For Alex / editorial review

- `[PRODUCT LIST]` is an intentional placeholder; the live collection page renders the product grid dynamically.
- All material rules used were `confidence: high`. No verify-gated assumptions.
- Ready for editorial pair review (Aleksandra + Emanuel), then Jamie sign-off, same gate as the rest of campaign 02.
