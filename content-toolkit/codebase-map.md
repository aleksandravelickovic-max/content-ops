# Codebase Map: zia-content-ops

> Auto-generated: 2026-05-13 02:03 | Commit: ae98ec64 | Branch: main
> 96 files | 19 code files | 109 functions/classes indexed

## Git Info
- Remote: https://forge.internal.searchatlas.com/search-atlas-group/content-team/content-ops.git
- Last commit: ae98ec6 docs: rebuild Zia Tile content HTML and update portal with annotation support

## File Distribution
- `.md`: 26 files
- `.html`: 18 files
- `.py`: 16 files
- `.json`: 4 files
- `.js`: 3 files
- `.css`: 3 files
- `.tag`: 2 files
- `.txt`: 2 files
- `.db`: 1 files
- `.yml`: 1 files

## Directory Structure
```
clients/
  searchatlas/
  zia-tile/
    reference-site/
content-toolkit/
  agents/
  commands/
  worktrees/
    agent-a2caf43aff80c9696/
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
  def get_compare_pairs(registry: dict)
  def find_draft_for_html
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
  def _get_user_or_none(request: Request)
  def require_admin(request: Request)
  def admin_dashboard
  def create_share_link
  def toggle_share_link
  def admin_comments
  def admin_resolve_comment
  def _build_tabs(groups: dict[str, list])
  def admin_campaigns
  def admin_campaign_detail
  def admin_campaign_create_share_link
  def admin_raw_html
  def admin_compare_view
  def admin_content_detail

### portal/app/routes/api.py
  class CommentCreate
  class CommentResolve
  def create_comment
  def resolve_comment

### portal/app/routes/auth.py
  def is_oauth_configured()
  def _email_domain_allowed(email: str)
  def login_page(request: Request, error: str | None = None)
  def google_login(request: Request)
  def google_callback(request: Request)
  def logout(request: Request)

### portal/app/routes/review.py
  def campaign_review
  def raw_html
  def compare_view
  def content_review

### portal/app/static/annotation.js
  function findTextInDom(container, exact, prefix, suffix)
  function textOffsetToRange(container, startOff, endOff)
  function renderHighlights()
  function clearHighlights(container)
  function scrollToComment(id)
  function extractAnchor(range)
  function showPopover(rect, anchor)
  function hidePopover()
  function escapeHtml(str)
  function submitInlineComment(form)
  function onDocumentMouseUp(e)
  function onDocumentMouseDown(e)
  function addJumpLinks()
  function init()

### portal/manage.py
  def init_db()
  def create_link(client: str, campaign: str, label: str | None = None, re...)
  def list_links()
  def revoke_link(token_str: str)
  def list_comments(token_str: str | None = None)
  def main()

### scripts/build-content-navigator.py
  def human_size(n)
  def slug_to_display(slug)
  def detect_type(rel_path)
  def detect_category(rel_path, file_type)
  def extract_title(path)
  def read_content(path)
  def get_changed_files()
  def get_pre_patch_content(rel_path)
  def extract_url_from_content(path)
  def url_to_html_filename(url)
  def build_html_mapping()
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

### scripts/fetch-missing-originals.py
  def extract_ziatile_urls(campaign_file: Path)
  def url_to_filename(url: str)
  def find_missing(urls: list[str])
  def fetch_page(url: str, session: requests.Session)
  def main()

## CLAUDE.md Present
This repo has a CLAUDE.md with project-specific instructions.
