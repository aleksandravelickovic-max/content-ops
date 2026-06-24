#!/usr/bin/env python3
"""
Weekly Content Health Report for searchatlas.com.

Replaces the cloud routine "SA Weekly Content Health Report", which broke when
Search Atlas's built-in GSC integration was disconnected. This script pulls GSC
data directly via OAuth (the same token the dashboard uses, no Search Atlas
dependency) and posts the report to a ClickUp chat channel via the v3 REST API.

Self-contained: depends only on `requests`. The GSC helpers are mirrored from
dashboard/generate.py so this runs on `main` without the rest of the dashboard.

Run locally (validate, no post):  python3 dashboard/content_health_report.py --dry-run
Run + post:                       CLICKUP_API_KEY=pk_... python3 dashboard/content_health_report.py

CI: set GSC_TOKEN_JSON, GSC_CLIENT_SECRETS_JSON, and CLICKUP_API_KEY as secrets.
    The workflow writes the GSC files to the expected paths before running this.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

# ── Config ───────────────────────────────────────────────────────────────────
# Optional .env next to this script (for local runs); CI uses real env vars.
_env = Path(__file__).parent / ".env"
if _env.exists():
    for _line in _env.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

GSC_PROPERTY     = os.environ.get("GSC_PROPERTY", "sc-domain:searchatlas.com")
GSC_TOKEN_FILE   = Path.home() / ".gsc-mcp" / "oauth-token.json"
GSC_SECRETS_FILE = Path.home() / ".config" / "gsc" / "client_secrets.json"
GSC_API_BASE     = "https://searchconsole.googleapis.com/webmasters/v3"

CU_API_KEY   = os.environ.get("CLICKUP_API_TOKEN", "") or os.environ.get("CLICKUP_API_KEY", "")
CU_WORKSPACE = os.environ.get("CLICKUP_WORKSPACE_ID", "9011399348")
CHANNEL_ID   = os.environ.get("CHANNEL_ID", "8chy2nm-1554391")

# Action-task creation (SEO Content list). Findings → tasks, assigned to a writer.
SEO_CONTENT_LIST  = os.environ.get("SEO_CONTENT_LIST_ID", "901111125948")
ASSIGNEE_DEFAULT  = int(os.environ.get("TASK_ASSIGNEE", "81531694"))   # Milena Barbaresco
ASSIGNEE_HOMEPAGE = int(os.environ.get("TASK_ASSIGNEE_HOMEPAGE", "81501508"))  # Aleksandra
TASK_STATUS       = "ready for writer"

# Short diagnosis labels for traffic-drop task titles.
DROP_SHORT = {
    "Page disappeared from search results": "deindexed",
    "Ranking loss": "ranking loss",
    "Impression decline (possible search demand drop)": "impression decline",
    "CTR collapse (rankings stable, fewer clicks)": "CTR collapse",
}
# Per-diagnosis refresh guidance for decay task titles + descriptions.
DECAY_ACTION = {
    "Ranking drop":   ("refresh to recover slipping rankings",
                       "Rankings are slipping — refresh the content and internal links to recover position."),
    "Demand decline": ("update for current search intent",
                       "Rankings held but clicks fell — refresh for current search intent and adjacent queries; verify the keyword still has volume."),
    "CTR collapse":   ("fix CTR collapse — snippet not converting",
                       "Ranking is stable but the snippet isn't converting — test a new title/meta description; it may be losing to ads or AI overviews."),
}

DECAY_DIAGNOSIS = {
    "Rankings declining": "Ranking drop",
    "Rankings improved but traffic still dropped (possible search demand decline)": "Demand decline",
    "Rankings stable (possible CTR or demand decline)": "CTR collapse",
}


def log(msg):
    print(f"[content-health] {msg}", flush=True)


# ── GSC (direct OAuth) — mirrored from dashboard/generate.py ───────────────────

def _load_gsc_auth():
    """Load and auto-refresh the stored GSC OAuth token. Returns headers or None."""
    if not GSC_TOKEN_FILE.exists() or not GSC_SECRETS_FILE.exists():
        return None
    try:
        token   = json.loads(GSC_TOKEN_FILE.read_text())
        secrets = json.loads(GSC_SECRETS_FILE.read_text())
        creds   = secrets.get("installed") or secrets.get("web") or {}
        now_ms  = int(datetime.now(timezone.utc).timestamp() * 1000)
        if token.get("expiry_date", 0) < now_ms + 60_000:
            resp = requests.post(creds["token_uri"], data={
                "client_id":     creds["client_id"],
                "client_secret": creds["client_secret"],
                "refresh_token": token["refresh_token"],
                "grant_type":    "refresh_token",
            }, timeout=15)
            if resp.status_code == 200:
                new = resp.json()
                token["access_token"] = new["access_token"]
                token["expiry_date"]  = now_ms + int(new.get("expires_in", 3600)) * 1000
                GSC_TOKEN_FILE.write_text(json.dumps(token, indent=2))
                log("  GSC token refreshed")
            else:
                log(f"  GSC token refresh failed: {resp.status_code}")
        return {"Authorization": f"Bearer {token['access_token']}"}
    except Exception as e:
        log(f"  GSC auth error: {e}")
        return None


def _gsc_query(auth, body):
    site = GSC_PROPERTY.replace(":", "%3A")
    url  = f"{GSC_API_BASE}/sites/{site}/searchAnalytics/query"
    try:
        resp = requests.post(url, headers={**auth, "Content-Type": "application/json"},
                             json=body, timeout=20)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return None, str(e)


def _gsc_pages_for_period(auth, start, end, limit=200):
    data, err = _gsc_query(auth, {
        "startDate": str(start), "endDate": str(end),
        "dimensions": ["page"], "rowLimit": limit,
    })
    if err:
        log(f"  GSC pages error ({start}→{end}): {err}")
        return {}
    out = {}
    for r in (data or {}).get("rows", []):
        url = (r.get("keys") or [None])[0]
        if url:
            out[url] = {
                "clicks":      int(r.get("clicks", 0)),
                "impressions": int(r.get("impressions", 0)),
                "ctr":         round(float(r.get("ctr", 0)) * 100, 2),
                "position":    round(float(r.get("position", 0)), 1),
            }
    return out


def _period_dates():
    """P1 = current 28d, P2 = prior 28d, P3 = oldest 28d. GSC lags ~3 days."""
    today    = datetime.now(timezone.utc).date()
    p1_end   = today - timedelta(days=3)
    p1_start = p1_end - timedelta(days=27)
    p2_end   = p1_start - timedelta(days=1)
    p2_start = p2_end - timedelta(days=27)
    p3_end   = p2_start - timedelta(days=1)
    p3_start = p3_end - timedelta(days=27)
    return p1_start, p1_end, p2_start, p2_end, p3_start, p3_end


def fetch_decay(auth):
    """Pages with net click decline across 3 consecutive 28-day periods."""
    log("Fetching GSC content decay…")
    p1s, p1e, p2s, p2e, p3s, p3e = _period_dates()
    p1 = _gsc_pages_for_period(auth, p1s, p1e, limit=150)
    p2 = _gsc_pages_for_period(auth, p2s, p2e, limit=150)
    p3 = _gsc_pages_for_period(auth, p3s, p3e, limit=150)
    if not p1:
        return []
    decay = []
    for url, m1 in p1.items():
        m3 = p3.get(url, {})
        clicks_now, clicks_p3 = m1["clicks"], m3.get("clicks", 0)
        if not clicks_p3:
            continue
        loss = clicks_p3 - clicks_now
        if loss < 3 or loss / clicks_p3 < 0.10:
            continue
        pos_delta = m1["position"] - m3.get("position", m1["position"])
        if pos_delta > 1.0:
            trend = "Rankings declining"
        elif pos_delta < -1.0:
            trend = "Rankings improved but traffic still dropped (possible search demand decline)"
        else:
            trend = "Rankings stable (possible CTR or demand decline)"
        decay.append({
            "page": url, "clicks_now": clicks_now,
            "clicks_p2": p2.get(url, {}).get("clicks", 0), "clicks_p3": clicks_p3,
            "loss": loss, "trend": trend,
        })
    decay.sort(key=lambda r: -r["loss"])
    log(f"  GSC decay: {len(decay)} pages")
    return decay


def fetch_quick_wins(auth):
    """Keywords in position 4–15 with high impressions and low CTR."""
    log("Fetching GSC quick wins…")
    p1s, p1e, *_ = _period_dates()
    data, err = _gsc_query(auth, {
        "startDate": str(p1s), "endDate": str(p1e),
        "dimensions": ["query"], "rowLimit": 250,
    })
    if err:
        log(f"  GSC quick wins error: {err}")
        return []
    wins = []
    for r in (data or {}).get("rows", []):
        query    = (r.get("keys") or [None])[0]
        position = round(float(r.get("position", 0)), 1)
        if not query or position < 4 or position > 15:
            continue
        impressions = int(r.get("impressions", 0))
        if impressions < 500:
            continue
        ctr = float(r.get("ctr", 0))
        if max(0, round(impressions * (0.11 - ctr))) < 100:
            continue
        wins.append({"query": query, "position": position, "impressions": impressions})
    wins.sort(key=lambda r: -r["impressions"])
    log(f"  GSC quick wins: {len(wins)} keywords")
    return wins


def fetch_traffic_drops(auth):
    """Pages that lost the most clicks: current 28d vs prior 28d, with diagnosis."""
    log("Fetching GSC traffic drops…")
    p1s, p1e, p2s, p2e, *_ = _period_dates()
    cur   = _gsc_pages_for_period(auth, p1s, p1e, limit=200)
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
        cur_pos, prior_pos = cm.get("position", 0), pm["position"]
        cur_imp, prior_imp = cm.get("impressions", 0), pm["impressions"]
        imp_pct = ((cur_imp - prior_imp) / prior_imp * 100) if prior_imp else 0
        if cur_clicks == 0:
            diagnosis = "Page disappeared from search results"
        elif cur_pos and prior_pos and (cur_pos - prior_pos) > 2:
            diagnosis = "Ranking loss"
        elif imp_pct <= -15:
            diagnosis = "Impression decline (possible search demand drop)"
        else:
            diagnosis = "CTR collapse (rankings stable, fewer clicks)"
        drops.append({
            "page": url, "prior_clicks": prior_clicks, "cur_clicks": cur_clicks,
            "loss": loss, "pct": round((cur_clicks - prior_clicks) / prior_clicks * 100, 1),
            "diagnosis": diagnosis,
        })
    drops.sort(key=lambda r: -r["loss"])
    log(f"  GSC traffic drops: {len(drops)} pages")
    return drops


# ── Report ─────────────────────────────────────────────────────────────────--

def path_slug(url):
    """Path-only label (e.g. /blog/aio/). Off-site hosts keep their subdomain."""
    p = urlparse(url)
    host, path = p.netloc, (p.path or "/")
    if host in ("searchatlas.com", "www.searchatlas.com"):
        return "/ (homepage)" if path == "/" else path
    return host + ("/" if path in ("", "/") else path)


def build_report(decay, drops, wins):
    today = datetime.now(timezone.utc).date().isoformat()
    bar = "━" * 24
    L = ["📉 Search Atlas — Weekly Content Health Report", today, "",
         bar, "DECAYING PAGES (3-period decline)", bar]
    for d in decay[:5]:
        L += [path_slug(d["page"]),
              f"  Clicks: {d['clicks_p3']} → {d['clicks_p2']} → {d['clicks_now']} | Loss: -{d['loss']}",
              f"  Diagnosis: {DECAY_DIAGNOSIS.get(d['trend'], d['trend'])}", ""]
    L += [bar, "RECENT TRAFFIC DROPS (last 28 days)", bar]
    for d in drops[:5]:
        L += [path_slug(d["page"]),
              f"  Clicks: {d['prior_clicks']:,} → {d['cur_clicks']:,} ({d['pct']}%)",
              f"  Diagnosis: {d['diagnosis']}", ""]
    L += [bar, "QUICK WINS (position 4–15)", bar]
    top5 = wins[:5]
    for w in top5:
        L += [f'"{w["query"]}" — pos {w["position"]} — {w["impressions"]:,} impressions', ""]
    L += [bar, "SUMMARY", bar,
          f"- Total decaying pages found: {len(decay)}",
          f"- Total recent drops flagged: {len(drops)}"]
    if top5:
        t = top5[0]
        L.append(f'- Top quick win: "{t["query"]}" at position {t["position"]} '
                 f'with {t["impressions"]:,} impressions')
    gone = [d for d in drops if d["diagnosis"] == "Page disappeared from search results"]
    if gone:
        names = ", ".join(path_slug(d["page"]) for d in gone[:3])
        L.append(f"- Priority action this week: Investigate the pages that vanished from search "
                 f"results — {names} dropped from real traffic to 0 clicks, signaling possible deindexing.")
    elif top5:
        t = top5[0]
        L.append(f'- Priority action this week: Capture the "{t["query"]}" opportunity — '
                 f'{t["impressions"]:,} impressions at position {t["position"]}.')
    return "\n".join(L).rstrip()


def post_to_clickup(text):
    if not CU_API_KEY:
        raise SystemExit("CLICKUP_API_KEY / CLICKUP_API_TOKEN not set — cannot post.")
    url = (f"https://api.clickup.com/api/v3/workspaces/{CU_WORKSPACE}"
           f"/chat/channels/{CHANNEL_ID}/messages")
    resp = requests.post(url, headers={"Authorization": CU_API_KEY, "Content-Type": "application/json"},
                         json={"type": "message", "content": text, "content_format": "text/plain"},
                         timeout=20)
    resp.raise_for_status()
    return resp.json()


# ── ClickUp action tasks (v2 REST) ─────────────────────────────────────────---

def _dedup_key(slug):
    """Normalized key used to detect an existing open task for a page."""
    return "homepage" if slug == "/ (homepage)" else slug.lower()


def _open_task_names():
    """Names of all non-closed tasks in the SEO Content list (for dedup)."""
    names, page = [], 0
    while True:
        url = f"https://api.clickup.com/api/v2/list/{SEO_CONTENT_LIST}/task"
        resp = requests.get(url, headers={"Authorization": CU_API_KEY},
                            params={"include_closed": "false", "subtasks": "false", "page": page},
                            timeout=20)
        resp.raise_for_status()
        tasks = resp.json().get("tasks", [])
        if not tasks:
            break
        names += [t.get("name", "").lower() for t in tasks]
        if len(tasks) < 100:
            break
        page += 1
    return names


def _create_task(name, markdown, assignee, tags=None, priority=3, dry_run=False):
    if dry_run:
        log(f"  WOULD CREATE: {name}")
        return
    url = f"https://api.clickup.com/api/v2/list/{SEO_CONTENT_LIST}/task"
    body = {"name": name, "markdown_content": markdown, "status": TASK_STATUS,
            "assignees": [assignee], "priority": priority}
    if tags:
        body["tags"] = tags
    resp = requests.post(url, headers={"Authorization": CU_API_KEY, "Content-Type": "application/json"},
                         json=body, timeout=20)
    resp.raise_for_status()
    log(f"  created: {name}")


def create_tasks(decay, drops, wins, dry_run=False):
    """Create action tasks for the top findings, skipping pages/queries that
    already have an open task. Drops first, then decay (one task per page)."""
    existing = _open_task_names()
    seen = set()                       # page keys handled this run
    created = 0

    def page_taken(key):
        if key in seen:
            return True
        return any(key in n for n in existing)

    # Traffic drops → Recover / Investigate
    for d in drops[:5]:
        slug = path_slug(d["page"])
        key = _dedup_key(slug)
        if page_taken(key):
            continue
        seen.add(key)
        short = DROP_SHORT.get(d["diagnosis"], d["diagnosis"])
        if key == "homepage":
            name = f"Investigate homepage traffic drop — -{d['loss']:,} clicks ({d['pct']}%)"
            assignee = ASSIGNEE_HOMEPAGE
        else:
            name = f"Recover {slug} — {short}, -{d['loss']:,} clicks ({d['pct']}%)"
            assignee = ASSIGNEE_DEFAULT
        md = (f"**Source:** Content Health Report — Recent Traffic Drops\n\n"
              f"**Clicks:** {d['prior_clicks']:,} → {d['cur_clicks']:,} ({d['pct']}%)\n"
              f"**Diagnosis:** {d['diagnosis']}\n\n"
              f"**Action:** Diagnose the cause and refresh the page to recover the lost clicks.")
        _create_task(name, md, assignee, priority=2, dry_run=dry_run)
        created += 1

    # Decaying pages → Refresh (tagged 'refresh')
    for d in decay[:5]:
        slug = path_slug(d["page"])
        key = _dedup_key(slug)
        if page_taken(key):
            continue
        seen.add(key)
        diag = DECAY_DIAGNOSIS.get(d["trend"], d["trend"])
        title_action, body_action = DECAY_ACTION.get(diag, ("refresh content", "Refresh the content."))
        name = f"Refresh {slug} — {title_action}"
        md = (f"**Source:** Content Health Report — Decaying Pages\n\n"
              f"**Click loss:** {d['clicks_p3']} → {d['clicks_p2']} → {d['clicks_now']} (total: -{d['loss']})\n"
              f"**Diagnosis:** {diag}\n\n**Action:** {body_action}")
        assignee = ASSIGNEE_HOMEPAGE if key == "homepage" else ASSIGNEE_DEFAULT
        _create_task(name, md, assignee, tags=["refresh"], priority=2, dry_run=dry_run)
        created += 1

    # Quick wins → Quick win (keyed by query, separate namespace)
    for w in wins[:5]:
        q = w["query"]
        if any(q.lower() in n for n in existing):
            continue
        name = f'Quick win: "{q}" — pos {w["position"]}, {w["impressions"]:,} impressions'
        md = (f"**Source:** Content Health Report — Quick Wins\n\n"
              f"**Position:** {w['position']}\n**Impressions:** {w['impressions']:,}\n\n"
              f"**Action:** Add a direct-answer section / FAQ targeting this exact query to capture the impressions.")
        _create_task(name, md, ASSIGNEE_DEFAULT, priority=3, dry_run=dry_run)
        created += 1

    log(f"{'Would create' if dry_run else 'Created'} {created} task(s).")
    return created


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Build and print, do not post or create tasks.")
    ap.add_argument("--no-tasks", action="store_true", help="Post the report but do not create tasks.")
    ap.add_argument("--no-post", action="store_true", help="Skip posting the report; still create tasks.")
    args = ap.parse_args()
    auth = _load_gsc_auth()
    if not auth:
        raise SystemExit("GSC OAuth not available — check GSC_TOKEN_JSON / client_secrets.")
    decay, drops, wins = fetch_decay(auth), fetch_traffic_drops(auth), fetch_quick_wins(auth)
    report = build_report(decay, drops, wins)
    if args.dry_run:
        print("\n" + report + "\n")
        log("DRY RUN — not posted.")
        if not args.no_tasks:
            create_tasks(decay, drops, wins, dry_run=True)
        return
    if args.no_post:
        log("Skipping report post (--no-post).")
    else:
        result = post_to_clickup(report)
        log(f"Posted to channel {CHANNEL_ID} (message {result.get('data', {}).get('id', '?')}).")
    if not args.no_tasks:
        create_tasks(decay, drops, wins, dry_run=False)


if __name__ == "__main__":
    main()
