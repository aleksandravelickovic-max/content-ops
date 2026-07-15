---
description: Create or refresh canonical per-client folders for client intelligence and deliverables.
argument-hint: ""
---

Create the canonical folder structure for every client.

Run:

```bash
python3 scripts/build-client-context-dashboard.py
python3 scripts/organize-client-folders.py
```

## Creates per client

```text
clients/{client}/client-intelligence/
  README.md
  STYLE-GUIDE.md
  offerings.md
  offerings.json
  source-files.md

clients/{client}/deliverables/
  README.md
  index.json
  drafts/
  final/
  html/
  review/
  shipped/
```

## Rule

This command does not move existing campaign files. It indexes them into `deliverables/index.json` so the new folders can become the default workspace without breaking older paths.
