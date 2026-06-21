---
description: Weekly LLM visibility report for Search Atlas. Pulls brand overview, competitor share of voice, query performance, sentiment, and citations from the SA LLMV platform. Posts to a ClickUp channel and logs to Obsidian.
argument-hint: [clickup-channel-id]
---

Run a weekly LLM visibility report for searchatlas.com. Execute all steps in order.

## Arguments

$ARGUMENTS

If a ClickUp channel ID is provided, post the formatted report there. If no argument is given, output the report and ask Aleksandra where to send it.

## Step 1 — Pull LLMV data (run all five in parallel)

Use these MCP tools simultaneously:

1. `mcp__searchatlas__llmv_get_brand_overview` — domain: `searchatlas.com`, period: `30d`
2. `mcp__searchatlas__llmv_get_competitor_share_of_voice` — domain: `searchatlas.com`, period: `30d`, sort_by: `-share_of_voice`, page_size: 10
3. `mcp__searchatlas__llmv_get_queries_overview` — domain: `searchatlas.com`, period: `30d`, sort_by: `-visibility_score`
4. `mcp__searchatlas__llmv_get_sentiment_overview` — domain: `searchatlas.com`, period: `30d`, sort_by: `-mentions`
5. `mcp__searchatlas__llmv_get_citations_overview` — domain: `searchatlas.com`, period: `30d`, sort_by: `-mentions`, page_size: 10

## Step 2 — Build the report

Format the report exactly as shown below. Use real numbers from the data only — do not invent, round, or estimate.

For direction arrows on visibility score and sentiment: use ↑ if current > previous, ↓ if current < previous, → if unchanged.
For platform visibility, express as percentage (e.g. 80% = 4/5 topics).

---

```
🤖 Search Atlas — Weekly LLM Visibility Report
[Today's date]

━━━━━━━━━━━━━━━━━━━━━━━━
VISIBILITY SCORE (30-day)
━━━━━━━━━━━━━━━━━━━━━━━━
Overall: [score]/100 [→ direction vs prior]
Sentiment: [score]/100 [→ direction vs prior]
Mentions: [n] across 6 platforms

By platform:
- Google AI Mode:  [n]%  |  Sentiment: [n]%
- Grok:            [n]%  |  Sentiment: [n]%
- ChatGPT:         [n]%  |  Sentiment: [n]%
- Gemini:          [n]%  |  Sentiment: [n]%
- Copilot:         [n]%  |  Sentiment: [n]%
- Perplexity:      [n]%  |  Sentiment: [n]%

━━━━━━━━━━━━━━━━━━━━━━━━
SHARE OF VOICE (vs [total] competitors)
━━━━━━━━━━━━━━━━━━━━━━━━
#1  searchatlas.com (You)   [n]%
#2  [domain]                [n]%
#3  [domain]                [n]%
#4  [domain]                [n]%
#5  [domain]                [n]%

━━━━━━━━━━━━━━━━━━━━━━━━
QUERY PERFORMANCE (broad queries, sorted by visibility)
━━━━━━━━━━━━━━━━━━━━━━━━
Top 3:
- "[query]" — vis [n] | rank [n] | SoV [n]%
- "[query]" — vis [n] | rank [n] | SoV [n]%
- "[query]" — vis [n] | rank [n] | SoV [n]%

Needs attention:
- "[query]" — vis [n] | rank [n] | SoV [n]%
- "[query]" — vis [n] | rank [n] | SoV [n]%

━━━━━━━━━━━━━━━━━━━━━━━━
TOPIC SENTIMENT
━━━━━━━━━━━━━━━━━━━━━━━━
- [topic]: [n] mentions | [score]/100
- [topic]: [n] mentions | [score]/100
- [topic]: [n] mentions | [score]/100
- [topic]: [n] mentions | [score]/100
- [topic]: [n] mentions | [score]/100

━━━━━━━━━━━━━━━━━━━━━━━━
TOP CITED SOURCES (alongside SA)
━━━━━━━━━━━━━━━━━━━━━━━━
List top 5 non-SA domains cited in AI responses alongside SA:
- [domain]: [n] mentions | [n]% SoV
- [domain]: [n] mentions | [n]% SoV
- [domain]: [n] mentions | [n]% SoV
- [domain]: [n] mentions | [n]% SoV
- [domain]: [n] mentions | [n]% SoV

━━━━━━━━━━━━━━━━━━━━━━━━
ACTION THIS WEEK
━━━━━━━━━━━━━━━━━━━━━━━━
- Platform gap: [name the lowest-visibility platform and one specific fix]
- Query gap: [name the lowest-visibility query and one specific content action]
- SoV opportunity: [name the closest competitor to close the gap on]
```

---

## Step 3 — Post to ClickUp

If a channel ID was provided in the arguments, post the formatted report to that channel using `mcp__claude_ai_ClickUp__clickup_send_chat_message`.

Use the report text as the message body. No preamble or explanation — just the report.

## Step 4 — Log to Obsidian

Write the report to `~/Documents/Obsidian Vault/Daily Notes/[YYYY-MM-DD]-llm-visibility.md`.

Include:
- The full report
- A frontmatter block with: `date`, `client: searchatlas`, `type: llm-visibility-report`

## Constraints

- Numbers must come directly from LLMV tool output. Do not estimate or average.
- Direction arrows (↑ ↓ →) must reflect the actual previous vs current period comparison from the brand overview tool.
- List only non-SA domains in the "Top Cited Sources" section.
- Action items must be specific to the data — not generic SEO advice.
- Keep the report under 60 lines so it reads cleanly in ClickUp chat.
