# LinkGraph Client Context Dashboard Project

Last updated: 2026-07-14
Owner: Aleksandra Velickovic
Repo: `/Users/aleksandravelickovic/content-ops`

This is the durable project record for the LinkGraph writer delivery system and client context dashboard work. Beads owns task status. This file explains what exists, where it lives, and how to continue without reconstructing the project from chat history.

## Goal

Build a LinkGraph-specific delivery system for writers working across 20+ clients. The system should give each client its own usable context page with:

- style rules and voice constraints
- services, products, goods, treatments, collections, or offering taxonomy
- sitemap and website intelligence
- source files from the client folder
- a dedicated place for deliverables
- enough client context that writers do not miss obvious service/product facts
- anti-slop guardrails, including no generic AI phrasing, no duplicated context, and no unsupported claims

The dashboard is not meant to be a marketing page. It is a writer-facing operating surface.

## Current Outputs

Generated dashboard:

- `reports/client-context-dashboard/index.html`
- `reports/client-context-dashboard/{client}.html`
- `reports/client-context-dashboard/data.json`

Delivery dashboard:

- `reports/linkgraph-delivery-dashboard.html`
- `reports/linkgraph-delivery-dashboard.json`

Client folders now use this structure:

- `clients/{client}/client-intelligence/`
- `clients/{client}/deliverables/`
- `clients/{client}/raw/knowledge/`
- `clients/{client}/raw/research/`

`SearchAtlas` is excluded from the client context dashboard. The dashboard is for LinkGraph client delivery, not internal SA content.

## Main Scripts

Build the client context dashboard:

```bash
python3 scripts/build-client-context-dashboard.py
```

Refresh client folder organization and generated client intelligence:

```bash
python3 scripts/organize-client-folders.py
```

Crawl client websites and refresh sitemap/page intelligence:

```bash
python3 scripts/crawl-client-websites.py
```

Build the delivery dashboard:

```bash
python3 scripts/build-delivery-dashboard.py
```

Local report server used during this project:

```bash
python3 -m http.server 8765 --directory reports
```

Dashboard URL pattern:

```text
http://127.0.0.1:8765/client-context-dashboard/index.html
http://127.0.0.1:8765/client-context-dashboard/5gstore.html
http://127.0.0.1:8765/client-context-dashboard/a-plus-landscaping.html
```

## Knowledge Base Placement

Project-level memory lives here:

- `memory/linkgraph-client-context-dashboard.md`

Command docs live here:

- `content-toolkit/commands/build-client-context-dashboard.md`
- `content-toolkit/commands/refresh-delivery-dashboard.md`
- `content-toolkit/commands/crawl-client-websites.md`
- `content-toolkit/commands/organize-client-folders.md`

Client-specific knowledge lives inside each client folder:

- `clients/{client}/raw/knowledge/`
- `clients/{client}/STYLE-SYSTEM.md`
- `clients/{client}/client-intelligence/`

Editable offering/service taxonomies should live in:

```text
clients/{client}/raw/knowledge/service-taxonomy.md
```

The dashboard generator also reads:

```text
clients/{client}/raw/knowledge/services.md
clients/{client}/raw/knowledge/offerings.md
clients/{client}/raw/knowledge/products/*.md
```

Generated files in `client-intelligence/` should not be treated as the only source of truth. They are useful writer-facing outputs, but edits should usually happen in `STYLE-SYSTEM.md` or `raw/knowledge/`.

## APlus Landscaping Fix

The dashboard initially missed APlus Landscaping's actual services and produced junk offerings such as page-structure instructions and crawl-noise titles.

Added:

- `clients/a-plus-landscaping/raw/knowledge/service-taxonomy.md`

That file captures the website navigation and homepage context supplied by Aleksandra, including:

- Outdoor Living Design
- Hardscaping
- Patios
- Paver Driveways
- Retaining Walls
- Steps & Pillars
- Permeable Pavers
- Stone Decks
- Concrete Overlays
- Decks & Structures
- Decks
- Pergolas
- Pavilions
- Gazebos
- Porches
- Louvered Pergolas
- Pools & Waterscapes
- Custom Pools
- Streams
- Ponds
- Water Feature
- Water Falls
- Spas
- Landscaping & Lighting
- Landscaping
- Planting
- Trees
- Landscape Lighting
- Hardscape Lighting
- Landscape Maintenance Packages
- Outdoor Features
- Outdoor Kitchens
- Firepits/Fireplaces
- Grills & Appliances
- Pizza Ovens
- Patio Furniture
- Snow

The generator now treats service taxonomy files as high-priority offering sources and blocks page-structure junk such as:

- `H2 FAQ`
- `Meta description`
- `CTA`
- `What we build`
- `Why A Plus`

Validation run:

```bash
python3 -m py_compile scripts/build-client-context-dashboard.py
python3 scripts/build-client-context-dashboard.py
python3 scripts/organize-client-folders.py
```

Result:

- 24 client dashboard pages built
- APlus generated 39 offerings with distinct descriptions
- 5Gstore stayed clean after the taxonomy/parser change

## All-Client Taxonomy Pass

Updated: 2026-07-14

The APlus taxonomy pattern was extended to every dashboard client except SearchAtlas, which remains excluded.

Added or verified editable taxonomy files at:

```text
clients/{client}/raw/knowledge/service-taxonomy.md
```

Coverage after the pass:

- 24 dashboard clients
- 24 service taxonomy files
- 0 missing taxonomy files

Altify required a manual correction because the crawler returned `0 product/service URLs` even though the live navigation clearly lists offerings. The taxonomy now includes:

- Altify Insights
- Altify Sales Process
- Altify Opportunities
- Altify Accounts
- Revenue Enablement Services
- MaxAI
- Relationship Map
- Insight Map
- TeamView
- Test and Improve
- Opportunity Map
- role-based solutions for CRO / Sales Leadership, CTO / IT, Sales Operations, Sales Enablement, and Sales Representative / Account Executive

Other clients were populated from the strongest available source per client:

- style-system product/service sections
- refreshed website intelligence
- local raw research and live-baseline files
- visible website navigation where supplied

Important caveat: ecommerce or catalog clients may need a later editorial decision on taxonomy depth. Current pass includes category-level offerings for 5Gstore and Zia Tile, and product-page-level entries for Loti Labs where the crawl returned high-confidence product pages. Confirm with Aleksandra before expanding every ecommerce client into full SKU coverage.

Validation run:

```bash
python3 scripts/crawl-client-websites.py --max-pages 18
python3 scripts/build-client-context-dashboard.py
python3 scripts/organize-client-folders.py
python3 -m py_compile scripts/build-client-context-dashboard.py scripts/crawl-client-websites.py scripts/organize-client-folders.py
```

Final offering-count scan:

```text
5gstore: 6
a-plus-landscaping: 39
altify: 19
anne-therese: 14
the-hope-house/arizonaiop: 11
axiom-hrs: 8
esthetics-center: 7
find-self-storage: 13
laser-center-of-marin: 5
liveops: 14
loti-labs: 38
makana-charters: 11
pekas-smith: 4
portugal-pathways: 10
print-and-cheques-now: 11
the-hope-house/scottsdaleazdetox: 12
the-hope-house/scottsdaletmstherapy: 4
the-hope-house/thehopehouse: 15
the-nash-casino: 11
thera: 12
trustlayer: 13
us-self-storage: 8
us-storage-units: 12
zia-tile: 20
```

Generator cleanup added during this pass:

- service taxonomy files are first-class offering sources
- page-template labels such as `H2`, `CTA`, `Meta description`, and `Program and service pages` are filtered out
- tour-inclusion sections such as lunch, soft drinks, and snorkel gear no longer become Makana offerings
- `service details`, `solution / feature pages`, and similar scaffolding headings are filtered out

Anti-slop scan across taxonomy files returned no hits for the standard banned phrase list.

## 5Gstore Fixes

The dashboard originally showed noisy top terms such as:

- latest
- warranty
- click
- submit
- question
- youtube
- posts

The generator now uses semantic/topical terms instead of raw crawl frequency terms. For 5Gstore, the cleaned terms include:

- Antennas
- Enterprise Routers
- Hardware Accessories
- Mobile Hotspots
- Signal Boosters
- Software Licenses / Cloud Services
- Cellular Connectivity
- Signal Strength
- Mobile Broadband
- SpeedFusion bonding

5Gstore offerings are currently kept to meaningful product/service categories rather than scraped support or warranty page noise.

## Dashboard Design Direction

The dashboard was rebuilt toward LinkGraph styling rather than a generic report. It should feel like an internal LinkGraph platform:

- centered content
- wide but constrained layout
- client pages instead of one giant page
- no sticky sidebar trapping content
- one page per client
- offering catalog as a core section
- website intelligence as supporting evidence
- full style system available lower on the page

The design is still not final. Aleksandra flagged that the structure and formatting need to make more sense across all dashboards, especially the way voice rules, avoid rules, terminology, and offering evidence are grouped.

## Delivery System Direction

Each client needs separate places for:

- style guide, services, products, and context
- deliverables

This has been added by folder organization:

```text
clients/{client}/client-intelligence/
clients/{client}/deliverables/
```

Campaign deliverables were migrated into client deliverable structures in earlier work. The repo still has a noisy git status with many deleted old campaign paths and many untracked generated folders, so do not commit broad repo state without a careful review.

## Monthly Production Pipeline

Updated: 2026-07-14

The next layer is a month-based production queue that starts from weekly topic and keyword intake and prepares files for Google Drive.

Weekly intake lives here:

```text
content-production/weekly-intake/
```

CSV template:

```text
content-production/weekly-intake/example-topics.csv
```

Import command:

```bash
python3 scripts/import-weekly-intake.py content-production/weekly-intake/YYYY-MM-DD/topics.csv
```

The importer creates:

```text
clients/{client}/deliverables/{YYYY-MM}/
  intake/
  briefs/
  drafts/
  reviews/
  final/
  platform-uploads/
  registry.json
```

Each `registry.json` tracks the monthly queue for that client:

- deliverable ID
- topic
- primary keyword
- secondary keywords
- type
- status
- priority
- due date
- production paths
- Google Drive upload status
- Google Drive file/folder URLs once available

Brief stubs link back to:

- `STYLE-SYSTEM.md`
- `raw/knowledge/service-taxonomy.md`
- `client-intelligence/offerings.md`
- `raw/research/website-intelligence.md`

Google Drive is the first upload target. Current implementation is manifest-first because this Codex session does not have a callable Google Drive upload connector.

Drive export command:

```bash
python3 scripts/build-google-drive-export.py --month YYYY-MM
```

Outputs:

```text
reports/google-drive-export/{YYYY-MM}/
  manifest.json
  upload-plan.md
  files/
```

The manifest is the upload queue for a future Google Drive API adapter. When Google Drive credentials or a connector are available, that adapter should:

1. Read `reports/google-drive-export/{YYYY-MM}/manifest.json`.
2. Create or find the Drive folders named in `drive_folder_name`.
3. Upload staged files.
4. Write Drive URLs back into each client monthly `registry.json`.
5. Rebuild `scripts/build-delivery-dashboard.py` so dashboard status reflects upload state.

The delivery dashboard now reads monthly registries and includes monthly deliverable counts plus latest Google Drive upload state in the Work column.

Command docs:

- `content-toolkit/commands/import-weekly-intake.md`
- `content-toolkit/commands/export-google-drive.md`

## Important Beads

Closed during this project:

- `cops-ha5`: migrated campaign deliverables and cleaned offerings
- `cops-rie`: excluded SearchAtlas/SA from the client dashboard
- `cops-rty`: restyled dashboard for LinkGraph
- `cops-xpv`: fixed sidebar quick context structure
- `cops-whc`: reworked all client dashboard page structure
- `cops-zmy`: replaced crawl-noise top terms with semantic topics
- `cops-o6q`: added editable service taxonomy ingestion and populated APlus Landscaping taxonomy

Current checkpoint bead:

- `cops-4me`: save the whole project in the content-ops knowledge base

## Current Repo State Warning

The repo has many unrelated untracked, modified, and deleted files from the broader dashboard/folder reorganization. Before committing, use targeted status and diff commands. Do not run broad destructive cleanup.

Useful targeted status command:

```bash
git status --short \
  scripts/build-client-context-dashboard.py \
  clients/a-plus-landscaping/raw/knowledge/service-taxonomy.md \
  clients/a-plus-landscaping/client-intelligence/offerings.md \
  reports/client-context-dashboard/a-plus-landscaping.html \
  reports/client-context-dashboard/data.json \
  memory/linkgraph-client-context-dashboard.md
```

## How To Continue

Start by running:

```bash
bd prime
bd ready
```

Then inspect:

```bash
memory/linkgraph-client-context-dashboard.md
content-toolkit/commands/build-client-context-dashboard.md
reports/client-context-dashboard/index.html
```

For any client with missing services/products, add or update:

```text
clients/{client}/raw/knowledge/service-taxonomy.md
```

Then regenerate:

```bash
python3 scripts/build-client-context-dashboard.py
python3 scripts/organize-client-folders.py
```

Check the relevant client HTML page before marking the bead closed.

## Open Product Questions For Aleksandra

The dashboard still needs decisions on:

- Whether services/products should be grouped by category on the page instead of rendered as a flat card grid.
- Whether each client page should show a short writer brief at the top before the full style system.
- Which fields belong in `dashboard/delivery-registry.json` versus each client's `client-intelligence/`.
- Whether deliverables should be linked from the client context pages, the delivery dashboard, or both.
- Whether every client needs a hand-curated `service-taxonomy.md`, or only clients whose website crawl/style system misses context.
