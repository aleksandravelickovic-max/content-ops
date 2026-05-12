# Codebase Map: zia-content-ops

> Auto-generated: 2026-05-12 14:07 | Commit: 65ef9d8e | Branch: main
> 51 files | 2 code files | 6 functions/classes indexed

## Git Info
- Remote: https://forge.internal.searchatlas.com/search-atlas-group/content-team/content-ops.git
- Last commit: 65ef9d8 refactor: rename to CLAUDE.md and universal-rules for clarity

## File Distribution
- `.md`: 28 files
- `.html`: 14 files
- `.json`: 2 files
- `.tag`: 1 files
- `.py`: 1 files
- `.js`: 1 files
- `.css`: 1 files

## Directory Structure
```
claude/
claude-config/
  agents/
  commands/
  settings/
  skills/
  agents/
  commands/
clients/
  searchatlas/
  zia-tile/
    reference-site/
ruff_cache/
  0.15.12/
scripts/
universal-rules/
```

## Code Index (Functions & Classes)

### clients/zia-tile/reference-site/_build.py
  def build_nav(active_slug: str)
  def build_index_body()
  def fix_internal_links(html_body: str, source_path: Path | None)
  def render_markdown(source: Path)
  def page_template(page: dict, body_html: str)
  def main()

## CLAUDE.md Present
This repo has a CLAUDE.md with project-specific instructions.
