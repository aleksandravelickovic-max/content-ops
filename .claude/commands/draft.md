Generate a full article from a content brief, following `CLAUDE.md` rules exactly.

## Input

Accept one of:
- A topic or keyword
- A brief (preferred) — either pasted inline or referenced by path

If no brief is provided:
1. Run the `/brief` logic internally for the given topic.
2. Then generate the article from that brief.

Do not ask for clarification if the input is clearly a topic. Only ask if the input is ambiguous (e.g., a URL, a file path that doesn't exist, or a fragment that could be either a topic or a directive).

## Core requirements

### 1. Answer-first writing
- The first sentence of every section must directly answer the section heading.
- No introductions that set up what's coming.
- No "in this article," "this guide covers," "let's explore," or equivalent framing.
- Mirror the heading in the first sentence so the answer is extractable on its own.

### 2. Strict structure adherence
- Use the exact H2 and H3 hierarchy from the brief.
- Do not add, remove, reorder, or rename sections.
- Do not insert "Introduction," "Conclusion," "Summary," or "Key takeaways" unless the brief lists them.
- If the brief is missing something you think is important, flag it at the top of the output under `Flags:` and continue with the brief as given.

### 3. AEO and GEO optimization
Write so retrieval systems can extract answers cleanly and cite specific statements.

Include, where the brief supports it:
- **Definition blocks** — one-sentence, entity-first definitions for every core concept introduced.
- **Direct Q&A sentences** — where the brief's key questions map to a section, answer the question in a single, quotable sentence before elaborating.
- **Comparison statements** — when the brief specifies a comparison (e.g., X vs. Y), write a one-sentence contrast before any longer explanation.
- **Step-by-step lists** — for practical sections, use ordered steps with a concrete action per step.

### 4. No bloat
- No filler paragraphs.
- No repeated ideas across sections.
- No generic SEO padding (tips roundups, benefits lists, "why it matters" paragraphs) unless the brief requires them.
- Every paragraph must add information not present earlier in the article.

### 5. Specificity enforcement
When describing anything, follow this hierarchy from CLAUDE.md:
1. **Mechanism** — how it works.
2. **Capability** — what it does.
3. **Outcome** — what it produces.

Prefer mechanism over outcome when both are available. Replace vague claims (powerful, robust, seamless, transformative, comprehensive) with concrete mechanism, capability, or outcome. Do not generalize into claims that cannot be verified.

### 6. Factual integrity
Do not invent:
- Statistics, percentages, or growth figures.
- Tool names, product features, pricing, or capabilities.
- Case studies, client names, quotes, or testimonials.
- Sources, studies, or citations.

If a claim requires external validation and none is supplied:
- Replace it with a verifiable, qualitative statement, or
- Flag it at the top of the output under `Flags:` and omit the unverifiable part.

Do not present inference as fact. Label inference explicitly when used.

### 7. Practicality
The practical H2 from the brief must be:
- Step-based (ordered list).
- Actionable (each step names a specific task the reader performs).
- Specific (names tools, inputs, cadence, or outputs where the brief supports it).

No conceptual filler inside the practical section.

### 8. Length control
- Keep sections tight. Stop when the answer is complete.
- Do not expand to sound comprehensive.
- Paragraphs: 1–4 lines. One idea per sentence.
- Do not pad short sections with examples, analogies, or restatements.

### 9. Brief anchoring
- Each section must stay within the scope defined by the brief.
- Do not introduce concepts, frameworks, or terminology that are not implied by the brief.
- If a section requires information not present in the brief, flag it under `Flags:` instead of expanding beyond scope.
- Define each core concept once. Do not repeat or rephrase definitions in later sections.
- Each section must flow logically from the previous one without restating prior content.
- Do not recap earlier sections.
- H1 must match the topic or primary query exactly, unless the brief specifies a different title.

### 10. Formatting requirements
- All H2 and H3 sections must be written as explicit markdown headings (`##` and `###`).
- Every core concept introduced in a section must start with a one-sentence definition before explanation.
- Each paragraph must answer one specific question or explain one mechanism only.
- All comparisons must be formatted as markdown tables when multiple attributes are compared.
- Flags must be concise and only include actionable constraints or missing inputs.

### 11. Question-based heading optimization (PAA / AEO)

Convert H2 or H3 headings into question form only when:
- The section answers a direct user query.
- The phrasing matches real search or prompt patterns.
- The question improves extractability.

Do NOT convert headings into questions when:
- The section is conceptual or structural (e.g., comparisons, frameworks, workflows).
- The question form becomes unnatural or vague.
- It reduces clarity.

Prioritize question-form headings for:
- Definitions (What is X?)
- Comparisons (What is the difference between X and Y?)
- Processes (How does X work?)
- Actions (How to do X?)

Leave headings in statement form when:
- They organize multi-part systems (e.g., "AI SEO tools by function").
- They introduce grouped concepts.
- They support scanning better as labels.

When a heading is in question form:
- The first sentence must answer it directly, in one sentence.
- The answer must be extractable on its own (snippet-ready).

Brief alignment:
- Question-form headings must still follow the structure defined in the brief. Do not change section meaning when converting.
- Prefer converting headings into question form when the mapped query in the brief is already a question.

FAQ section:
- Include a final H2 FAQ section only if it exists in the brief.
- Questions must not duplicate earlier headings exactly.
- Answers must be one to three sentences maximum.

### 12. Intro block (controlled)

- Include a short intro block below the H1 before the first H2.
- Length: 2–4 sentences maximum.
- First sentence must define the topic clearly (entity-first).
- Remaining sentences may:
  - Clarify scope.
  - Distinguish from adjacent concepts.
  - State what the reader will learn (without "this article will…" phrasing).

Do NOT:
- Use storytelling.
- Use rhetorical hooks.
- Use filler phrases.
- Delay the definition.

The intro must be extractable as a standalone definition block.

This intro block is unlabeled (no heading) and does not count as an "Introduction" section for the purposes of section 2.

### 13. Listicle expansion rules (for "best", "tools", "examples" topics)

When the article is a listicle or grouped-tool format:

Each item (tool, category, or example) must include:
- What it is (one sentence).
- How it works (mechanism).
- When to use it (specific use case).
- Limitation or tradeoff (to avoid generic praise).

Do NOT:
- List items without explanation.
- Repeat the same structure with shallow variations.
- Use vendor-style descriptions.

Depth rule:
- Each item must justify its inclusion.
- If an item cannot support 3–4 meaningful sentences, remove it.

Compression rule still applies:
- Keep each item tight.
- No marketing fluff.
- No generic "best for" language unless backed by explanation.

### 14. Editorial judgment (required for listicles)

Each section must include a clear recommendation signal:
- Who this tool is best for.
- When it is a better choice than alternatives.
- When it should NOT be chosen.

It is allowed to:
- Compare tools directly.
- Indicate stronger vs. weaker options.
- Highlight tradeoffs clearly.

Do NOT:
- Fabricate performance claims.
- Invent rankings or metrics.

Preference must be based on:
- Use case fit.
- Workflow alignment.
- Feature focus.

Avoid neutrality when a meaningful distinction exists.

### 15. Listicle depth (controlled expansion)

For each item, include exactly these 5 layers:

1. What it is (1 sentence).
2. How it works (mechanism, 1–2 sentences).
3. When to use it (specific use case).
4. When it is a better choice than alternatives (clear comparison).
5. When to avoid it (clear limitation or tradeoff).

Rules:
- Each layer must add new information.
- Do not repeat ideas across layers.
- Do not use generic praise (powerful, robust, leading).
- Do not reference vague sources ("users say", "many marketers").

Depth target:
- Each item must deliver a complete decision, not just a description.

Implication line (required):
- After the five-layer structure, add one short implication sentence.
- Explain why the tradeoff matters in practice.
- Connect the tool choice to a real decision or outcome.
- Each tool section should read as a recommendation, not a checklist.

### 16. Listicle intro (required for "best" topics)

After defining the topic, include:
- How tools are grouped.
- What criteria matter.
- What the reader should focus on when choosing.

Do NOT:
- Claim testing unless verified.
- Use hype language.

### 17. Remove internal process language

Do not include:
- References to "SERP analysis."
- "Reviewed sources."
- "Multi-source verification."
- "Based on sources."
- "Per source descriptions."
- Any description of how the content was created.

Translate uncertainty into:
- Guidance.
- Tradeoffs.
- Validation steps (e.g., "trial before buying", "verify current coverage").

Output must read as final content, not analysis. The reader should not be able to tell whether a brief, research pass, or SERP audit was involved in producing it.

This rule overrides any tendency to footnote the drafting process inside the article body. Flags at the top of the output may note missing inputs or unverifiable claims; the article itself may not.

### 18. Step and metric implications, punctuation

Implication sentences:
- After key steps or metrics, add one short implication sentence that explains what the result changes in practice.
- One sentence maximum. Place it immediately after the step or metric, not in a separate section.
- The implication must describe a concrete consequence for the reader's decision or workflow, not restate the step.

Punctuation:
- Do not use em dashes (`—`) in article body. Use commas, colons, parentheses, or separate sentences instead.
- This applies to prose, table cells, and bullets. Flags at the top of the output are exempt.

## Output format

- Clean markdown.
- H1 from the brief's topic (or derived directly from it).
- H2 and H3 structure exactly as specified in the brief.
- No intro fluff above the first H2.
- No conclusion unless the brief requires it.
- No meta commentary ("as covered above," "we saw earlier").
- If any flags are raised (missing input, unverifiable claim omitted, structural deviation), list them at the very top under a `Flags:` heading before the H1.

## Behavior constraints

- Do not default to blog-style writing.
- Do not sound like a generic SEO article.
- Do not restate the same idea with different wording.
- Do not over-explain concepts a reader of this brief already understands.
- Do not use AI-pattern vocabulary (ensure, leverage, crucial, optimize, delve, robust, seamless, unlock, elevate, transform, game-changing, it's not about X it's about Y).
- Do not open paragraphs with links.
- Do not use headings that end in `-ing` verbs.
- Do not write multi-paragraph introductions to sections.

## Editing pass (mandatory before returning output)

Before returning the article, do a self-edit pass:
1. Delete every sentence that does not add information.
2. Replace every vague claim with a concrete one, or remove it.
3. Confirm the first sentence of each section answers the heading.
4. Confirm no paragraph starts with a link.
5. Confirm no invented data remains.
6. Confirm heading structure matches the brief exactly.

Only return the article after this pass is complete.
