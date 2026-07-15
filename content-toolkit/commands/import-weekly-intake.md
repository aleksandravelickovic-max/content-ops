---
description: Import a weekly topic and keyword CSV into per-client monthly deliverable registries.
argument-hint: "content-production/weekly-intake/YYYY-MM-DD/topics.csv [--month YYYY-MM]"
---

Import weekly LinkGraph topics and keywords.

Run:

```bash
python3 scripts/import-weekly-intake.py $ARGUMENTS
```

## CSV columns

Required:

- `client`
- `topic`
- `primary_keyword`

Recommended:

- `month`
- `type`
- `secondary_keywords`
- `notes`
- `priority`
- `due_date`
- `status`

If `month` is not in the CSV, pass it as:

```bash
python3 scripts/import-weekly-intake.py content-production/weekly-intake/2026-07-20/topics.csv --month 2026-07
```

## What it creates

For each client/month:

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

Each row gets a deliverable ID, registry entry, and brief stub linked to:

- `STYLE-SYSTEM.md`
- `raw/knowledge/service-taxonomy.md`
- `client-intelligence/offerings.md`
- `raw/research/website-intelligence.md`

## After importing

Refresh dashboards:

```bash
python3 scripts/build-delivery-dashboard.py
python3 scripts/build-client-context-dashboard.py
```

