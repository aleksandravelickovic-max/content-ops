---
description: Refresh the editable LinkGraph delivery dashboard from client folders, pipeline runs, and dashboard/delivery-registry.json.
argument-hint: "[--json-only]"
---

Refresh the LinkGraph delivery dashboard.

## What to do

Run:

```bash
python3 scripts/build-delivery-dashboard.py $ARGUMENTS
```

## Editable source

Team-owned fields live in:

```text
dashboard/delivery-registry.json
```

Edit that file for:

- owner
- writer
- CSM
- priority
- status
- blocker
- next action
- review URL
- delivery URL
- notes

Do not hand-edit generated reports.

## Generated outputs

- `reports/linkgraph-delivery-dashboard.html`
- `reports/linkgraph-delivery-dashboard.json`

## Monthly production queues

The dashboard also reads monthly deliverable registries created by:

```bash
python3 scripts/import-weekly-intake.py content-production/weekly-intake/YYYY-MM-DD/topics.csv
```

Monthly registries live at:

```text
clients/{client}/deliverables/{YYYY-MM}/registry.json
```

Google Drive export queues are built with:

```bash
python3 scripts/build-google-drive-export.py --month YYYY-MM
```

## After running

Report the dashboard path and the summary counts printed by the script.
