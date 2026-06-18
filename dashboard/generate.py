#!/usr/bin/env python3
"""
Dashboard data generator.

Pulls from:
  - SearchAtlas API  (SEARCHATLAS_API_KEY)  — ContentGenius articles, GSC performance, quota
  - ClickUp API      (CLICKUP_API_KEY)       — content pipeline task counts

Writes:  dashboard/data.json

Run manually:     python dashboard/generate.py
Run with debug:   python dashboard/generate.py --debug
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

    for t in all_tasks:
        status = (t.get("status", {}) or {}).get("status", "")
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


def fetch_gsc():
    """Pull 28-day GSC performance vs prior 28-day period."""
    log("Fetching GSC performance…")
    today = datetime.now(timezone.utc).date()
    p_end   = today - timedelta(days=3)   # GSC typically lags 2-3 days
    p_start = p_end - timedelta(days=27)
    pp_end   = p_start - timedelta(days=1)
    pp_start = pp_end - timedelta(days=27)

    def pull(start, end):
        data, err = sa_get("/gsc/site-property-performance/", {
            "selected_property": GSC_PROPERTY,
            "period_start": str(start),
            "period_end": str(end),
            "limit": 5,
        })
        if err:
            log(f"  GSC error: {err}")
            return None
        return data

    current = pull(p_start, p_end)
    if not current:
        return None

    prior = pull(pp_start, pp_end)

    def extract_totals(d):
        if not d:
            return {}
        overview = d.get("overview") or {}
        rows = overview.get("rows", [])
        cols = overview.get("columns", [])
        if rows and cols:
            row = rows[0]
            return dict(zip(cols, row))
        return d.get("totals") or {}

    cur  = extract_totals(current)
    prev = extract_totals(prior) if prior else {}

    def delta(key):
        c = cur.get(key, 0) or 0
        p = prev.get(key, 0) or 0
        if not p:
            return None
        return round((c - p) / p * 100, 1)

    top_pages = []
    for section in (current.get("by_page") or []):
        cols = section.get("columns", [])
        for row in section.get("rows", [])[:5]:
            d = dict(zip(cols, row))
            top_pages.append({"page": d.get("page", ""), "clicks": d.get("clicks", 0)})

    log(f"  GSC: clicks={cur.get('clicks')}, impressions={cur.get('impressions')}")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period": f"{p_start} to {p_end}",
        "clicks":             cur.get("clicks"),
        "impressions":        cur.get("impressions"),
        "ctr":                round(float(cur.get("ctr") or 0) * 100, 2),
        "position":           round(float(cur.get("position") or 0), 1),
        "clicks_delta":       delta("clicks"),
        "impressions_delta":  delta("impressions"),
        "top_pages":          top_pages,
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

    # Articles published this week (primary new metric)
    clickup_stats = None
    if CU_API_KEY:
        clickup_stats = fetch_clickup_articles_published(days=7)
        sources_status["clickup_published"] = "connected" if clickup_stats else "error"
    else:
        sources_status["clickup_published"] = "api_key_required"

    # 4-category task buckets for the pillar-dashboard ClickUp section
    clickup_tasks = None
    if CU_API_KEY:
        clickup_tasks = fetch_clickup_task_buckets()
        sources_status["clickup_tasks"] = "connected" if clickup_tasks else "error"
    else:
        sources_status["clickup_tasks"] = "api_key_required"

    # ContentGenius pipeline (or ClickUp if key available)
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

    # GSC
    gsc = None
    if SA_API_KEY:
        gsc = fetch_gsc()
        sources_status["gsc"] = "connected" if gsc else "not_connected"
    else:
        sources_status["gsc"] = "api_key_required"

    # Quota
    credits = {"alerts": [], "highlights": []}
    if SA_API_KEY:
        credits = fetch_quota()

    # Local filesystem
    local = scan_local_fs()
    sources_status["local_fs"] = "connected" if local else "error"

    # Merge strategy: read existing data.json and only overwrite sections
    # that were successfully fetched. This preserves hand-crafted sections
    # (llm_visibility, content_decay, quick_wins) across runs.
    out_path = Path(args.output)
    existing = {}
    if out_path.exists():
        try:
            with open(out_path) as f:
                existing = json.load(f)
        except Exception:
            pass

    existing["meta"] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "2.1.0",
        "sources": {**existing.get("meta", {}).get("sources", {}), **sources_status},
    }
    if clickup_stats is not None:
        existing["clickup_stats"] = clickup_stats
    if clickup_tasks is not None:
        existing["clickup_tasks"] = clickup_tasks
    if pipeline is not None:
        existing["content_pipeline"] = pipeline
    if local:
        existing["local_stats"] = local
    if gsc is not None:
        existing["gsc"] = gsc
    if credits.get("alerts") or credits.get("highlights"):
        existing["platform_credits"] = credits

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(existing, f, indent=2, default=str)

    log(f"Written to {out_path}")
    log("Done.")


if __name__ == "__main__":
    main()
