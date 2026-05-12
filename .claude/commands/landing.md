---
description: Generate a full SaaS landing page following the Search Atlas template (hero, testimonial, performance stats, two-column product explanation, capability list, getting-started steps, feature cards, comparison matrix, grouped FAQ).
argument-hint: <product or feature>
---

Create a SaaS landing page following `CLAUDE.md`.

## Step 1: Ask for missing inputs

Before generating anything, ask for:

### Required
- Product name
- Target audience (primary, secondary if any)
- Category label (e.g., "AI Google Ads Automation", "AI SEO Automation")
- 3 eyebrow tag phrases (short concrete feature signals for the top of the hero)
- Tagline (one-sentence outcome)
- Description paragraph (2 to 4 sentences, what the product does)
- Primary outcome (what measurably improves)
- Pricing positioning (cheap, mid, premium) or a pricing page URL
- 3 to 5 known competitors

### Strongly recommended (flag if missing, do not invent)
- 1 primary testimonial: full quote with a concrete metric, name, title, company
- 4 performance stats (big number + 2 to 4 word label each)
- 5 to 9 feature card inputs, each including:
  - Feature name
  - One-sentence capability
  - One-sentence mechanism (how it works)
  - CTA copy
  - A short description of the screenshot that should appear with the card
- A 5-step Getting Started workflow
- 6 to 8 capability bullets for the "What X Makes Possible" section
- 8 to 12 comparison rows (capability + how each competitor handles it)

If the user provides partial information, ask once for the gap. If they say skip, include a placeholder and list the gap in the `Flags:` block at the top of the output.

## Step 2: Competitive context (internal only)

Identify competitors from the user's list. If the user did not supply names, ask. Review for:

- common messaging patterns
- overused positioning
- feature gaps
- differentiation opportunities

Do not output sources, research notes, or any language describing how the analysis was done.

## Step 3: Positioning (internal only)

Draft internally before writing:

- Core angle (what this product does differently)
- What it replaces or improves
- Best fit user
- When NOT to choose it

Use these to steer hero, product explanation, and comparison. Do not output the positioning draft as a section; bake it into the page.

## Step 4: Generate landing page

Produce the page in this exact order, using the formats below.

### 1. Hero

```
✓ [Eyebrow tag 1]   ✓ [Eyebrow tag 2]   ✓ [Eyebrow tag 3]

[Category label]

# Meet [Product Name]

[Tagline: one-sentence outcome. Bold the key phrase.]

[Description: 2 to 4 sentences explaining what the product does. Bold 1 to 2 capability phrases. No fluff.]

**[Primary CTA]**   **[Secondary CTA]**
```

Rules:
- The hero must communicate the primary outcome in the first line (H1 or tagline).
- The reader must understand what the product does within 5 seconds of scanning the hero.
- Do not stack multiple concepts in the tagline. One outcome per tagline.
- Eyebrow tags must be concrete features, not slogans.
- Category label must match how buyers describe the space.
- H1 must include the primary keyword or product name.
- No adjectives like powerful, robust, seamless, cutting-edge, or transformative.

### 2. Testimonial

```
> "[Direct quote with a concrete outcome. Must include a specific metric or named capability.]"
>
> **[Name]**, [Title], [Company]
```

Rules:
- Use only a testimonial the user provided.
- The quote must name a specific number, outcome, or capability.
- If no testimonial is available, skip this section and list "Missing testimonial" in Flags.

### 3. Performance Impact

```
## Performance Impact

| **[Number 1]** | **[Number 2]** | **[Number 3]** | **[Number 4]** |
| :---: | :---: | :---: | :---: |
| [Short label 1] | [Short label 2] | [Short label 3] | [Short label 4] |

[One sentence explaining what these numbers translate to in practice.]
```

Rules:
- Exactly 4 stat cells.
- Numbers must come from the user. Do not invent.
- The transition sentence must describe a concrete workflow change, not a slogan.

### 4. What Is [Product]?

```
## What Is [Product Name]?

[Screenshot: concrete description of the UI the screenshot should show.]

[Paragraph 1: entity-first definition. One to two sentences.]

[Paragraph 2: how it works. Mechanism-first. One to two sentences. Bold 1 to 2 capability phrases.]

[Paragraph 3: how it fits into the user's existing workflow. One to two sentences.]

[Paragraph 4: closing statement about speed, control, or scope. One sentence.]

**[CTA]**
```

Rules:
- Definition-first, no storytelling hook.
- Bold only concrete capability phrases.
- No "in today's landscape" or similar transitions.

### 5. What [Product] Makes Possible

```
## What [Product] Makes Possible

- **[Capability 1]**  
[One sentence: what the user does. Mechanism-first.]

- **[Capability 2]**  
[One sentence.]

[6 to 8 items total]
```

Rules:
- Each bullet names a concrete user action.
- Avoid benefit-only statements; name the mechanism or the output.

### 6. Getting Started with [Product]

```
## Getting Started with [Product Name]

[One sentence describing what happens after connection or installation.]

**[CTA]**

### Step 1: [Action]
[One sentence, under 25 words.]

### Step 2: [Action]
[One sentence.]

### Step 3: [Action]
[One sentence.]

### Step 4: [Action]
[One sentence.]

### Step 5: [Action]
[One sentence.]
```

Rules:
- Exactly 5 steps.
- Each step names a concrete user action.
- No step is longer than one sentence.

### 7. Feature Cards

Produce 5 to 9 feature cards. Each card uses this format:

```
### Card [N]

[Screenshot: concrete description of the UI, chart, or flow the screenshot should show.]

**[Card headline: concrete capability, not a slogan.]**

[2 to 3 sentence description. State what it does, how it works, and why it matters, in that order. Bold 1 to 2 key phrases.]

**[CTA matched to the action, not "Learn more"]**
```

Rules:
- Each card must represent a distinct capability.
- Do not repeat mechanisms across cards.
- If two cards overlap, merge them into one or sharpen the difference until each has a clear, separate job.
- Each card headline is a capability statement, not a benefit.
- Each card has a unique CTA ("Run Campaign Audit", "Launch My Campaign", etc.).
- Screenshots must be described specifically enough for a designer to pick the right UI.

### 8. Comparison: Why [Product] Outperforms [Category]

```
## Why [Product] Outperforms Traditional [Category] Tools

[One opening sentence summarizing the core difference between [Product] and the category.]

| Feature | [Product] | [Competitor 1] | [Competitor 2] | [Competitor 3] | [Competitor 4] |
| --- | --- | --- | --- | --- | --- |
| [Capability 1] | ✅ [Short description] | ❌ [Short description] | ⚠️ [Short description] | ⚠️ [Short description] | ❌ [Short description] |
| [Capability 2] | ✅ ... | ... | ... | ... | ... |

[8 to 12 rows total]
```

Rules:
- Use ✅ for full support, ⚠️ for partial, ❌ for not supported.
- Every cell must include a short descriptor next to the icon, not just the icon.
- Competitors must be real and in the same category.
- Before filling a competitor cell, search the web to confirm whether that competitor supports the capability.
- Do not invent competitor capabilities. If the web check cannot confirm a capability, use a neutral descriptor such as "Limited", "Manual", or "Not documented" next to the icon. Do not output the word "Verify".

### 9. Frequently Asked Questions

```
## Frequently Asked Questions

### General
- **What is [Product]?**  
[1 to 3 sentence answer.]
- **What does [Product] actually do?**  
[Answer.]
- **How does [Product] work?**  
[Answer.]
- **How is [Product] different from [category] tools?**  
[Answer.]
- **Is [Product] a replacement for [upstream platform]?**  
[Answer.]
- **Who is [Product] built for?**  
[Answer.]

### Capabilities
[5 to 7 capability questions]

### Integration & Scale
[3 to 4 integration questions]

### [Feature-specific group, e.g., PPC Retargeting, AI Visibility, Local SEO]
[3 to 4 feature-specific questions]

### Pricing & Trust
[4 to 5 pricing and trust questions, including: is it included in all plans, data security, free trial availability]
```

Rules:
- Group FAQs by category. No flat FAQ lists.
- Each answer is 1 to 3 sentences.
- Answers must name a specific mechanism or fact, not a generic claim.
- Do not duplicate earlier headings verbatim as FAQ questions.

## Global rules

- No em dashes. Use commas, colons, parentheses, or separate sentences.
- No fluff or repetition.
- No clichés: powerful, robust, seamless, cutting-edge, transformative, game-changing, unlock, elevate, in today's landscape.
- No AI-style vocabulary: ensure, leverage, crucial, delve.
- No invented testimonials, stats, pricing, or competitor capabilities.
- No fake social proof.
- No meta or process language. The output is the finished page, not an analysis.
- Every section must help the reader decide whether to buy.
- Follow mechanism, capability, outcome, in that order, when describing features.
- Screenshots are always placeholders in the format `[Screenshot: concrete description]`.

## Flags

At the very top of the output, before the hero, list any missing inputs under a `Flags:` heading:

- Missing testimonial
- Missing performance stats
- Missing screenshots (number of cards affected)
- Missing pricing

If no flags apply, omit the block.

## Output format

- Clean markdown.
- Follow the section order above exactly.
- No commentary outside the page itself.
- No explanation of reasoning.
