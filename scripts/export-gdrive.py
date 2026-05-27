#!/usr/bin/env python3
"""
Upload a rendered HTML draft to Google Drive (converting it to a Google Doc)
and write the resulting link into the client's delivery tracker sheet.

Decision source: 2026-05-27 Lucas Automation Sync-Up.
- Alex Bellanger (CSM) shares Google Doc links with the Zia client for approval.
- Currently this is a manual upload + paste step.
- The CLI / API path is cheaper in tokens than asking an MCP to do the same.

This script uses `google-api-python-client` (already installed in this env).
The `gdrive` standalone CLI (glotlabs) is the other supported option — both
do the same thing; the Python path is preferred because it handles the
Sheets row write in the same authenticated session.

Usage:
    python3 scripts/export-gdrive.py <path-to-draft.html> --client <slug> [--campaign <slug>] [--dry-run]

    <path-to-draft.html>   Required. The rendered HTML (output of stage 12 / /render-html).
    --client <slug>        Required. e.g. zia-tile. Used to load clients/{slug}/delivery.yml.
    --campaign <slug>      Optional. Used to namespace the upload + the sheet row.
    --dry-run              Optional. Print the planned upload + sheet row without performing it.

Exit codes:
    0  success
    1  input error (missing file, missing config, etc.)
    2  dependency missing
    3  auth missing or invalid
    4  API error from Drive or Sheets

Setup (one-time per operator):
    1. In Google Cloud Console, create a project, enable Drive + Sheets APIs.
    2. Create OAuth client credentials (Desktop app), download as credentials.json.
    3. Place credentials.json at ~/.config/content-ops/credentials.json
       (or set CONTENT_OPS_GDRIVE_CREDENTIALS to its path).
    4. First invocation triggers the browser OAuth flow and caches token.json
       next to credentials.json.

Setup (one-time per client):
    Create clients/{client}/delivery.yml with:
        drive_folder_id: "<id of the Drive folder where Docs land>"
        sheet_id: "<id of the tracking sheet>"
        sheet_tab: "<tab name, e.g. 'Deliveries'>"
        columns:
          date: "A"           # ISO date the link was added
          piece: "B"          # slug or topic
          campaign: "C"
          gdoc_link: "D"
          source_html: "E"    # repo path for chain of custody
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError as e:
    print(f"Missing Google API dependency: {e}.", file=sys.stderr)
    print("Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
]
DEFAULT_CREDS_DIR = Path.home() / ".config" / "content-ops"


def load_delivery_config(client_slug: str) -> dict:
    config_path = REPO_ROOT / "clients" / client_slug / "delivery.yml"
    if not config_path.exists():
        print(f"error: missing delivery config at {config_path}", file=sys.stderr)
        print("       create it per the schema in scripts/export-gdrive.py docstring.", file=sys.stderr)
        sys.exit(1)
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_credentials_path() -> Path:
    env_override = os.environ.get("CONTENT_OPS_GDRIVE_CREDENTIALS")
    if env_override:
        return Path(env_override)
    return DEFAULT_CREDS_DIR / "credentials.json"


def get_credentials() -> Credentials:
    creds_path = get_credentials_path()
    token_path = creds_path.with_name("token.json")

    if not creds_path.exists():
        print(f"error: OAuth credentials not found at {creds_path}", file=sys.stderr)
        print("       see setup instructions in scripts/export-gdrive.py docstring.", file=sys.stderr)
        sys.exit(3)

    creds: Credentials | None = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
        creds = flow.run_local_server(port=0)

    assert creds is not None
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def upload_html_as_gdoc(drive_service, html_path: Path, folder_id: str, doc_name: str) -> dict:
    metadata = {
        "name": doc_name,
        "parents": [folder_id],
        "mimeType": "application/vnd.google-apps.document",
    }
    media = MediaFileUpload(str(html_path), mimetype="text/html", resumable=False)
    file = (
        drive_service.files()
        .create(body=metadata, media_body=media, fields="id, webViewLink, name")
        .execute()
    )
    return file


def append_to_sheet(sheets_service, sheet_id: str, sheet_tab: str, row_values: list[str]) -> None:
    range_a1 = f"'{sheet_tab}'!A:Z"
    body = {"values": [row_values]}
    sheets_service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_a1,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()


def build_row(columns: dict, values: dict) -> list[str]:
    """Place each value at the column letter declared in delivery.yml.

    Unconfigured columns are left blank. Order is determined by column letter.
    """
    by_letter = {}
    for key, letter in columns.items():
        if key in values:
            by_letter[letter.upper()] = values[key]

    if not by_letter:
        return []

    max_letter = max(by_letter.keys())
    width = ord(max_letter) - ord("A") + 1
    row: list[str] = ["" for _ in range(width)]
    for letter, value in by_letter.items():
        row[ord(letter) - ord("A")] = value
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload HTML draft to Google Drive (as a Doc) and log the link.")
    parser.add_argument("html_path", type=Path, help="Path to the rendered HTML draft.")
    parser.add_argument("--client", required=True, help="Client slug (e.g. zia-tile). Loads clients/{slug}/delivery.yml.")
    parser.add_argument("--campaign", default="", help="Campaign slug for namespacing.")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without performing upload or sheet write.")
    args = parser.parse_args()

    if not args.html_path.exists() or not args.html_path.is_file():
        print(f"error: input file does not exist: {args.html_path}", file=sys.stderr)
        return 1

    config = load_delivery_config(args.client)
    folder_id = config.get("drive_folder_id")
    sheet_id = config.get("sheet_id")
    sheet_tab = config.get("sheet_tab", "Deliveries")
    columns = config.get("columns", {})

    if not folder_id or not sheet_id:
        print(f"error: delivery.yml for {args.client} missing drive_folder_id or sheet_id.", file=sys.stderr)
        return 1

    doc_name = args.html_path.stem
    source_rel = args.html_path.relative_to(REPO_ROOT).as_posix() if args.html_path.is_absolute() else args.html_path.as_posix()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if args.dry_run:
        print("DRY RUN")
        print(f"  upload:   {args.html_path}")
        print(f"  -> folder: {folder_id}")
        print(f"  -> name:   {doc_name}")
        print(f"  sheet:    {sheet_id} tab='{sheet_tab}'")
        print(f"  row:      date={today} piece={doc_name} campaign={args.campaign} source={source_rel}")
        return 0

    try:
        creds = get_credentials()
        drive = build("drive", "v3", credentials=creds, cache_discovery=False)
        sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)

        uploaded = upload_html_as_gdoc(drive, args.html_path, folder_id, doc_name)
        link = uploaded.get("webViewLink", "")

        row_values = build_row(
            columns,
            {
                "date": today,
                "piece": doc_name,
                "campaign": args.campaign,
                "gdoc_link": link,
                "source_html": source_rel,
            },
        )
        if row_values:
            append_to_sheet(sheets, sheet_id, sheet_tab, row_values)

        print(link)
        return 0
    except HttpError as e:
        print(f"error: Google API error: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
