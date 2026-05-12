# Codebase Map: zia-content-ops

> Auto-generated: 2026-05-12 14:29 | Commit: 04ff9159 | Branch: main
> 52 files | 3 code files | 19 functions/classes indexed

## Git Info
- Remote: https://forge.internal.searchatlas.com/search-atlas-group/content-team/content-ops.git
- Last commit: 04ff915 feat: add gdocs content exports and style audit report for Zia Tile campaign

## File Distribution
- `.md`: 23 files
- `.html`: 16 files
- `.json`: 4 files
- `.py`: 2 files
- `.tag`: 1 files
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
reports/
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

### scripts/build-content-navigator.py
  def human_size(n)
  def slug_to_display(slug)
  def detect_type(rel_path)
  def detect_category(rel_path, file_type)
  def extract_title(path)
  def read_content(path)
  def scan_directory(base_path, rel_root, allowed_exts=None)
  def generate_campaign_registry(client_name, campaign_path)
  def generate_client_registry(client_name, client_path)
  def generate_all_registries()
  def build_content_store(registries)
  def build_html(registries, content_store)
  def main()

## CLAUDE.md Present
This repo has a CLAUDE.md with project-specific instructions.
