---
description: Rewrite text — strip fluff, improve specificity, preserve meaning.
argument-hint: <text to rewrite>
---

Rewrite the text below following the rules in `CLAUDE.md`.

## Input
$ARGUMENTS

## Rules
1. **Remove fluff.** Cut clichés (powerful, innovative, seamless, transform, unlock, elevate, robust, cutting-edge, game-changing), filler phrases, and generic SaaS language.
2. **Improve specificity using this hierarchy, in order of preference:**
   1. Mechanism — how it works
   2. Capability — what it does
   3. Outcome — what it produces
   Prefer mechanism over outcome when both are possible.
3. **Preserve meaning.** Do not add new claims, widen the scope, narrow the scope, or change the level of certainty unless I explicitly ask for it.
4. **Do not over-simplify.** Avoid flattening into generic statements that strip useful meaning.
5. **Flag unverifiable claims.** If the rewrite would require product capabilities, stats, pricing, or facts not present in the input, stop and flag them instead of inventing.

## Output format
- **Rewrite:** one tight version.
- **What changed:** one or two bullets naming the most important substitutions only.
- **Flags:** list unverifiable claims or missing inputs only when relevant. Omit this section if there are none.
- Keep the full output concise.
