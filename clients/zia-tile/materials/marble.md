---
material: marble
display_name: Marble
glazed: n/a
origin: Italy + Spain
freeze_thaw: not_suitable
pools_spas: not_suitable
variation_trio_applies: false
variation_language: [veining, tone, natural stone variation, honed or polished finish]
sealing_profile: natural-stone
confidence: high
source: STYLE-SYSTEM.md §4.1, §11, §12; raw/research/materials-reference.md v3 Quick Reference (Emanuel, 2026-05-20, live-site precedence)
---

# Marble (Solid) — material rules

Natural quarried stone from Italy and Spain. Named stones: Carrara, Nero Marquina, Grigio Carnico, Rosso Alicante, Giallo Reale, Verdi Alpi. Honed or polished.

## Freeze/thaw — NOT SUITABLE (Ext Non-F/T ✓ only)

Per the Materials Reference Guide v3 Quick Reference: Marble Ext F/T = ✗, Ext Non-F/T = ✓. STYLE-SYSTEM §4.1's "can be used outdoors in appropriate climates" = NON-freeze/thaw climates specifically. The earlier `suitable` value was too permissive; the matrix corrects to not_suitable for freeze/thaw exteriors. The "Marble Patterns" sub-line shares this rule.

## Pools & spas — NOT SUITABLE

Per the Materials Reference Guide v3 Quick Reference: Marble Pool/Spa = ✗. Marble is NOT pool/spa approved. The sub-line Roman Mosaics IS pool-approved — do not transfer that rule to Marble.

## Sealing — profile: natural-stone

Natural stone requires sealing. Direct readers to the Installation Guide; never name sealer products in customer-facing copy.

## Variation language

- Use: veining, tone, natural stone variation, honed or polished finish.
- This is natural stone, not a fired or glazed clay product. Do NOT apply the chips/pits/crazing trio (zellige) or terra cotta variation language.

## Related: Roman Mosaics

Roman Mosaics use the same premium stone as Solid Marble but have different application rules per the live Tile Usage matrix: Roman Mosaics IS pool/spa approved (Marble is not) and IS NOT Ext Non-F/T approved (Marble is). See `roman-mosaics.md` and do not let material-guard inherit Marble rules onto a Roman Mosaics page.

## Reconciliation note (2026-05-25)

Two rule flips against Materials Reference Guide v3: freeze/thaw `suitable` → `not_suitable` (sharpened to non-F/T-only outdoor); pools/spas `verify` → `not_suitable` (confirmed).
