---
description: Make text sound natural and human without adding fluff or changing meaning.
argument-hint: <text to humanize>
---

Humanize the text below following the rules in `CLAUDE.md`.

## Input
$ARGUMENTS

## Goals
- Make the text sound natural, direct, and human-written.
- Remove AI-style phrasing patterns.
- Improve flow and readability without adding fluff.
- Preserve the original meaning exactly.

## Rules

### 1. Preserve meaning
- Do not change the claim, scope, or intent.
- Do not add new information, examples, or opinions.
- Do not exaggerate or soften claims.

### 2. Remove AI-style phrasing
- Remove patterns such as:
  - overly formal phrasing
  - generic transitions ("in today's landscape", "it is important to note")
  - repetitive sentence openings
  - "both X and Y" constructions
  - unnecessary emphasis

### 3. Improve flow
- Vary sentence structure naturally.
- Break rigid or repetitive phrasing.
- Use simpler transitions where needed.
- Avoid robotic or overly symmetrical sentences.

### 4. Keep precision
- Do not replace specific language with vague language.
- Keep technical terms where they are correct.
- Do not simplify to the point of losing meaning.

### 5. Keep it tight
- Do not add filler or extra sentences.
- Do not expand the text.
- Keep the length similar or slightly shorter.

### 6. Natural tone
- Write as a clear, competent human editor.
- Avoid:
  - hype language
  - overly casual tone
  - slang
  - jokes

### 7. Sentence quality
- Prefer clean, direct sentences.
- Split overly long sentences when needed.
- Remove awkward or forced phrasing.

## Output format
- **Humanized:** one improved version
- **What changed:** 2–3 bullets describing the main improvements

## Constraints
- Do not add fluff.
- Do not use em dashes.
- Do not introduce meta language or commentary.
