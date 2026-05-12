# Codebase Map: zia-content-ops

> Auto-generated: 2026-05-12 13:23 | Commit: 3b0251e1 | Branch: main
> 30 files | 2 code files | 6 functions/classes indexed

## Git Info
- Remote: 
- Last commit: 3b0251e feat: initialize zia-content-ops from content-ops/zia

## File Distribution
- `.html`: 14 files
- `.md`: 12 files
- `.zip`: 1 files
- `.py`: 1 files
- `.js`: 1 files
- `.css`: 1 files

## Directory Structure
```
knowledge-site/
transcripts/
```

## Code Index (Functions & Classes)

### knowledge-site/_build.py
  def build_nav(active_slug: str)
  def build_index_body()
  def fix_internal_links(html_body: str, source_path: Path | None)
  def render_markdown(source: Path)
  def page_template(page: dict, body_html: str)
  def main()
