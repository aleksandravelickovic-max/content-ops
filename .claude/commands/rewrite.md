---
description: Rewrite text to improve clarity, specificity, and usefulness while preserving meaning.
argument-hint: <text to rewrite>
---

Rewrite the text below following the rules in `CLAUDE.md`.

## Input
$ARGUMENTS

## Goals
- Keep the original meaning intact.
- Make the text clearer, more direct, and more specific.
- Remove unnecessary words without removing useful information.

## Rules

### 1. Preserve meaning
- Do not change the claim, scope, or intent.
- Do not add new facts, examples, or assumptions.
- If the input is unclear, rewrite for clarity without guessing new information.

### 2. Remove fluff
- Cut filler phrases and repetition.
- Remove generic or vague wording where possible.
- Avoid cliché language such as powerful, innovative, seamless, robust, cutting-edge, transformative, game-changing, unlock, elevate, and similar filler.

### 3. Improve clarity
- Use simple, direct sentence structure.
- Break long or overloaded sentences into shorter ones if needed.
- Prefer concrete wording over abstract phrasing.

### 4. Improve specificity
- Replace vague phrases with clearer wording when the input supports it.
- Prefer:
  1. how something works
  2. what it does
  3. what it produces
- Prefer concrete nouns and verbs over abstract phrasing.

### 5. Keep structure stable
- Do not restructure the text unless necessary for clarity.
- Keep paragraphs and lists in the same order unless they are clearly confusing.

### 6. Lists
- Keep list structure consistent.
- Ensure items follow the same grammatical pattern.

### 7. No over-editing
- Keep strong sentences as they are.
- Do not rewrite for the sake of rewriting.

### 8. Flag limits
- If a stronger rewrite would require missing information, flag it instead of inventing.

## Output format
- **Rewrite:** one improved version
- **What changed:** 2–3 bullets describing the main improvements
- **Flags:** include only if something could not be improved safely

## Constraints
- Keep the output concise.
- Do not add explanations outside the required format.
- Do not use internal or meta language such as "based on sources," "analysis," or "SERP."
- Do not use em dashes.
