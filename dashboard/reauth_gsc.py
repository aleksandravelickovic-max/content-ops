#!/usr/bin/env python3
"""
reauth_gsc.py — mint a fresh GSC OAuth token for the dashboard generator.

Opens your browser, you approve Google Search Console access, and this writes
a new ~/.gsc-mcp/oauth-token.json with a fresh refresh_token.

Run:  python3 dashboard/reauth_gsc.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

TOKEN_FILE   = Path.home() / ".gsc-mcp" / "oauth-token.json"
SECRETS_FILE = Path.home() / ".config"  / "gsc" / "client_secrets.json"
SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/webmasters.readonly",
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


if __name__ == "__main__":
    main()
