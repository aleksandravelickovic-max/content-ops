---
description: Upload a rendered HTML draft to Google Drive (as a Google Doc) and log the link in the client's tracker sheet.
argument-hint: <path-to-draft.html> --client <slug> [--campaign <slug>] [--dry-run]
model: haiku
---

Push a pipeline-produced HTML draft into the client delivery workflow. Uploads the HTML to a Drive folder converting it to a Google Doc (the format Alex Bellanger uses to share with the client for approval), then appends a row to the client's tracking sheet with the link, source path, and metadata.

This command is mechanical (no LLM judgment) and runs on **haiku** because it's a deterministic shell-out to `scripts/export-gdrive.py`. It does not modify the source HTML or the MD.

Decision source: 2026-05-27 Lucas Automation Sync-Up. The previous step (drag and drop MD into Google Drive UI) was manual per operator and produced inconsistent doc-name and folder placement. The CLI / API path was specifically called out as cheaper in tokens than asking an MCP to do the same.

## Input

`$ARGUMENTS`: `<path-to-draft.html> --client <slug> [--campaign <slug>] [--dry-run]`

- `path-to-draft.html` — required. The rendered HTML (output of stage 12 / `/render-html`).
- `--client <slug>` — required. e.g. `zia-tile`. Loads `clients/{slug}/delivery.yml`.
- `--campaign <slug>` — optional. Used to namespace the sheet row.
- `--dry-run` — optional. Print the planned upload + sheet row without performing it. Useful for verifying the config without hitting the API.

## What it does

1. Loads `clients/{client}/delivery.yml` for the folder + sheet IDs.
2. Authenticates against Google Drive + Sheets APIs using cached OAuth token (or runs the OAuth flow on first invocation).
3. Uploads the HTML file to the configured Drive folder with `mimeType: application/vnd.google-apps.document` so Drive converts it on the fly. Headings and structure survive because the source is HTML, not MD.
4. Appends a row to the configured Sheet tab with date, piece slug, campaign, the doc link, and the repo source path.
5. Prints the Google Doc link to stdout.

## Setup (one-time per operator)

1. In Google Cloud Console: create a project, enable the Drive and Sheets APIs.
2. Create OAuth client credentials (Desktop app type). Download as `credentials.json`.
3. Place it at `~/.config/content-ops/credentials.json` (or set `CONTENT_OPS_GDRIVE_CREDENTIALS` to its absolute path).
4. Install Python deps:
   ```
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pyyaml
   ```
5. First invocation triggers the browser OAuth flow once. `token.json` is cached next to `credentials.json` and reused.

## Setup (one-time per client)

Create `clients/{client}/delivery.yml`:

```yaml
drive_folder_id: "<Drive folder ID where Docs land>"
sheet_id: "<Tracking sheet ID>"
sheet_tab: "Deliveries"
columns:
  date: "A"
  piece: "B"
  campaign: "C"
  gdoc_link: "D"
  source_html: "E"
```

There's a `clients/zia-tile/delivery.yml.example` checked in as the schema reference. **Do not commit a populated `delivery.yml`** — the IDs are not secret per se but they live in Aleksandra's working Drive and tracker. Add `delivery.yml` to `.gitignore`.

## Example

```
/export-gdrive clients/zia-tile/campaigns/01-product-collection-pages/runs/collection-cotto-allende/draft.html --client zia-tile --campaign 01-product-collection-pages
```

Dry-run version (no API calls, prints the plan):

```
/export-gdrive clients/zia-tile/campaigns/01-product-collection-pages/runs/collection-cotto-allende/draft.html --client zia-tile --dry-run
```

## Integration with `/run-piece`

`/run-piece` does NOT call this automatically. The export step is operator-triggered because:
- It hits external APIs (rate limits, quota).
- It's irreversible by the pipeline (you'd have to delete the Doc + the sheet row manually).
- The same draft sometimes needs human review *before* hitting the CSM's tracker.

After `/run-piece` completes, decide per piece whether to push it through `/export-gdrive`. The `/batch-review` workflow remains the same — gate-pass + human review on the HTML preview, then explicit export.

## Constraints

- Do not invoke without `--dry-run` until the OAuth token is established and the client's `delivery.yml` is populated.
- Do not edit the HTML before uploading. If the HTML needs changes, fix the MD source, re-run `/render-html`, then re-upload (which creates a *new* Doc — Drive does not overwrite).
- If `scripts/export-gdrive.py` errors with exit code 2 (dependency missing) or 3 (auth missing), report the gap to the user and stop. Do not invent a link.
- Each upload creates a fresh Doc. There is no "update existing Doc" path here by design — published versions are immutable for the CSM's audit trail.
