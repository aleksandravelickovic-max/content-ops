# Shared agents

Custom subagents the team can spawn via the `Agent` tool.

## File format

One `.md` file per agent, kebab-case name. Frontmatter required:

```markdown
---
name: agent-name
description: One-line description of when to use this agent. Used by Claude to pick the right agent.
tools: Read, Grep, Edit  # optional — restricts which tools the agent can call
---

System prompt for the agent goes here. Describe the agent's role, behavior, constraints, and output format.
```

## Install

Personal (works in every repo):

```bash
cp claude-config/agents/<name>.md ~/.claude/agents/
```

Project-only:

```bash
cp claude-config/agents/<name>.md .claude/agents/
```

## Naming

Match the agent's function: `fact-checker`, `seo-auditor`, `humanizer`. Avoid generic names like `helper` or `writer-2`.

## What goes here vs. stays in your own .claude/

Push to `claude-config/agents/` when the agent is useful for more than one person on the team. Keep agent drafts and one-off experiments in your own `~/.claude/agents/` until they're stable.
