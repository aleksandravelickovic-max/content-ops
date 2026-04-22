---
description: Generate a content brief that reflects how a real SEO/content team thinks.
argument-hint: <topic or keyword>
---

Create a content brief for the topic or keyword below, following `CLAUDE.md` rules.

## Input
$ARGUMENTS

## Rules
- No fluff. No "comprehensive guide" phrasing. No templated SEO language.
- Every section must have a reason to exist. If a section cannot be filled with specific, defensible content, remove it.
- Flag unverifiable claims and missing inputs instead of inventing.
- When describing anything, follow the mechanism → capability → outcome hierarchy from CLAUDE.md.

## Process (required before writing the brief)
1. Use WebSearch to identify top-ranking pages for the query.
2. Select 3–5 representative results. Exclude ads and duplicate domains.
3. Use WebFetch to inspect those pages.
4. Extract from the fetched pages:
   - Common sections.
   - Repeated structures.
   - Weak or missing explanations.
5. Extract query patterns from the SERP:
   - Questions used in headings.
   - Definitions used in introductions.
   - Comparisons and "vs" patterns.
   - Step-based queries ("how to", "steps", "process").
6. Use these query patterns to:
   - Shape H2 and H3 structure.
   - Generate the Key questions section.
   - Identify answer surface opportunities.
7. Base the brief on that analysis.

Rules for the analysis:
- Ignore outliers. Focus on patterns that appear across multiple results.
- Do not invent SERP gaps. If no clear gap exists, state that directly in the Content angle section.
- Do not replicate SERP structure directly. Use patterns to inform decisions, not to copy outlines.
- Prioritize clarity, completeness, and logical flow over matching competitor structure.
- Merge redundant SERP sections into clearer, more efficient structure where possible.

## Output format

Produce the brief in clean markdown using exactly this structure. Do not add an intro, reasoning, or closing summary.

### 1. Definition-first angle
One-sentence, entity-first definition of the topic. Precise, not generic.

### 2. Search intent breakdown
What the user is actually trying to do when they search this. Describe the real job-to-be-done, not informational/commercial/transactional labels.

### 3. Content angle
How this article will differ from the patterns observed in top-ranking SERP results. Name the specific gap, contrarian take, or depth advantage — grounded in what the live SERP currently does or fails to do. If no clear differentiator exists, say so.

### 4. Proposed structure
H2 and H3 sections only.

H2 rules:
- Each H2 must reflect a real user query or search pattern.
- Phrase it in a way that could realistically appear in search or AI prompts.
- Avoid generic labels (e.g., Benefits, Importance, Overview).

H3 rules:
- Use H3s only when the H2 covers a multi-part concept that requires breakdown.
- Each H3 must represent a distinct sub-question, step, or component.
- Do not use H3s for filler or formatting.

Format:
- H2 title
  → mapped query
  - H3 (if needed)
    → mapped sub-query

No filler sections.

### 5. Key questions to answer
Specific, answerable queries aligned with AEO/GEO — the kind of questions users type into AI answer engines expecting a named source.

### 6. Entity coverage
Core entities (people, products, concepts, places, related terms) that must appear for topical completeness. One line each.

### 7. Practical section
One H2 dedicated to implementation, workflow, or tools. Name what the reader will actually do after reading.

### 8. Risks to avoid
What makes content on this topic generic, wrong, or low-value. Specific traps for this topic — not general writing advice.

### 9. Answer surface opportunities
Where this content can appear in AI answers or featured snippets.

Include:
- Definitions
- Direct question-answer pairs
- Comparison statements
- Step-by-step instructions
