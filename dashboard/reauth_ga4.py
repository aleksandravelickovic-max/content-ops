#!/usr/bin/env python3
"""
reauth_ga4.py — mint a fresh GA4 OAuth token for the dashboard generator.

Opens your browser, you approve Google Analytics (read-only) access, and this
writes a new ~/.ga4-mcp/oauth-token.json with a fresh refresh_token.

Reuses the same OAuth client as reauth_gsc.py (~/.config/gsc/client_secrets.json)
with an additional GA4 scope — sign in with whichever Google account has Viewer
access on the GA4 property (e.g. marketing@searchatlas.com).

Run:  python3 dashboard/reauth_ga4.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

TOKEN_FILE   = Path.home() / ".ga4-mcp" / "oauth-token.json"
SECRETS_FILE = Path.home() / ".config"  / "gsc" / "client_secrets.json"
SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
]


def main():
    if not SECRETS_FILE.exists():
        raise SystemExit(f"Missing client secrets: {SECRETS_FILE}")

    flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS_FILE), SCOPES)
    # prompt=consent forces Google to return a NEW refresh_token.
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    expiry_ms = int(creds.expiry.replace(tzinfo=timezone.utc).timestamp() * 1000) \
        if creds.expiry else int(datetime.now(timezone.utc).timestamp() * 1000) + 3600_000

    token = {
        "access_token":  creds.token,
        "refresh_token": creds.refresh_token,
        "scope":         " ".join(creds.scopes or SCOPES),
        "token_type":    "Bearer",
        "expiry_date":   expiry_ms,
    }
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(token, indent=2))
    print(f"\n✓ Wrote fresh token to {TOKEN_FILE}")
    print(f"  refresh_token present: {bool(creds.refresh_token)}")
    print("\nIf this fails with 'access_denied' or an API-not-enabled error, the GA4 Data API")
    print("needs enabling on the same GCP project as the GSC OAuth client, and the signed-in")
    print("Google account needs Viewer access on the GA4 property.")


if __name__ == "__main__":
    main()
