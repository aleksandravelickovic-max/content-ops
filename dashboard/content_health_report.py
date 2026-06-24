#!/usr/bin/env python3
"""
Weekly Content Health Report for searchatlas.com.

Replaces the cloud routine "SA Weekly Content Health Report", which broke when
Search Atlas's built-in GSC integration was disconnected. This script pulls GSC
data directly via the same OAuth token the dashboard uses (no Search Atlas
dependency) and posts the report to a ClickUp chat channel via the v3 REST API.

Data sources (all reused from dashboard/generate.py):
  - Content decay  — fetch_gsc_decay
  - Quick wins     — fetch_gsc_quick_wins
  - Traffic drops  — computed here from two 28-day periods

Run locally (validate, no post):  python3 dashboard/content_health_report.py --dry-run
Run + post:                       python3 dashboard/content_health_report.py
Override channel:                 CHANNEL_ID=8chy2nm-1554391 python3 dashboard/content_health_report.py

CI: set GSC_TOKEN_JSON, GSC_CLIENT_SECRETS_JSON, and CLICKUP_API_KEY as secrets.
    The workflow writes the GSC files to the expected paths before running this.
"""

import os
import sys
import argparse
from datetime import datetime, timezone
from urllib.parse import urlparse

# Import the proven GSC + ClickUp machinery from the dashboard generator.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests
from generate import (
    _load_gsc_auth,
    _period_dates,
    _gsc_pages_for_period,
    fetch_gsc_decay,
    fetch_gsc_quick_wins,
    CU_API_KEY,
    CU_WORKSPACE,
)

CHANNEL_ID = os.environ.get("CHANNEL_ID", "8chy2nm-1554391")

# Map the decay trend strings to the report's three-word diagnosis vocabulary.
DECAY_DIAGNOSIS = {
    "Rankings declining": "Ranking drop",
    "Rankings improved but traffic still dropped (possible search demand decline)": "Demand decline",
    "Rankings stable (possible CTR or demand decline)": "CTR collapse",
}


def log(msg):
    print(f"[content-health] {msg}", flush=True)


def path_slug(url):
    """Path-only label, matching the report style (e.g. /blog/aio/). Off-site
    hosts keep their subdomain (e.g. shop.searchatlas.com/)."""
    p = urlparse(url)
    host = p.netloc
    path = p.path or "/"
    if host in ("searchatlas.com", "www.searchatlas.com"):
        return "/ (homepage)" if path == "/" else path
    return host + ("/" if path in ("", "/") else path)


def fetch_traffic_drops(auth):
    """Pages that lost the most clicks: current 28d vs prior 28d, with a diagnosis."""
    log("Fetching GSC traffic drops…")
    p1s, p1e, p2s, p2e, *_ = _period_dates()
    cur = _gsc_pages_for_period(auth, p1s, p1e, limit=200)
    prior = _gsc_pages_for_period(auth, p2s, p2e, limit=200)
    if not prior:
        return []

    drops = []
    for url, pm in prior.items():
        prior_clicks = pm["clicks"]
        if prior_clicks <= 0:
            continue
        cm = cur.get(url, {})
        cur_clicks = cm.get("clicks", 0)
        loss = prior_clicks - cur_clicks
        if loss <= 0:
            continue
        cur_pos = cm.get("position", 0)
        prior_pos = pm["position"]
        cur_imp = cm.get("impressions", 0)
        prior_imp = pm["impressions"]
        imp_pct = ((cur_imp - prior_imp) / prior_imp * 100) if prior_imp else 0

        if cur_clicks == 0:
            diagnosis = "Page disappeared from search results"
        elif cur_pos and prior_pos and (cur_pos - prior_pos) > 2:
            diagnosis = "Ranking loss"
        elif imp_pct <= -15:
            diagnosis = "Impression decline (possible search demand drop)"
        else:
            diagnosis = "CTR collapse (rankings stable, fewer clicks)"

        pct = round((cur_clicks - prior_clicks) / prior_clicks * 100, 1)
        drops.append({
            "page": url,
            "prior_clicks": prior_clicks,
            "cur_clicks": cur_clicks,
            "loss": loss,
            "pct": pct,
            "diagnosis": diagnosis,
        })

    drops.sort(key=lambda r: -r["loss"])
    log(f"  GSC traffic drops: {len(drops)} pages")
    return drops


def build_report(decay, drops, wins):
    """Format the report exactly like the cloud routine's output."""
    today = datetime.now(timezone.utc).date().isoformat()
    L = []
    bar = "━" * 24
    L.append("📉 Search Atlas — Weekly Content Health Report")
    L.append(today)
    L.append("")
    L.append(bar)
    L.append("DECAYING PAGES (3-period decline)")
    L.append(bar)
    for d in (decay or [])[:5]:
        L.append(path_slug(d["page"]))
        L.append(f"  Clicks: {d['clicks_p3']} → {d['clicks_p2']} → {d['clicks_now']} | Loss: -{d['loss']}")
        L.append(f"  Diagnosis: {DECAY_DIAGNOSIS.get(d['trend'], d['trend'])}")
        L.append("")

    L.append(bar)
    L.append("RECENT TRAFFIC DROPS (last 28 days)")
    L.append(bar)
    for d in drops[:5]:
        L.append(path_slug(d["page"]))
        L.append(f"  Clicks: {d['prior_clicks']:,} → {d['cur_clicks']:,} ({d['pct']}%)")
        L.append(f"  Diagnosis: {d['diagnosis']}")
        L.append("")

    L.append(bar)
    L.append("QUICK WINS (position 4–15)")
    L.append(bar)
    by_impressions = sorted(wins or [], key=lambda r: -r["impressions"])[:5]
    for w in by_impressions:
        L.append(f'"{w["query"]}" — pos {w["position"]} — {w["impressions"]:,} impressions')
        L.append("")

    top_win = by_impressions[0] if by_impressions else None
    L.append(bar)
    L.append("SUMMARY")
    L.append(bar)
    L.append(f"- Total decaying pages found: {len(decay or [])}")
    L.append(f"- Total recent drops flagged: {len(drops)}")
    if top_win:
        L.append(f'- Top quick win: "{top_win["query"]}" at position {top_win["position"]} '
                 f'with {top_win["impressions"]:,} impressions')
    gone = [d for d in drops if d["diagnosis"] == "Page disappeared from search results"]
    if gone:
        names = ", ".join(path_slug(d["page"]) for d in gone[:3])
        L.append(f"- Priority action this week: Investigate the pages that vanished from search "
                 f"results — {names} dropped from real traffic to 0 clicks, signaling possible deindexing.")
    elif top_win:
        L.append(f'- Priority action this week: Capture the "{top_win["query"]}" opportunity — '
                 f'{top_win["impressions"]:,} impressions at position {top_win["position"]}.')
    return "\n".join(L).rstrip()


def post_to_clickup(text):
    """Post the report to the ClickUp chat channel via the v3 REST API."""
    if not CU_API_KEY:
        raise SystemExit("CLICKUP_API_KEY / CLICKUP_API_TOKEN not set — cannot post.")
    url = (f"https://api.clickup.com/api/v3/workspaces/{CU_WORKSPACE}"
           f"/chat/channels/{CHANNEL_ID}/messages")
    resp = requests.post(
        url,
        headers={"Authorization": CU_API_KEY, "Content-Type": "application/json"},
        json={"type": "message", "content": text, "content_format": "text/plain"},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Build and print the report, do not post.")
    args = ap.parse_args()

    auth = _load_gsc_auth()
    if not auth:
        raise SystemExit("GSC OAuth not available — check GSC_TOKEN_JSON / client_secrets.")

    decay = fetch_gsc_decay(auth)
    drops = fetch_traffic_drops(auth)
    wins = fetch_gsc_quick_wins(auth)
    report = build_report(decay, drops, wins)

    if args.dry_run:
        print("\n" + report + "\n")
        log("DRY RUN — not posted.")
        return

    result = post_to_clickup(report)
    log(f"Posted to channel {CHANNEL_ID} (message {result.get('data', {}).get('id', '?')}).")


if __name__ == "__main__":
    main()
