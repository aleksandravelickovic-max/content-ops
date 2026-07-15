# QA Log: Roto-Rooter Water Damage Blogs

## Context loaded

- Client: Roto-Rooter.
- Local `STYLE-SYSTEM.md`: not available in `clients/roto-rooter/`.
- Universal rules loaded.
- Human-writing skill loaded.
- Source notes reviewed.

## Round 1: Factual grounding

- Removed the unverified Money.com, State Farm, ice-dam, and mold-cost figures from final body copy.
- Kept verified 24 to 48 hour mold/drying timing from EPA and CDC.
- Kept RR claims limited to verified service pages: IICRC certification, 24/7 service, water categories, moisture sensors, drying logs, camera inspection, insurance documentation, mold remediation.

## Round 2: PR angle and structure

- Strengthened Article A headline and opening around hidden water damage before stains appear.
- Reframed Article B around the verified urgency story: drying vs replacing, 24 to 48 hour window, and scope creep from delay.
- Removed final-copy editor notes from the article body.

## Round 3: Structure, duplication, and claim precision

- Checked both final drafts for repeated section logic and unsupported cost claims.
- Replaced loose PR phrasing such as "best chance" and "Roto-Rooter states" with more precise wording.
- Kept Article B cost discussion scope-based instead of dollar-based because the supplied numerical claims remain unverified.

## Round 4: Voice and anti-slop

- Scanned both final drafts for banned phrases, decorative transitions, rule-of-three cadence, and generic authority language.
- No banned marketing phrases remained in final copy.
- Broke dense paragraphs into cleaner editorial rhythm and simplified one stiff mitigation sentence.

## Round 5: Final publish-readiness

- Checked headings, title tags, meta descriptions, word counts, and final-copy residue.
- Reran banned-language and unsupported-claim scans with a corrected regex.
- Lengthened both meta descriptions to meet the 140 to 160 character target.
- Ran `python3 -m py_compile scripts/build-content-navigator.py` as a lightweight repo sanity check.

## PR-specific pass

- Added PR hooks to both final files so the GDocs version has a clear media angle.
- Added suggested RR expert quotes, clearly labeled for approval rather than attributed to a named spokesperson.
- Sharpened Article A around seasonal homeowner risk and the "inspect before you demolish" message.
- Sharpened Article B around the first 48 hours, drying vs replacing, and the three preventable decisions homeowners get wrong.
- Kept unverified dollar figures out of the final body copy.
