---
description: Build the multi-page LinkGraph client context dashboard, with one HTML page per client.
argument-hint: ""
---

Build the writer-facing client context dashboard.

Before changing the dashboard system, read:

```text
memory/linkgraph-client-context-dashboard.md
```

Run:

```bash
python3 scripts/build-client-context-dashboard.py
```

## Output

- `reports/client-context-dashboard/index.html`
- `reports/client-context-dashboard/{client}.html`
- `reports/client-context-dashboard/data.json`

## What it includes

Each client page includes:

- writer quick context
- extracted offerings, services, goods, treatments, collections, or product categories
- sitemap and sampled page intelligence
- product/service URLs from the crawl
- full style-system sections
- local source files read from the client folder

## Editable client knowledge

Client-specific service, product, and offering knowledge belongs in:

```text
clients/{client}/raw/knowledge/
```

For curated service taxonomies, use:

```text
clients/{client}/raw/knowledge/service-taxonomy.md
```

The generated `client-intelligence/` files are writer-facing outputs. Do not treat them as the only source of truth.

Refresh website crawl data first when URLs, services, products, or sitemaps may have changed:

```bash
python3 scripts/crawl-client-websites.py
```
