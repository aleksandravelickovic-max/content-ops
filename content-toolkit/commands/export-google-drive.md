---
description: Build a Google Drive upload manifest and staging folder for monthly LinkGraph deliverables.
argument-hint: "--month YYYY-MM [--client client-slug]"
---

Build the Google Drive export queue.

Run:

```bash
python3 scripts/build-google-drive-export.py $ARGUMENTS
```

Example:

```bash
python3 scripts/build-google-drive-export.py --month 2026-07
```

## What it creates

```text
reports/google-drive-export/{YYYY-MM}/
  manifest.json
  upload-plan.md
  files/
```

The manifest is the upload queue for Google Drive. It includes:

- target Drive folder names
- client
- deliverable ID
- topic
- keyword
- status
- expected brief, draft, review, final, and upload receipt files
- staged local file paths where files exist

## Current limitation

This command does not call the Google Drive API yet. It prepares a Drive-ready upload queue. When a Drive connector, service account, or OAuth flow is available, the upload adapter should read `manifest.json` and write Drive URLs back to each monthly `registry.json`.

