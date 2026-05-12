# Stylometric SEO Writing System

Canonical source of all stylistic, structural, and semantic SEO rules for content production. Referenced by CLAUDE.md and applied to all client work unless a client's BRAND-VOICE.md explicitly overrides a specific rule.

## 1. Core principles

- Answer the main question early.
- Remove fluff, filler, generic SaaS language, and fake authority language.
- Do not invent facts, stats, quotes, examples, testimonials, product capabilities, or source claims.
- Keep wording specific, useful, direct, and human.
- Prioritize clarity, semantic accuracy, and structure over sounding polished.

## 2. Writing rules

### 2.1 Sentence and paragraph structure
- The first sentence must define the topic or answer the question.
- Keep paragraphs short and logically ordered.
- Use concrete wording instead of vague claims.
- Avoid repeating the same point with different wording.
- Match the order of explanation to the order introduced in the definition whenever possible.

### 2.2 Banned language
- Avoid clichés: powerful, robust, innovative, cutting-edge, seamless, unlock, elevate, transform, game-changing.
- Avoid filler intensifiers: truly, really, simply, of course, literally, incredibly.
- Avoid generic authority claims: industry-leading, best-in-class, world-class, next-generation.

### 2.3 Vague-to-specific replacement hierarchy
When removing vague or promotional language, replace it with concrete alternatives. Prioritize in this order:
1. **Mechanism** — how it works
2. **Capability** — what it does
3. **Outcome** — what it produces

Prefer mechanism over outcome when both are possible. Avoid over-simplifying into generic statements that remove useful meaning.

### 2.4 Headings
- Use headings that reflect the exact topic of the section.
- Keep heading structure scannable and logically nested.

### 2.5 Outlines
- When creating outlines, include one section for tools, workflows, or implementation steps when relevant.

## 3. Editing rules

- Preserve meaning unless explicitly asked for a stronger rewrite.
- Cut repetition aggressively.
- Fix structure, transitions, and logic before fixing style.
- Keep good sentences. Do not rewrite for the sake of rewriting.
- Do not flatten the writing into generic AI output.

## 4. SEO rules

### 4.1 Keyword usage
- Match search intent before adding keywords.
- Use exact-match terminology only where it fits naturally and improves retrieval.
- Do not keyword stuff.
- Do not add filler sections just to increase length.

### 4.2 Semantic structure
- Prefer entity clarity, topical completeness, and direct answers.
- Structure content so that each section answers a discrete question or covers a discrete subtopic.
- Heading hierarchy (H1 → H2 → H3) must be logically nested — never skip levels.

### 4.3 Meta standards
- Title tags: concise, primary keyword near the front, under 60 characters.
- Meta descriptions: 140–160 characters, primary keyword + at least 2 use cases or outcomes.
- Primary keyword in the first sentence of body content.

## 5. Research and factuality

- Flag uncertainty clearly.
- Separate fact from inference.
- When citing product features or pricing, use only verified inputs from provided material or clearly identified sources.
- Never present assumptions as facts.

## 6. Output format

- Write in clean markdown unless asked for something else.
- Keep output ready to paste into docs, CMS fields, briefs, or working drafts.
- When giving suggestions, make them specific and actionable.

## 7. Knowledge usage

- Use information from `clients/{client}/raw/knowledge/` as the source of truth for product and platform data.
- Use information from `clients/{client}/raw/` as the source of truth for client-specific research and inputs.
- Prefer knowledge files over assumptions.
- Do not invent product capabilities, pricing, or behavior if not present.
- When conflicts exist, prefer facts in `/knowledge/facts/`.
