# Codebase Map: content-ops

> Auto-generated: 2026-06-16 | Commit: b536a4d | Branch: feat/sa-ai-cmo-batch-01
> 1,308 files total

## Git Info
- Remote: https://forge.internal.searchatlas.com/search-atlas-group/content-team/content-ops.git
- Last commit: b536a4d chore: regenerate registry files and content navigator
- Active branch: feat/sa-ai-cmo-batch-01

## File Distribution
- `.md`: 664 files
- `.html`: 341 files
- `.txt`: 167 files
- `.json`: 45 files
- `.py`: 32 files
- `.yml`: 23 files
- `.js`: 4 files
- `.css`: 4 files

## Active Clients (20)

| Client | Campaigns | Notes |
|---|---|---|
| searchatlas | 01-blog-content | AI CMO cluster, 11 finals |
| zia-tile | 01-product-collection-pages, 02-march-april-updates, 02-may-2026-blogs, 03-may-batch | Reference site included |
| altify | 01-may-content-optimization | Enterprise account planning AI |
| 5gstore | 01-may-content-optimization | 4G/5G networking equipment |
| a-plus-landscaping | — | Family-owned design-build, Central PA |
| anne-therese | — | Medical aesthetics, OH + FL |
| axiom-hrs | — | HCM/payroll, UKG partner |
| esthetics-center | 01-blog-content | Medical aesthetics + plastic surgery, Northern CA |
| laser-center-of-marin | — | Aesthetic clinic, Marin County CA |
| liveops | — | Cloud remote agent network for enterprise CX |
| loti-labs | — | Research peptides/capsules, RUO compliance |
| pekas-smith | — | AZ Social Security Disability law firm |
| portugal-pathways | — | HNW relocation advisory, British English |
| print-and-cheques-now | — | Canadian cheque printing, CPA #1010 |
| the-hope-house | — | 4 sub-brands: Hope House, AZ IOP, Scottsdale Detox, Scottsdale TMS |
| the-nash-casino | — | NH charitable gaming, Nashua NH |
| thera | — | VIP rehab clinic, Midtown Manhattan |
| trustlayer | — | AI-powered COI + third-party compliance |
| us-self-storage | — | Storage marketplace, 20,000+ facilities |
| us-storage-units | — | Storage marketplace, 10,000+ facilities |

## Directory Structure

```
clients/
  searchatlas/
    STYLE-SYSTEM.md
    delivery.yml                        # Drive folder IDs — DO NOT COMMIT credentials
    registry.json
    campaigns/
      01-blog-content/
        batches/
          ai-cmo-batch-01.csv
          production-log.md
        briefs/                         # 9 briefs
        drafts/                         # 20 drafts (v1 + v2 for each article)
          ai-cmo-for-marketing-agencies-v1.md / v2.md
          ai-cmo-for-startups-and-lean-teams-v1.md
          ai-cmo-for-startups-v2.md
          ai-cmo-kpis-v1.md
          ai-cmo-vs-fractional-cmo-v1.md / v2.md
          ai-cmo-vs-marketing-agency-v1.md / v2.md
          ai-marketing-automation-mistakes-v1.md / v2.md
          best-ai-cmo-tools-execution-depth-comparison-v1.md
          best-ai-cmo-tools-v2.md
          how-to-build-an-ai-marketing-stack-v1.md / v2.md
          how-to-measure-ai-marketing-performance-v1.md / v2.md
          what-is-google-ai-mode.md
          what-is-multiplayer-marketing-v1.md / .html
        final/                          # 11 articles — each has .md + .html
          ai-cmo-for-marketing-agencies
          ai-cmo-for-startups
          ai-cmo-for-startups-and-lean-teams   # stale — superseded by ai-cmo-for-startups
          ai-cmo-kpis
          ai-cmo-vs-fractional-cmo
          ai-cmo-vs-marketing-agency
          ai-marketing-automation-mistakes
          best-ai-cmo-tools
          best-ai-cmo-tools-execution-depth-comparison
          how-to-build-an-ai-marketing-stack
          how-to-measure-ai-marketing-performance
        sa-editorial-guidelines-dpr.md
        registry.json
    raw/
      knowledge/
        competitors/                    # 55 competitor files
        facts/                          # 26 fact files
        products/                       # 43 product files (incl. atlas-coworker.md)
        proof/                          # 7 study/proof files
        testimonials/                   # 21 testimonial files
  zia-tile/
    STYLE-SYSTEM.md
    COMPLIANCE.yml
    reference-site/
    materials/
    page-templates/
    _approved/
    campaigns/
      01-product-collection-pages/
      02-march-april-updates/
      02-may-2026-blogs/
      03-may-batch/
  {other 18 clients}/
    STYLE-SYSTEM.md
    campaigns/ (where applicable)
    raw/ (where applicable)

content-toolkit/                        # Symlinked as .claude/
  agents/                               # Writing, editing, QA, judge agents
  commands/                             # Slash commands
    auto-brief.md
    bulk-article-production.md
    content-decay-report.md
    llm-visibility-report.md
    render-html.md
    run-piece.md
    (+ others)
  skills/
    bulk-article-production/
      SKILL.md                          # Bulk production workflow
      scripts/
        qa_scan.py                      # QA gate: em dash, prohibited terms, FAQ, H1
        validate_batch.py               # CSV batch validation
      templates/
        article-brief-template.md       # Includes SERP research block + FAQ candidates
  contracts/                            # Keyway B1-B5 contracts
  PIPELINE.md
  IMPROVEMENT-LOOP.md
  codebase-map.md                       # This file
  settings-content-ops.json

portal/                                 # FastAPI content review portal
  app/
    main.py / config.py / database.py / models.py / content.py
    routes/ (admin, review, api, auth)
    static/ (styles.css, app.js, annotation.css, annotation.js)
    templates/ (base, admin, review)
  Dockerfile / docker-compose.yml
  manage.py

scripts/
  build-content-navigator.py            # Generates reports/content-navigator.html
  build-html-before-after.py
  render-html.py
  export-gdrive.py
  format-to-wp.py

reports/
  content-navigator.html                # Standalone content browser (21MB)
  searchatlas-pr-link-building-guide.html
  team-evidence-analysis-2026-06-02.html
  (+ audit reports)

universal-rules/
  UNIVERSAL-RULES.md
```

## SA Campaign: 01-blog-content — Article Status

| Slug | Final | HTML | Status |
|---|---|---|---|
| ai-cmo-for-marketing-agencies | ✓ | ✓ | QA passed |
| ai-cmo-for-startups | ✓ | ✓ | QA passed — systems architect model, 30-day setup |
| ai-cmo-kpis | ✓ | ✓ | QA passed — two-tier KPI framework |
| ai-cmo-vs-fractional-cmo | ✓ | ✓ | QA passed |
| ai-cmo-vs-marketing-agency | ✓ | ✓ | QA passed |
| ai-marketing-automation-mistakes | ✓ | ✓ | QA passed |
| best-ai-cmo-tools | ✓ | ✓ | QA passed — execution depth comparison |
| how-to-build-an-ai-marketing-stack | ✓ | ✓ | QA passed — Atlas Coworker + Multiplayer framing added |
| how-to-measure-ai-marketing-performance | ✓ | ✓ | QA passed |
| what-is-google-ai-mode | draft only | — | Not produced as final |
| what-is-multiplayer-marketing | draft only | ✓ | Not produced as final |
| ai-cmo-for-startups-and-lean-teams | stale | ✓ | Superseded by ai-cmo-for-startups — candidate for deletion |

## SA Knowledge Base

| Category | Count | Notable additions |
|---|---|---|
| products | 43 | atlas-coworker.md (June 2026) |
| competitors | 55 | — |
| facts | 26 | search-atlas-plan-details.md (pricing source of truth) |
| testimonials | 21 | — |
| proof | 7 | — |

## Code Index (Functions & Classes)

### content-toolkit/skills/bulk-article-production/scripts/qa_scan.py
  def scan(path: str)
  Gates: em dash | prohibited terms (14) | H1 in first 30 lines | FAQ section

### content-toolkit/skills/bulk-article-production/scripts/validate_batch.py
  def validate_csv(path: str)

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

### scripts/render-html.py
  Converts final .md drafts to semantic HTML delivery artifacts.

### portal/app/content.py
  def get_campaign_path(client_slug, campaign_slug)
  def load_registry(client_slug, campaign_slug)
  def load_client_registry(client_slug)
  def get_content_html(client_slug, campaign_slug, content_path)
  def list_campaigns(client_slug)
  def list_clients()

### portal/app/routes/admin.py
  def admin_dashboard
  def create_share_link
  def admin_comments
  def admin_campaigns
  def admin_campaign_detail

### portal/app/routes/review.py
  def campaign_review
  def content_review

### portal/manage.py
  def init_db()
  def create_link(client, campaign, label)
  def list_links()
  def revoke_link(token_str)
  def list_comments(token_str)

## CLAUDE.md Present
This repo has CLAUDE.md files at: / (global), /Users/aleksandravelickovic/ (personal), and content-ops/ (project).
