---
description: Weekly content health report for Search Atlas. Pulls decaying pages, recent traffic drops, and quick-win keywords from GSC. Posts to a ClickUp channel and logs to Obsidian.
argument-hint: [clickup-channel-id]
---

Run a weekly content health report for searchatlas.com. Execute all steps in order.

## Arguments

$ARGUMENTS

If a ClickUp channel ID is provided, post the formatted report there. If no argument is given, output the report and ask Aleksandra where to send it.

## Step 1 — Pull GSC data (run all three in parallel)

Use these MCP tools simultaneously:

1. `mcp__gsc__content_decay` — pages with consistent 3-period click decline
2. `mcp__gsc__traffic_drops` — pages that lost the most traffic in the last 28 days vs prior 28 days
3. `mcp__gsc__quick_wins` — keywords at positions 4–15 with high impressions

## Step 2 — Build the report

Format the report exactly as shown below. Use real numbers from the data only — do not invent, round, or estimate.

---

```
📉 Search Atlas — Weekly Content Health Report
[Today's date]

━━━━━━━━━━━━━━━━━━━━━━━━
DECAYING PAGES (3-period decline)
━━━━━━━━━━━━━━━━━━━━━━━━
List the top 5 by total click loss. For each:
- Page URL (shortened slug only, not full URL)
- Click loss: period3 → period2 → period1 (oldest to newest)
- Diagnosis: one of: Ranking drop | Demand decline | CTR collapse
- Suggested action: one line, specific and actionable

━━━━━━━━━━━━━━━━━━━━━━━━
RECENT TRAFFIC DROPS (last 28 days)
━━━━━━━━━━━━━━━━━━━━━━━━
List the top 5 pages by click loss vs prior period. For each:
- Page URL (slug only)
- Clicks: prior → current (with % change)
- Diagnosis from the tool

━━━━━━━━━━━━━━━━━━━━━━━━
QUICK WINS (position 4–15)
━━━━━━━━━━━━━━━━━━━━━━━━
List the top 5 keywords by impressions. For each:
- Keyword
- Current position
- Impressions
- Suggested action: one line (e.g. "Add FAQ targeting this query", "Strengthen H2", "Update intro to target this phrase")

━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━
- Total decaying pages found: [n]
- Total recent drops flagged: [n]
- Top quick win: [keyword] at position [n] with [n] impressions
- Priority action this week: [one sentence]
```

---

## Step 3 — Post to ClickUp

If a channel ID was provided in the arguments, post the formatted report to that channel using `mcp__claude_ai_ClickUp__clickup_send_chat_message`.

Use the report text as the message body. Do not add any preamble or explanation — just the report.

## Step 4 — Log to Obsidian

Write the report to `~/Documents/Obsidian Vault/Daily Notes/[YYYY-MM-DD]-content-health.md`.

Include:
- The full report
- A frontmatter block with: `date`, `client: searchatlas`, `type: content-health-report`

## Constraints

- Numbers must come directly from GSC tool output. Do not estimate or average.
- Slug format: strip `https://searchatlas.com` — show only the path (e.g. `/blog/keyword-research-api/`).
- Diagnoses must match the tool's own diagnosis field — do not override it.
- Suggested actions must be specific to the page/keyword, not generic SEO advice.
- Keep the report under 60 lines so it reads cleanly in ClickUp chat.
