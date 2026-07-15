---
description: Crawl LinkGraph client websites, fetch sitemaps, and write editable product/service/context intelligence files.
argument-hint: "[--client client-slug] [--max-pages 14]"
---

Build or refresh website intelligence for LinkGraph clients.

Run:

```bash
python3 scripts/crawl-client-websites.py $ARGUMENTS
```

## What it writes

Per client:

- `clients/{client}/raw/research/website-intelligence.json`
- `clients/{client}/raw/research/website-intelligence.md`

Aggregate reports:

- `reports/client-website-intelligence.json`
- `reports/client-website-intelligence.html`

## What to edit

Edit the per-client Markdown files when a human adds context, corrections, exclusions, or notes.

If a website URL is missing, add it to the client's `STYLE-SYSTEM.md`, raw overview file, or `dashboard/delivery-registry.json` under `website_urls`, then rerun.

## After running

Report:

- number of clients crawled
- clients with usable sitemaps
- clients missing website URLs
- clients where only homepage sampling worked
