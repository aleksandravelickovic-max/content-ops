# BLOCKED: bathroom-tile-ideas

**Failing stages:** voice-judge (62/100), koray-judge (61/100)
**Gate:** 80 minimum for both
**Status:** Halted — do not render HTML until resolved

---

## Voice judge failures (62/100)

### 1. Generic lead — highest priority fix
Current: "The bathroom handles moisture, daily wear, and changing light while holding a design for decades."
Problem: This is a category-claim opener — the exact pattern AD/Wallpaper* never uses. STYLE-SYSTEM §2.5 and §6.1 require anchoring on a specific material, origin, or physical detail.
Fix: Open on one specific material detail or named place. Example anchor: a zellige tile's chips, pits, and crazing catching light, or the quarry origin of Carrara marble.

### 2. Closing is a marketing recap
Current: "These are materials that wear in, not out." + duplicate contact CTA
Problem: Reads as a tagline followed by a CTA. STYLE-SYSTEM §2.5 specifies: closers end on maker's intent, homeowner's words, or a practical aside — never a CTA or generic takeaway.
Fix: End on one concrete detail about one material — something specific, not a summary.

### 3. Duplicate zellige light-shift sentences
Current: "chips, pits, and crazing that catch and shift the light from every angle" followed immediately by "color and sheen that shift as light moves across the wall"
Problem: Same idea restated in two consecutive sentences. Repetition masking as specificity.
Fix: Merge into one sentence or drop the second.

### 4. Zellige CTA redirect
Current: "For the full range, visit the zellige collection at ziatile.com."
Problem: Reads as SEO boilerplate. No other material section has this. Either apply consistently or replace with a specific detail.

---

## Koray judge failures (61/100)

### 1. Query intent mismatch
Primary keyword "bathroom tile ideas" signals design inspiration and selection guidance. Section openers define material origins — they do not answer what each tile does in a bathroom context.
Fix: Reframe each H2 opener to lead with the bathroom application first (what this material does for a shower wall or bathroom floor), then deliver provenance.

### 2. Missing meta title and meta description
Required by STYLE-SYSTEM §10.3. Completely absent.
Fix: Add at top of file:
- Title: `Bathroom Tile Ideas | Zia Tile` (under 60 chars)
- Description: 140-160 chars, primary keyword + at least two use cases (shower walls, bathroom floors)

### 3. Missing internal links
Only zellige has a collection link. Marble, limestone, ceramics, and the Install Guide have none.
Fix: Add collection page links for each material. Add Installation Guide link in sealing references per Jamie's editorial rules.

### 4. Two redundant closing H2 sections
"Finish and selection" and "What bathroom tile rewards" both summarize material performance already covered per section. Creates structural confusion and dilutes heading coherence.
Fix: Merge into one closing section or cut one entirely.

---

## Summary of fixes needed before re-run

| Priority | Fix | Section |
|---|---|---|
| Critical | Replace generic lead with material-anchored opener | Intro |
| Critical | Fix duplicate zellige light-shift sentences | zellige section |
| Critical | Reframe H2 section openers to lead with bathroom application | All sections |
| Critical | Add meta title + description | Top of file |
| Major | Replace marketing closer with editorial closer | Final section |
| Major | Add internal links for marble, limestone, ceramics, Install Guide | Throughout |
| Major | Remove or replace zellige CTA redirect | zellige section |
| Minor | Merge two redundant closing H2 sections | Closing |
