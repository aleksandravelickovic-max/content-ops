# Shared skills

Skills the team can invoke via the `Skill` tool or by typing `/<skill-name>`.

## File format

Each skill is a folder containing a `SKILL.md` file. The folder name becomes the skill name.

```
skills/
└── my-skill/
    └── SKILL.md
```

`SKILL.md` frontmatter:

```markdown
---
name: my-skill
description: One-line description. Used by Claude to decide when to activate the skill.
---

# Instructions for the skill

What it does, when to use it, and what output it produces.
```

A skill folder can also contain supporting files (templates, prompts, scripts) referenced from `SKILL.md`.

## Install

Personal:

```bash
cp -r claude-config/skills/<name> ~/.claude/skills/
```

Project-only:

```bash
cp -r claude-config/skills/<name> .claude/skills/
```

## Naming

Use kebab-case folder names. The name in the frontmatter must match the folder name.
