# claude-config

Shared Claude Code customizations for the team. Push your agents, slash commands, skills, and settings snippets here so the rest of the team can use them.

## Structure

```
claude-config/
├── agents/      # Custom subagents (.md files with frontmatter)
├── commands/    # Custom slash commands (.md files)
├── skills/      # Skills (folders containing SKILL.md)
└── settings/    # Example settings.json snippets, hooks, permissions
```

Each subdirectory has its own README with the file format, naming convention, and install steps.

## How to use something from this folder

Claude Code looks for customizations in two places:

- `~/.claude/` — personal, applies everywhere
- `<repo>/.claude/` — project-scoped, applies only in that repo

To use a shared element, copy or symlink it into one of those locations.

### Example: install a shared agent personally

```bash
cp claude-config/agents/<name>.md ~/.claude/agents/
```

### Example: install a shared command for this project only

```bash
cp claude-config/commands/<name>.md .claude/commands/
```

Symlink instead of copy if you want updates from `git pull` to flow through automatically:

```bash
ln -s "$(pwd)/claude-config/agents/<name>.md" ~/.claude/agents/<name>.md
```

## How to contribute

1. Build and test the agent / command / skill locally in your own `.claude/` folder.
2. Once it works, copy the file into the matching `claude-config/` subdir.
3. Open a PR. Include a one-line description in the file's frontmatter (`description:` field) so teammates know what it does without opening it.
4. Update the subdir README if you added a new pattern other people should follow.

## Conventions

- Use kebab-case filenames: `seo-auditor.md`, not `SEO_Auditor.md`.
- Every agent and command needs a `description` in its frontmatter.
- Don't commit secrets, API keys, or workspace-specific paths. Use placeholders.
- Project-specific customizations (e.g. tied to one client's knowledge base) should live in that project's `.claude/`, not here. This folder is for things multiple teammates can reuse.
