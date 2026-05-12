# Shared slash commands

Custom `/commands` the team can invoke from any Claude Code session.

## File format

One `.md` file per command, kebab-case name. The filename becomes the slash command: `brief.md` → `/brief`.

```markdown
---
description: One-line description of what this command does. Shown in the slash command picker.
---

Instructions for Claude when the command is invoked.

Use $ARGUMENTS to reference arguments the user passes after the command name.
```

## Install

Personal:

```bash
cp claude-config/commands/<name>.md ~/.claude/commands/
```

Project-only:

```bash
cp claude-config/commands/<name>.md .claude/commands/
```

## Naming

Use verbs or short nouns: `brief`, `draft`, `ship`, `humanize`. Avoid prefixes like `do-` or `run-`.

## What goes here

Commands that bake in a workflow the whole team runs the same way — content briefs, drafting flows, QA checks. Personal shortcuts stay in your own `~/.claude/commands/`.
