# Shared settings snippets

Example `settings.json` blocks, permission rules, and hook configs. These are reference snippets, not full settings files — copy the parts you want into your own `~/.claude/settings.json` or `.claude/settings.json`.

## What lives here

- `permissions-*.json` — reusable permission rule sets (e.g. read-only Bash allowlists, MCP tool allowlists)
- `hooks-*.json` — hook configurations (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, etc.)
- `env-*.json` — environment variable blocks

Use kebab-case filenames that describe the snippet's purpose: `permissions-bq-readonly.json`, `hooks-format-on-save.json`.

## How to apply a snippet

1. Open the snippet and the target settings file (`~/.claude/settings.json` for personal, `.claude/settings.json` for project).
2. Merge the relevant block into the target file. Don't overwrite the whole file — merge the keys you want.
3. Restart Claude Code if you changed hooks or permissions.

## Don't commit

- API keys, tokens, or credentials
- Absolute paths tied to one person's machine
- Workspace IDs or account-specific identifiers

Use placeholders like `<YOUR_API_KEY>` or `${HOME}` and document them in a comment above the block.
