#!/usr/bin/env python3
"""
Dashboard data generator.

Pulls from:
  - Google GSC API   (OAuth token at ~/.gsc-mcp/oauth-token.json) — traffic, pages, decay, quick wins
  - SearchAtlas API  (SEARCHATLAS_API_KEY)  — ContentGenius articles, quota
  - ClickUp API      (CLICKUP_API_KEY)       — content pipeline task counts

Writes:  dashboard/data.json

Run manually:     python3 dashboard/generate.py
Run with debug:   python3 dashboard/generate.py --debug

CI: set GSC_TOKEN_JSON and GSC_CLIENT_SECRETS_JSON as GitHub secrets.
    The workflow writes them to the expected paths before running this script.
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing dependency: pip install requests")
    sys.exit(1)

# ── Config ──────────────────────────────────────────────────────────────────

REPO_ROOT    = Path(__file__).parent.parent
DASHBOARD    = Path(__file__).parent
OUTPUT_FILE  = DASHBOARD / "data.json"
CLIENTS_DIR  = REPO_ROOT / "clients"

# Load .env from dashboard directory if it exists
_env_file = DASHBOARD / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

SA_API_KEY   = os.environ.get("SEARCHATLAS_API_KEY", "")
SA_BASE_URL  = os.environ.get("SEARCHATLAS_BASE_URL", "https://api.searchatlas.com/api/v1")

# Support both CLICKUP_API_TOKEN and CLICKUP_API_KEY
CU_API_KEY   = os.environ.get("CLICKUP_API_TOKEN", "") or os.environ.get("CLICKUP_API_KEY", "")
CU_WORKSPACE = os.environ.get("CLICKUP_WORKSPACE_ID", "9011399348")

# ClickUp content list IDs (SA Marketing → Content Writing Team)
CLICKUP_LISTS = {
    "SEO Content":            "901111125948",
    "General Content":        "901110742485",
    "Agentic Marketing":      "901113624480",
    "Trophy / LLM Content":   "901112999493",
    "AI Content":             "901112648779",
}

# GSC property to pull (update when GSC is connected)
GSC_PROPERTY = os.environ.get("GSC_PROPERTY", "sc-domain:searchatlas.com")

DEBUG = False


# ── Helpers ──────────────────────────────────────────────────────────────────

def log(msg):
    print(f"[generate] {msg}", flush=True)


def sa_get(path, params=None):
    if not SA_API_KEY:
        return None, "SEARCHATLAS_API_KEY not set"
    url = f"{SA_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    headers = {"Authorization": f"Token {SA_API_KEY}", "Content-Type": "application/json"}
    try:
        resp = requests.get(url, headers=headers, params=params or {}, timeout=20)
        if DEBUG:
            log(f"SA GET {url} → {resp.status_code}")
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return None, str(e)


def cu_get(path, params=None):
    if not CU_API_KEY:
        return None, "CLICKUP_API_KEY not set"
    url = f"https://api.clickup.com/api/v2/{path.lstrip('/')}"
    headers = {"Authorization": CU_API_KEY}
    try:
        resp = requests.get(url, headers=headers, params=params or {}, timeout=20)
        if DEBUG:
            log(f"CU GET {url} → {resp.status_code}")
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return None, str(e)


# ── Google GSC (direct OAuth) ────────────────────────────────────────────────

GSC_TOKEN_FILE   = Path.home() / ".gsc-mcp"  / "oauth-token.json"
GSC_SECRETS_FILE = Path.home() / ".config"   / "gsc" / "client_secrets.json"
GSC_API_BASE     = "https://searchconsole.googleapis.com/webmasters/v3"


def _load_gsc_auth():
    """Load and auto-refresh the stored GSC OAuth token. Returns headers dict or None."""
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
    """POST to GSC searchAnalytics/query for GSC_PROPERTY."""
    site = GSC_PROPERTY.replace(":", "%3A")
    url  = f"{GSC_API_BASE}/sites/{site}/searchAnalytics/query"
    try:
        resp = requests.post(url, headers={**auth, "Content-Type": "application/json"},
                             json=body, timeout=20)
        if DEBUG:
            log(f"  GSC POST → {resp.status_code}")
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return None, str(e)


def _slug_from_url(url, lookup=None):
    """Human-readable label for a URL. Uses lookup dict first, then derives from path."""
    if lookup and url in lookup:
        return lookup[url]
    try:
        from urllib.parse import urlparse
        p     = urlparse(url)
        host  = p.netloc
        parts = [x for x in p.path.rstrip("/").split("/") if x]
        if host != "searchatlas.com":
            return host + ("/" + "/".join(parts) if parts else "")
        if not parts:
            return "Homepage"
        if parts[0] == "blog":
            return "Blog: " + (parts[1].replace("-", " ").title() if len(parts) > 1 else "index")
        return parts[-1].replace("-", " ").title()
    except Exception:
        return url


def _gsc_pages_for_period(auth, start, end, limit=100):
    """Return {url: {clicks, impressions, ctr, position}} for one period."""
    data, err = _gsc_query(auth, {
        "startDate": str(start),
        "endDate":   str(end),
        "dimensions": ["page"],
        "rowLimit":   limit,
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
    """Return (p1_start, p1_end, p2_start, p2_end, p3_start, p3_end) as date objects.
    P1 = current 28d, P2 = prior 28d, P3 = oldest 28d. GSC lags ~3 days."""
    today   = datetime.now(timezone.utc).date()
    p1_end  = today - timedelta(days=3)
    p1_start = p1_end - timedelta(days=27)
    p2_end  = p1_start - timedelta(days=1)
    p2_start = p2_end - timedelta(days=27)
    p3_end  = p2_start - timedelta(days=1)
    p3_start = p3_end - timedelta(days=27)
    return p1_start, p1_end, p2_start, p2_end, p3_start, p3_end


BRAND_REGEX = "searchatlas|search atlas|linkgraph|otto seo|atlas agent|manick bhan"


def fetch_gsc_branded_split(auth, total_cur, total_prior):
    """Branded vs non-branded click split for current and prior 28-day periods.
    Non-branded = total_clicks - branded_clicks (avoids double-counting edge cases)."""
    log("Fetching GSC branded/non-branded split…")
    p1s, p1e, p2s, p2e, *_ = _period_dates()

    def branded_clicks(start, end):
        data, err = _gsc_query(auth, {
            "startDate": str(start),
            "endDate":   str(end),
            "dimensions": ["query"],
            "dimensionFilterGroups": [{
                "groupType": "and",
                "filters": [{"dimension": "QUERY", "operator": "includingRegex", "expression": BRAND_REGEX}],
            }],
            "rowLimit": 500,
        })
        if err:
            log(f"  GSC branded error ({start}→{end}): {err}")
            return None
        return sum(int(r.get("clicks", 0)) for r in (data or {}).get("rows", []))

    b_cur   = branded_clicks(p1s, p1e)
    b_prior = branded_clicks(p2s, p2e)
    if b_cur is None:
        return None

    nb_cur    = max(0, total_cur   - b_cur)
    nb_prior  = max(0, total_prior - b_prior) if b_prior is not None else None
    pct_cur   = round(nb_cur  / total_cur   * 100, 1) if total_cur   else 0.0
    pct_prior = round(nb_prior / total_prior * 100, 1) if (nb_prior is not None and total_prior) else None
    ppt_chg   = round(pct_cur - pct_prior, 1) if pct_prior is not None else None

    log(f"  Non-branded: {nb_cur} ({pct_cur}%)  Branded: {b_cur} ({round(b_cur/total_cur*100,1) if total_cur else 0}%)")
    return {
        "brand_filter": BRAND_REGEX,
        "current": {
            "branded_clicks":    b_cur,
            "nonbranded_clicks": nb_cur,
            "nonbranded_pct":    pct_cur,
        },
        "prior": {
            "branded_clicks":    b_prior,
            "nonbranded_clicks": nb_prior,
            "nonbranded_pct":    pct_prior,
        } if b_prior is not None else None,
        "nonbranded_ppt_change": ppt_chg,
    }


def fetch_gsc(auth):
    """Site-level totals: current vs prior 28-day period."""
    log("Fetching GSC site performance…")
    p1s, p1e, p2s, p2e, *_ = _period_dates()

    def pull_totals(start, end):
        data, err = _gsc_query(auth, {"startDate": str(start), "endDate": str(end), "rowLimit": 1})
        if err:
            log(f"  GSC totals error: {err}")
            return {}
        rows = (data or {}).get("rows", [])
        if not rows:
            return {}
        r = rows[0]
        return {
            "clicks":      int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "ctr":         round(float(r.get("ctr", 0)) * 100, 2),
            "position":    round(float(r.get("position", 0)), 1),
        }

    cur  = pull_totals(p1s, p1e)
    prev = pull_totals(p2s, p2e)
    if not cur:
        return None

    def pct(key):
        c, p = cur.get(key, 0) or 0, prev.get(key, 0) or 0
        return round((c - p) / p * 100, 2) if p else None

    def delta(key):
        return round((cur.get(key, 0) or 0) - (prev.get(key, 0) or 0), 2)

    log(f"  GSC: clicks={cur.get('clicks')}, impressions={cur.get('impressions')}")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period": f"{p1s} to {p1e}",
        "current": cur,
        "prior":   prev,
        "change": {
            "clicks_pct":      pct("clicks"),
            "impressions_pct": pct("impressions"),
            "ctr_delta":       delta("ctr"),
            "position_change": delta("position"),
        },
    }


def fetch_gsc_content_performance(auth, slug_lookup=None):
    """Top 10 pages by clicks + climbing pages (≥20% growth). Two periods."""
    log("Fetching GSC page performance…")
    p1s, p1e, p2s, p2e, *_ = _period_dates()
    now_pages   = _gsc_pages_for_period(auth, p1s, p1e, limit=50)
    prior_pages = _gsc_pages_for_period(auth, p2s, p2e, limit=50)
    if not now_pages:
        return None

    top_pages = []
    for url, m in sorted(now_pages.items(), key=lambda x: -x[1]["clicks"])[:10]:
        top_pages.append({
            "page":        url,
            "slug":        _slug_from_url(url, slug_lookup),
            "clicks":      m["clicks"],
            "impressions": m["impressions"],
            "ctr":         m["ctr"],
            "position":    m["position"],
        })

    climbing = []
    for url, m in now_pages.items():
        if m["clicks"] < 10:
            continue
        prior_clicks = (prior_pages.get(url) or {}).get("clicks", 0)
        if prior_clicks == 0:
            climbing.append({"page": url, "slug": _slug_from_url(url, slug_lookup),
                             "clicks_prior": 0, "clicks_now": m["clicks"],
                             "growth_pct": None, "is_new": True, "position": m["position"]})
        elif m["clicks"] >= prior_clicks * 1.2:
            growth = round((m["clicks"] - prior_clicks) / prior_clicks * 100, 1)
            climbing.append({"page": url, "slug": _slug_from_url(url, slug_lookup),
                             "clicks_prior": prior_clicks, "clicks_now": m["clicks"],
                             "growth_pct": growth, "is_new": False, "position": m["position"]})

    climbing.sort(key=lambda r: (0 if r["is_new"] else -(r["growth_pct"] or 0)))
    log(f"  GSC pages: {len(top_pages)} top, {len(climbing)} climbing")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": f"Current 28d ({p1s}–{p1e}) vs prior 28d ({p2s}–{p2e}). Source: GSC.",
        "top_pages": top_pages,
        "climbing": climbing[:10],
    }


def fetch_gsc_decay(auth, slug_lookup=None):
    """Pages with consistent click decline across 3 consecutive 28-day periods."""
    log("Fetching GSC content decay…")
    p1s, p1e, p2s, p2e, p3s, p3e = _period_dates()
    p1 = _gsc_pages_for_period(auth, p1s, p1e, limit=150)
    p2 = _gsc_pages_for_period(auth, p2s, p2e, limit=150)
    p3 = _gsc_pages_for_period(auth, p3s, p3e, limit=150)
    if not p1:
        return None

    decay = []
    for url, m1 in p1.items():
        m3 = p3.get(url, {})
        clicks_now = m1["clicks"]
        clicks_p3  = m3.get("clicks", 0)
        if not clicks_p3:
            continue
        loss = clicks_p3 - clicks_now
        if loss < 3 or loss / clicks_p3 < 0.10:
            continue
        m2 = p2.get(url, {})
        pos_now = m1["position"]
        pos_p3  = m3.get("position", pos_now)
        pos_delta = pos_now - pos_p3  # positive = worse, negative = improved
        if pos_delta > 1.0:
            trend = "Rankings declining"
        elif pos_delta < -1.0:
            trend = "Rankings improved but traffic still dropped (possible search demand decline)"
        else:
            trend = "Rankings stable (possible CTR or demand decline)"
        decay.append({
            "page":         url,
            "slug":         _slug_from_url(url, slug_lookup),
            "clicks_now":   clicks_now,
            "clicks_p2":    m2.get("clicks", 0),
            "clicks_p3":    clicks_p3,
            "loss":         loss,
            "position_now": pos_now,
            "trend":        trend,
        })

    decay.sort(key=lambda r: -r["loss"])
    log(f"  GSC decay: {len(decay)} pages")
    return decay


def fetch_gsc_quick_wins(auth):
    """Keywords in position 4–15 with high impressions and low CTR."""
    log("Fetching GSC quick wins…")
    p1s, p1e, *_ = _period_dates()
    data, err = _gsc_query(auth, {
        "startDate":  str(p1s),
        "endDate":    str(p1e),
        "dimensions": ["query"],
        "rowLimit":   250,
    })
    if err:
        log(f"  GSC quick wins error: {err}")
        return None

    wins = []
    for r in (data or {}).get("rows", []):
        query      = (r.get("keys") or [None])[0]
        position   = round(float(r.get("position", 0)), 1)
        if not query or position < 4 or position > 15:
            continue
        impressions = int(r.get("impressions", 0))
        if impressions < 500:
            continue
        clicks = int(r.get("clicks", 0))
        ctr    = float(r.get("ctr", 0))
        # Opportunity = clicks you'd gain at ~11% CTR (top-5 benchmark) minus current clicks
        opportunity = max(0, round(impressions * (0.11 - ctr)))
        if opportunity < 100:
            continue
        wins.append({
            "query":       query,
            "position":    position,
            "impressions": impressions,
            "clicks":      clicks,
            "ctr":         round(ctr, 4),
            "opportunity": opportunity,
        })

    wins.sort(key=lambda r: -r["opportunity"])
    log(f"  GSC quick wins: {len(wins)} keywords")
    return wins[:20]


# ── Data sources ─────────────────────────────────────────────────────────────

def fetch_contentgenius():
    """Pull article list from ContentGenius."""
    log("Fetching ContentGenius articles…")
    data, err = sa_get("/content-genius/articles/", {"page_size": 50, "ordering": "-updated_at"})
    if err:
        log(f"  CG error: {err}")
        return None

    items = data.get("results") or data.get("items") or []
    status_map = {
        "NOT_BEGUN": "not_begun",
        "IN_PROGRESS": "in_progress",
        "NEEDS_REVIEW": "needs_review",
        "COMPLETED": "completed",
    }
    summary = {"not_begun": 0, "in_progress": 0, "needs_review": 0, "completed": 0, "total": len(items)}
    articles = []
    for item in items:
        raw_status = item.get("status", "NOT_BEGUN")
        key = status_map.get(raw_status, "not_begun")
        summary[key] = summary.get(key, 0) + 1
        articles.append({
            "id": item.get("id"),
            "title": item.get("title", ""),
            "status": raw_status,
            "score": item.get("content_score"),
            "updated": (item.get("updated_at") or "")[:10],
        })

    log(f"  Found {len(articles)} articles")
    return {
        "source": "contentgenius",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "articles": articles,
    }


PUBLISHED_LISTS = {
    "SEO Content":     "901111125948",
    "General Content": "901110742485",
}

CU_USER_ID = os.environ.get("CLICKUP_USER_ID", "81501508")

ASSIGNED_LISTS = {
    "SEO Content":       "901111125948",
    "General Content":   "901110742485",
    "Agentic Marketing": "901113624480",
}

def fetch_clickup_articles_published(days=7):
    """Count tasks moved to 'published' status in the last N days."""
    if not CU_API_KEY:
        return None

    log(f"Fetching ClickUp articles published (last {days}d)…")
    cutoff_ms = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp() * 1000)
    count = 0
    tasks_found = []

    for list_name, list_id in PUBLISHED_LISTS.items():
        data, err = cu_get(f"/list/{list_id}/task", {
            "statuses[]": "published",
            "date_done_gt": cutoff_ms,
            "include_closed": "true",
            "order_by": "updated",
            "reverse": "true",
        })
        if err:
            log(f"  ClickUp '{list_name}' published error: {err}")
            continue

        tasks = data.get("tasks", [])
        log(f"  {list_name}: {len(tasks)} published in last {days}d")
        count += len(tasks)
        for t in tasks:
            tasks_found.append({
                "title": t.get("name", ""),
                "list": list_name,
                "updated": datetime.fromtimestamp(
                    int(t["date_updated"]) / 1000, tz=timezone.utc
                ).strftime("%Y-%m-%d") if t.get("date_updated") else "",
            })

    return {
        "articles_published_7d": count,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_days": days,
        "tasks": tasks_found,
    }


def fetch_clickup_task_buckets():
    """Bucket Aleksandra's tasks into Overdue / No Due Date / Assigned / Recently Completed.

    ClickUp's `include_closed` flag and `date_closed_gt` query param don't behave as
    their names suggest on this endpoint (include_closed=false still returns many
    "complete"-status tasks; date_closed_gt is ignored entirely). The only reliable
    signal is the `date_closed` field itself: null means still open, set means done.
    So fetch everything once and bucket client-side on due_date / date_closed.
    """
    if not CU_API_KEY:
        return None

    log("Fetching ClickUp task buckets (overdue/no-due-date/assigned/recently-completed)…")
    now = datetime.now(timezone.utc)
    all_tasks = []
    for list_name, list_id in ASSIGNED_LISTS.items():
        page = 0
        while True:
            data, err = cu_get(f"/list/{list_id}/task", {
                "assignees[]": CU_USER_ID,
                "include_closed": "true",
                "page": page,
            })
            if err:
                log(f"  ClickUp '{list_name}' page {page} error: {err}")
                break
            tasks = data.get("tasks", [])
            for t in tasks:
                t["_list_name"] = list_name
                all_tasks.append(t)
            if len(tasks) < 100:
                break
            page += 1

    overdue, no_due, assigned, recently_completed = [], [], [], []
    cutoff_ms = int((now - timedelta(days=7)).timestamp() * 1000)

    # Statuses that mean "done" in this workspace even when date_closed is unset.
    # ClickUp doesn't always populate date_closed for every completed-type status.
    DONE_STATUSES = {"complete", "approved", "published", "closed", "done"}

    for t in all_tasks:
        status = (t.get("status", {}) or {}).get("status", "").lower()
        base = {
            "id": t.get("id"),
            "title": t.get("name", ""),
            "status": status,
            "list": t["_list_name"],
            "url": t.get("url", ""),
        }
        dc = t.get("date_closed")
        if dc and int(dc) >= cutoff_ms:
            recently_completed.append({
                **base,
                "closed": datetime.fromtimestamp(int(dc) / 1000, tz=timezone.utc).strftime("%Y-%m-%d"),
            })
            continue
        if dc:
            continue  # closed before the 7-day window — not relevant to any bucket
        if status in DONE_STATUSES:
            continue  # effectively done even though date_closed is unset

        due_ms = t.get("due_date")
        if not due_ms:
            no_due.append({**base, "due": None})
        else:
            due_dt = datetime.fromtimestamp(int(due_ms) / 1000, tz=timezone.utc)
            if due_dt < now:
                overdue.append({**base, "due": due_dt.strftime("%Y-%m-%d"), "days_overdue": (now - due_dt).days})
            else:
                assigned.append({**base, "due": due_dt.strftime("%Y-%m-%d")})

    overdue.sort(key=lambda r: r["days_overdue"], reverse=True)
    assigned.sort(key=lambda r: r["due"])
    recently_completed.sort(key=lambda r: r["closed"], reverse=True)

    log(f"  Overdue: {len(overdue)}, No due date: {len(no_due)}, Assigned: {len(assigned)}, Recently completed: {len(recently_completed)}")
    return {
        "generated_at": now.isoformat(),
        "overdue": overdue,
        "no_due_date": no_due,
        "assigned": assigned,
        "recently_completed": recently_completed,
    }


def fetch_clickup_pipeline():
    """Count tasks by status across all SA content lists."""
    if not CU_API_KEY:
        log("  Skipping ClickUp — CLICKUP_API_KEY not set")
        return None

    log("Fetching ClickUp content pipeline…")
    STATUS_GROUPS = {
        "not_started": ["to do", "open", "not started", "backlog"],
        "in_progress":  ["in progress", "writing", "drafting", "in review", "to review", "qa"],
        "needs_review": ["review", "needs review", "client review", "revisions"],
        "completed":    ["complete", "done", "published", "approved"],
    }

    summary = {"not_begun": 0, "in_progress": 0, "needs_review": 0, "completed": 0, "total": 0}
    recent_tasks = []

    for list_name, list_id in CLICKUP_LISTS.items():
        data, err = cu_get(f"/list/{list_id}/task", {
            "include_closed": "true",
            "page": 0,
            "order_by": "updated",
            "reverse": "true",
        })
        if err:
            log(f"  ClickUp list '{list_name}': {err}")
            continue

        tasks = data.get("tasks", [])
        log(f"  {list_name}: {len(tasks)} tasks")
        for task in tasks:
            status_name = (task.get("status", {}).get("status") or "").lower()
            summary["total"] += 1
            bucket = "not_begun"
            for key, names in STATUS_GROUPS.items():
                if any(n in status_name for n in names):
                    bucket = key
                    break
            summary[bucket] = summary.get(bucket, 0) + 1
            recent_tasks.append({
                "id": task.get("id"),
                "title": task.get("name", ""),
                "status": status_name.title(),
                "list": list_name,
                "updated": datetime.fromtimestamp(
                    int(task["date_updated"]) / 1000, tz=timezone.utc
                ).strftime("%Y-%m-%d") if task.get("date_updated") else "",
            })

    recent_tasks.sort(key=lambda t: t.get("updated", ""), reverse=True)
    return {
        "source": "clickup",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "articles": recent_tasks[:20],
    }



# ── Google Sheets scorecard ───────────────────────────────────────────────────

SHEETS_SCORECARD_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1gMOwOW54NYCoc2zxW3FQyH140xptUacRGWs1iDAgB8g/export?format=csv"
)
SHEETS_N_WEEKS = 6

# (sheet column B name, dashboard display name, group)
SCORECARD_METRIC_MAP = [
    ("Clicks",                  "Clicks",                "traffic"),
    ("Impressions",             "Impressions",           "traffic"),
    ("Traffic (GA4)",           "Traffic GA4",           "traffic"),
    ("Organic Trials",          "Organic Trials",        "pipeline"),
    ("Organic Accounts",        "Organic Accounts",      "pipeline"),
    ("New Content Published",   "New Content Published", "pipeline"),
    ("LLM Clicks",              "LLM Clicks",            "llm"),
    ("LLM Trials",              "LLM Trials",            "llm"),
    ("Clicks Branded",          "Clicks Branded",        "branded"),
    ("Impressions Branded",     "Impressions Branded",   "branded"),
    ("Clicks Non-Branded",      "Clicks Non-Branded",    "branded"),
    ("Impressions Non-Branded", "Impressions Non-Branded", "branded"),
]


def _parse_sheet_num(v):
    """Parse a number from the scorecard CSV. Handles European format (4.105,00 → 4105)."""
    if not v:
        return None
    v = v.strip().strip('"')
    if v in ("", "-", "—", "N/A"):
        return None
    if "," in v and "." in v:
        # European: period = thousands sep, comma = decimal  →  4.119.950,00
        v = v.replace(".", "").replace(",", ".")
    elif "," in v:
        # Comma as decimal only  →  4232,00
        v = v.replace(",", ".")
    try:
        f = float(v)
        return int(f) if f == int(f) else round(f, 2)
    except ValueError:
        return None


def fetch_sheets_weekly_metrics(n_weeks=SHEETS_N_WEEKS):
    """Pull the last N weeks of scorecard data from the public Google Sheet."""
    import io
    import csv as csv_mod
    import urllib.request

    log("Fetching weekly scorecard from Google Sheets…")
    try:
        req = urllib.request.Request(
            SHEETS_SCORECARD_URL,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            content = r.read().decode("utf-8")
    except Exception as e:
        log(f"  Sheets fetch failed: {e}")
        return None

    rows = list(csv_mod.reader(io.StringIO(content)))

    # Find the "Date Range >" header row and the "EOS Date >" row
    date_range_row = None
    eos_date_row   = None
    data_start_col = 5   # default column where weekly data begins

    for row in rows:
        row_str = ",".join(row)
        if "Date Range" in row_str and date_range_row is None:
            date_range_row = row
            for ci, cell in enumerate(row):
                if "Date Range" in cell:
                    data_start_col = ci + 1
                    break
        if "EOS Date" in row_str and eos_date_row is None:
            eos_date_row = row
        if date_range_row and eos_date_row:
            break

    if date_range_row is None:
        log("  Sheets: 'Date Range' header row not found — using col 5 default")

    # Collect raw weekly values for each metric
    metric_data: dict = {}
    for row in rows:
        if len(row) <= data_start_col:
            continue
        name = row[1].strip() if len(row) > 1 else ""
        for sheet_name, _, _ in SCORECARD_METRIC_MAP:
            if name == sheet_name and sheet_name not in metric_data:
                metric_data[sheet_name] = row[data_start_col:]
                break

    if not metric_data:
        log("  Sheets: no metric rows found in CSV")
        return None

    # Use Clicks to find last N filled weeks
    reference = metric_data.get("Clicks", next(iter(metric_data.values())))
    filled = [i for i, v in enumerate(reference) if _parse_sheet_num(v) is not None]
    if not filled:
        log("  Sheets: no filled weeks found")
        return None

    selected = filled[-n_weeks:]          # oldest → newest indices
    selected_rev = list(reversed(selected))  # newest → oldest (for display)

    # Build human-readable week labels: "Jun 8-14"
    week_labels = []
    for idx in selected_rev:
        col = data_start_col + idx
        label = None
        if eos_date_row and col < len(eos_date_row):
            eos = eos_date_row[col].strip()   # e.g. "Jun-10"
            month = eos.split("-")[0] if "-" in eos else ""
            if date_range_row and col < len(date_range_row):
                dr = date_range_row[col].strip().replace(" ", "")  # "8-14"
                if month and dr:
                    label = f"{month} {dr}"
        if not label and date_range_row and col < len(date_range_row):
            label = date_range_row[col].strip()
        week_labels.append(label or f"Week {idx + 1}")

    # Build output rows
    out_rows = []
    for sheet_name, display_name, group in SCORECARD_METRIC_MAP:
        vals_raw = metric_data.get(sheet_name, [])
        values = [
            _parse_sheet_num(vals_raw[idx]) if idx < len(vals_raw) else None
            for idx in selected_rev
        ]
        out_rows.append({"metric": display_name, "group": group, "values": values})

    log(f"  Sheets: {len(selected)} weeks · {len(out_rows)} metrics")
    return {
        "source": "google_sheets",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "weeks": week_labels,
        "rows": out_rows,
    }


# ── Weighted content scorecard (Content Scoring Model) ─────────────────────────

WEIGHTED_SCORECARD_GID = "1917611627"
WEIGHTED_SCORECARD_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1IlrmXGJqHjiTtED0qu5QgnDRzD18kIW1kmBuRzZhcSI/export?format=csv"
    f"&gid={WEIGHTED_SCORECARD_GID}"
)

# Search Atlas Q2 totals live in column A (label) / column B (value).
_SA_TOTAL_LABELS = ["SEO Content (weighted)", "SEO Briefs", "Other Projects", "Landing Pages"]
_MONTH_ABBR = {
    "jan": "Jan", "feb": "Feb", "mar": "Mar", "apr": "Apr", "april": "Apr",
    "may": "May", "jun": "Jun", "june": "Jun", "jul": "Jul", "aug": "Aug",
    "sep": "Sep", "sept": "Sep", "oct": "Oct", "nov": "Nov", "dec": "Dec",
}


def fetch_weighted_content_scorecard():
    """Pull the live weighted Content Scoring Model (Total SA vs 360 goal + weekly series)."""
    import io
    import csv as csv_mod
    import urllib.request

    log("Fetching weighted content scorecard (Content Scoring Model)…")
    try:
        req = urllib.request.Request(WEIGHTED_SCORECARD_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            content = r.read().decode("utf-8")
    except Exception as e:
        log(f"  Weighted scorecard fetch failed: {e}")
        return None

    rows = list(csv_mod.reader(io.StringIO(content)))

    def cell(row, i):
        return row[i].strip().strip('"') if len(row) > i else ""

    # Search Atlas Q2 totals: col A label, col B value
    breakdown, total = [], None
    for row in rows:
        label = cell(row, 0)
        if label in _SA_TOTAL_LABELS:
            v = _parse_sheet_num(cell(row, 1))
            if v is not None:
                breakdown.append({"label": label, "value": v})
        elif label == "Total SA":
            total = _parse_sheet_num(cell(row, 1))

    # Goal / Current Completion / Missing / Over live in col G (label) / col H (value)
    goal = current = missing = over = None
    for row in rows:
        key = cell(row, 6).rstrip(":").strip()
        val = _parse_sheet_num(cell(row, 7))
        if key == "Goal":
            goal = val
        elif key == "Current Completion":
            current = val
        elif key == "Missing":
            missing = val
        elif key == "Over":
            over = val

    if current is None:
        current = total

    # Weekly "Sum for SAG" series — find the "Owner" header row and the month row above it
    owner_idx = next((i for i, row in enumerate(rows) if cell(row, 0) == "Owner"), None)
    weekly = []
    if owner_idx is not None:
        header = rows[owner_idx]
        month_row = rows[owner_idx - 1] if owner_idx > 0 else []
        sum_row = next((row for row in rows if cell(row, 0).startswith("Sum for")), None)

        cur_month = ""
        for ci in range(1, len(header)):
            rng = cell(header, ci)
            if not rng:
                continue
            m = cell(month_row, ci) if month_row else ""
            if m:
                cur_month = _MONTH_ABBR.get(m.strip().lower(), m.strip())
            pts = _parse_sheet_num(cell(sum_row, ci)) if sum_row else None
            label = f"{cur_month} {rng.replace(' ', '')}".strip()
            weekly.append({"week": label, "points": pts})

    filled = [w for w in weekly if w["points"] is not None]
    latest = filled[-1] if filled else None

    if total is None and current is None and not weekly:
        log("  Weighted scorecard: no parseable data")
        return None

    log(f"  Weighted: Total SA={total} / goal {goal} (over {over}); latest week "
        f"{latest['week'] if latest else 'n/a'}={latest['points'] if latest else 'n/a'}")
    return {
        "source": "google_sheets",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scorecard_url": WEIGHTED_SCORECARD_URL.split("/export")[0] + "/edit",
        "quarter": "q2" if goal == 360 else ("q3" if goal == 420 else None),
        "goal": goal,
        "current": current,
        "total": total,
        "missing": missing,
        "over": over,
        "pct": round(current / goal * 100, 1) if (current and goal) else None,
        "breakdown": breakdown,
        "weekly": weekly,
        "latest_week": latest,
    }


def fetch_quota():
    """Pull platform credit usage from SearchAtlas."""
    log("Fetching SA quota…")
    data, err = sa_get("/account/quota/")
    if err:
        log(f"  Quota error: {err}")
        return {"alerts": [], "highlights": []}

    items = data.get("items") or data.get("result", {}).get("items") or []

    HIGHLIGHT_RESOURCES = {
        "Ai Content Generation":       "AI Content Generation",
        "Ai Premium Content Generation": "AI Premium Generation",
        "Competitor Research Projects": "Competitor Research",
        "Max Keyword Lookups":          "Keyword Lookups",
        "Otto Projects":                "OTTO Projects",
        "Projects":                     "LLMV Projects",   # LLMV
    }

    alerts = []
    highlights = []
    seen = set()

    for item in items:
        resource = item.get("resource") or ""
        warning  = item.get("warning") or ""
        total    = item.get("total") or 0
        consumed = item.get("consumed") or 0
        remaining = item.get("remaining") or 0
        usage_pct = item.get("usage_pct") or 0

        if warning and "EXHAUSTED" in warning.upper():
            alerts.append({
                "resource": resource,
                "status": "exhausted",
                "pct": usage_pct,
                "app": item.get("app"),
            })

        label = HIGHLIGHT_RESOURCES.get(resource)
        if label and label not in seen:
            seen.add(label)
            highlights.append({
                "resource": label,
                "consumed": consumed,
                "remaining": remaining,
                "total": total,
                "pct": round(usage_pct, 1),
            })

    log(f"  Quota: {len(alerts)} alerts, {len(highlights)} highlights")
    return {"alerts": alerts, "highlights": highlights}


def scan_local_fs():
    """Count drafts and clients from the filesystem."""
    log("Scanning local filesystem…")
    if not CLIENTS_DIR.exists():
        return {}

    clients = sorted(
        d.name for d in CLIENTS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )
    draft_count = sum(1 for _ in CLIENTS_DIR.rglob("*.md")
                      if "/drafts/" in str(_).replace("\\", "/"))
    brief_count = sum(1 for _ in CLIENTS_DIR.rglob("brief.md"))

    log(f"  Clients: {len(clients)}, drafts: {draft_count}, briefs: {brief_count}")
    return {
        "active_clients": len(clients),
        "total_drafts":   draft_count,
        "active_briefs":  brief_count,
        "clients":        clients,
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    global DEBUG
    parser = argparse.ArgumentParser(description="Generate dashboard data.json")
    parser.add_argument("--debug", action="store_true", help="Verbose output")
    parser.add_argument("--output", default=str(OUTPUT_FILE), help="Output file path")
    args = parser.parse_args()
    DEBUG = args.debug

    log("Starting data generation…")
    sources_status = {}

    # Read existing data.json early — merge strategy preserves sections that fail.
    out_path = Path(args.output)
    existing = {}
    if out_path.exists():
        try:
            with open(out_path) as f:
                existing = json.load(f)
        except Exception:
            pass

    # Build slug lookup from existing content_performance + content_decay
    # so auto-generated slugs stay human-readable across runs.
    slug_lookup: dict = {}
    for entry in (existing.get("content_performance") or {}).get("top_pages", []):
        if entry.get("page") and entry.get("slug"):
            slug_lookup[entry["page"]] = entry["slug"]
    for entry in (existing.get("content_performance") or {}).get("climbing", []):
        if entry.get("page") and entry.get("slug"):
            slug_lookup[entry["page"]] = entry["slug"]
    for entry in (existing.get("content_decay") or []):
        if entry.get("page") and entry.get("slug"):
            slug_lookup[entry["page"]] = entry["slug"]

    # ── GSC (Google OAuth direct) ────────────────────────────────────────────
    gsc_auth = _load_gsc_auth()
    gsc = gsc_perf = gsc_decay = gsc_wins = None
    if gsc_auth:
        gsc      = fetch_gsc(gsc_auth)
        gsc_perf = fetch_gsc_content_performance(gsc_auth, slug_lookup)
        gsc_decay = fetch_gsc_decay(gsc_auth, slug_lookup)
        gsc_wins  = fetch_gsc_quick_wins(gsc_auth)
        if gsc:
            split = fetch_gsc_branded_split(
                gsc_auth,
                total_cur   = gsc["current"]["clicks"],
                total_prior = gsc["prior"]["clicks"],
            )
            if split:
                gsc["branded_split"] = split
        sources_status["gsc"] = "connected" if gsc else "error"
    else:
        log("  GSC token not found — skipping (existing data preserved)")
        sources_status["gsc"] = "token_not_found"

    # ── ClickUp ──────────────────────────────────────────────────────────────
    clickup_stats = None
    if CU_API_KEY:
        clickup_stats = fetch_clickup_articles_published(days=7)
        sources_status["clickup_published"] = "connected" if clickup_stats else "error"
    else:
        sources_status["clickup_published"] = "api_key_required"

    clickup_tasks = None
    if CU_API_KEY:
        clickup_tasks = fetch_clickup_task_buckets()
        sources_status["clickup_tasks"] = "connected" if clickup_tasks else "error"
    else:
        sources_status["clickup_tasks"] = "api_key_required"

    pipeline = None
    if CU_API_KEY:
        pipeline = fetch_clickup_pipeline()
        sources_status["clickup"] = "connected" if pipeline else "error"
        sources_status["contentgenius"] = "skipped"
    else:
        sources_status["clickup"] = "api_key_required"

    if not pipeline and SA_API_KEY:
        pipeline = fetch_contentgenius()
        sources_status["contentgenius"] = "connected" if pipeline else "error"
    elif not pipeline and not SA_API_KEY:
        sources_status["contentgenius"] = "api_key_required"

    # ── Google Sheets scorecard ──────────────────────────────────────────────
    sheets_wm = fetch_sheets_weekly_metrics()
    if sheets_wm:
        existing["weekly_metrics"] = sheets_wm
        sources_status["sheets_scorecard"] = "connected"
    else:
        sources_status["sheets_scorecard"] = "error"

    # ── Weighted content scorecard (Content Scoring Model) ───────────────────
    weighted = fetch_weighted_content_scorecard()
    if weighted:
        existing["weighted_content"] = weighted
        sources_status["weighted_scorecard"] = "connected"
    else:
        sources_status["weighted_scorecard"] = "error"

    # ── SA quota ─────────────────────────────────────────────────────────────
    credits = {"alerts": [], "highlights": []}
    if SA_API_KEY:
        credits = fetch_quota()

    # ── Local filesystem ─────────────────────────────────────────────────────
    local = scan_local_fs()
    sources_status["local_fs"] = "connected" if local else "error"

    # ── Merge ────────────────────────────────────────────────────────────────
    existing["meta"] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "2.2.0",
        "sources": {**existing.get("meta", {}).get("sources", {}), **sources_status},
    }
    if gsc is not None:
        existing["gsc"] = gsc
    if gsc_perf is not None:
        existing["content_performance"] = gsc_perf
    if gsc_decay is not None:
        existing["content_decay"] = gsc_decay
    if gsc_wins is not None:
        existing["quick_wins"] = gsc_wins
    if clickup_stats is not None:
        existing["clickup_stats"] = clickup_stats
    if clickup_tasks is not None:
        existing["clickup_tasks"] = clickup_tasks
    if pipeline is not None:
        existing["content_pipeline"] = pipeline
    if local:
        existing["local_stats"] = local
    if credits.get("alerts") or credits.get("highlights"):
        existing["platform_credits"] = credits

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(existing, f, indent=2, default=str)

    log(f"Written to {out_path}")
    log("Done.")


if __name__ == "__main__":
    main()
