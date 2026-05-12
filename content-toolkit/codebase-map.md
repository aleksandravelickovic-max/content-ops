# Codebase Map: zia-content-ops

> Auto-generated: 2026-05-12 14:51 | Commit: 75967f1a | Branch: main
> 88 files | 19 code files | 99 functions/classes indexed

## Git Info
- Remote: https://forge.internal.searchatlas.com/search-atlas-group/content-team/content-ops.git
- Last commit: 75967f1 feat: add annotation portal, content navigator, and registry files

## File Distribution
- `.md`: 24 files
- `.html`: 17 files
- `.py`: 15 files
- `.json`: 4 files
- `.js`: 3 files
- `.css`: 3 files
- `.txt`: 3 files
- `.tag`: 2 files
- `.yml`: 2 files
- `.db`: 1 files
- `.sql`: 1 files

## Directory Structure
```
clients/
  searchatlas/
  zia-tile/
    reference-site/
content-toolkit/
  agents/
  commands/
portal/
  .ruff_cache/
    0.15.12/
    0.8.6/
  app/
    routes/
    static/
    templates/
reports/
ruff_cache/
  0.15.12/
  0.8.6/
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

### portal/app/content.py
  def get_campaign_path(client_slug: str, campaign_slug: str)
  def load_registry(client_slug: str, campaign_slug: str)
  def load_client_registry(client_slug: str)
  def get_content_html(client_slug: str, campaign_slug: str, content_path: str)
  def get_content_raw(client_slug: str, campaign_slug: str, content_path: str)
  def list_campaigns(client_slug: str)
  def list_clients()

### portal/app/database.py
  class Base
  def get_db()
  def init_db()

### portal/app/main.py
  def lifespan(app: FastAPI)
  def root()

### portal/app/models.py
  def utcnow()
  class ShareLink
  class Comment

### portal/app/routes/admin.py
  def admin_dashboard(request: Request, db: AsyncSession = Depends(get_db)
  def create_share_link
  def toggle_share_link
  def admin_comments
  def admin_resolve_comment

### portal/app/routes/api.py
  class CommentCreate
  class CommentResolve
  def create_comment
  def resolve_comment

### portal/app/routes/review.py
  def campaign_review
  def content_review

### portal/manage.py
  def init_db()
  def create_link(client: str, campaign: str, label: str | None = None)
  def list_links()
  def revoke_link(token_str: str)
  def list_comments(token_str: str | None = None)
  def main()

### scripts/annotation-api.py
  def lifespan(app: FastAPI)
  class AnnotationCreate
  class AnnotationUpdate
  class ReplyCreate
  def row_to_dict(row)
  def serve_navigator()
  def health()
  def list_annotations
  def create_annotation(body: AnnotationCreate)
  def update_annotation(ann_id: str, body: AnnotationUpdate)
  def delete_annotation(ann_id: str)
  def create_reply(ann_id: str, body: ReplyCreate)
  def annotation_stats()

### scripts/annotation-ui.js
  function checkApi()
  function apiFetch(path, opts)
  function loadAnnotations(docKey)
  function extractAnchor(range)
  function findTextInDom(container, exact, prefix, suffix)
  function textOffsetToRange(container, startOff, endOff)
  function renderHighlights()
  function clearHighlights()
  function showTooltip(rect)
  function hideTooltip()
  function showPopover(rect)
  function hidePopover()
  function renderSidebar()
  function scrollToSidebarCard(id)
  function escapeHtml(t)
  function formatTime(iso)
  function toggleMode()
  function onPreviewMouseUp(e)
  function hookNavigator()
  function init()

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

### scripts/build-html-before-after.py
  def parse_product_draft(path: Path)
  def build_collection_url_map()
  def discover_pages()
  def url_to_filename(url: str)
  def fetch_page(url: str, session: requests.Session)
  def fetch_all_originals(pages: list[dict])
  def extract_sections_from_product_draft(path: Path)
  def extract_sections_from_collection_draft(path: Path)
  def md_to_html(md_text: str)
  def apply_product_content(original_html: str, sections: dict, page_info: dict)
  def apply_collection_content(original_html: str, sections: dict, page_info: dict)
  def find_collection_for_product(product_slug: str, product_url: str)
  def build_revised_pages(pages: list[dict])
  def build_index_page(pages: list[dict])
  def main()

## CLAUDE.md Present
This repo has a CLAUDE.md with project-specific instructions.

## Config Files
docker-compose.yml
