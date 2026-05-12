# Codebase Map: zia-content-ops

> Auto-generated: 2026-05-12 14:15 | Commit: eac578ac | Branch: main
> 46 files | 2 code files | 6 functions/classes indexed

## Git Info
- Remote: https://forge.internal.searchatlas.com/search-atlas-group/content-team/content-ops.git
- Last commit: eac578a refactor: rename .claude/ to content-toolkit/ with symlink, remove dead claude-config/

## File Distribution
- `.md`: 23 files
- `.html`: 14 files
- `.json`: 2 files
- `.tag`: 1 files
- `.py`: 1 files
- `.js`: 1 files
- `.css`: 1 files

## Directory Structure
```
clients/
  searchatlas/
  zia-tile/
    reference-site/
content-toolkit/
  agents/
  commands/
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
