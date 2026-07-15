#!/usr/bin/env python3
"""
Build the LinkGraph delivery dashboard.

Inputs:
    dashboard/delivery-registry.json  Editable owner/status/review metadata.
    clients/**/STYLE-SYSTEM.md        Client roots.
    clients/**/campaigns/**           Campaigns and pipeline run state.

Outputs:
    reports/linkgraph-delivery-dashboard.html
    reports/linkgraph-delivery-dashboard.json

Usage:
    python3 scripts/build-delivery-dashboard.py
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
REGISTRY_PATH = ROOT / "dashboard" / "delivery-registry.json"
REPORTS_DIR = ROOT / "reports"
HTML_REPORT = REPORTS_DIR / "linkgraph-delivery-dashboard.html"
JSON_REPORT = REPORTS_DIR / "linkgraph-delivery-dashboard.json"
INTAKE_TEMPLATE_SOURCE = ROOT / "content-production" / "weekly-intake" / "example-topics.csv"
INTAKE_TEMPLATE_REPORT = REPORTS_DIR / "weekly-intake-template.csv"

REQUIRED_PACK_ITEMS = {
    "style_system": ("STYLE-SYSTEM.md", "Style system"),
    "raw": ("raw", "Raw source folder"),
    "raw_knowledge": ("raw/knowledge", "Knowledge folder"),
    "deliverables": ("deliverables", "Deliverables folder"),
}

RECOMMENDED_PACK_ITEMS = {
    "compliance": ("COMPLIANCE.yml", "Compliance rules"),
    "delivery": ("delivery.yml", "Delivery config"),
    "approved": ("_approved", "Approved examples"),
    "page_templates": ("page-templates", "Page templates"),
    "campaigns": ("campaigns", "Legacy campaign folder"),
}

EXCLUDED_CLIENT_SLUGS = {"searchatlas"}

STATUS_ORDER = [
    "blocked",
    "revision",
    "client-review",
    "editorial-review",
    "qa",
    "drafting",
    "briefing",
    "approved",
    "delivered",
    "published",
    "paused",
    "ready",
]


@dataclass
class ClientSummary:
    slug: str
    display_name: str
    path: Path
    registry: dict[str, Any]
    readiness_score: int = 0
    readiness_status: str = "not-ready"
    missing_required: list[str] = field(default_factory=list)
    missing_recommended: list[str] = field(default_factory=list)
    campaigns: list[dict[str, Any]] = field(default_factory=list)
    runs: list[dict[str, Any]] = field(default_factory=list)
    monthly_deliverables: list[dict[str, Any]] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    inferred_status: str = "ready"
    website_intelligence: dict[str, Any] = field(default_factory=dict)

    @property
    def status(self) -> str:
        return str(self.registry.get("status") or self.inferred_status or "ready")

    @property
    def owner_label(self) -> str:
        writer = self.registry.get("writer") or "Unassigned writer"
        editor = self.registry.get("editor") or "Unassigned editor"
        csm = self.registry.get("csm") or "Unassigned CSM"
        return f"CSM/POC: {csm} / Editor: {editor} / Writer: {writer}"


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise SystemExit(f"Missing editable registry: {REGISTRY_PATH}")
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {REGISTRY_PATH}: {exc}") from exc
    data.setdefault("clients", {})
    return data


def client_slug_from_style_system(path: Path) -> str:
    return path.parent.relative_to(CLIENTS_DIR).as_posix()


def discover_clients(registry: dict[str, Any]) -> list[ClientSummary]:
    clients: dict[str, ClientSummary] = {}
    for style_path in sorted(CLIENTS_DIR.rglob("STYLE-SYSTEM.md")):
        if "/raw/" in style_path.as_posix():
            continue
        slug = client_slug_from_style_system(style_path)
        if slug in EXCLUDED_CLIENT_SLUGS:
            continue
        entry = dict(registry.get("clients", {}).get(slug, {}))
        display_name = entry.get("display_name") or slug.replace("/", " / ").replace("-", " ").title()
        clients[slug] = ClientSummary(
            slug=slug,
            display_name=display_name,
            path=style_path.parent,
            registry=entry,
        )

    # Keep registry-only clients visible so stale config is obvious.
    for slug, entry in sorted(registry.get("clients", {}).items()):
        if slug in EXCLUDED_CLIENT_SLUGS:
            continue
        if slug not in clients:
            client_path = CLIENTS_DIR / slug
            display_name = entry.get("display_name") or slug.replace("/", " / ").replace("-", " ").title()
            clients[slug] = ClientSummary(slug, display_name, client_path, dict(entry))

    return sorted(clients.values(), key=lambda client: client.display_name.lower())


def path_exists(client: ClientSummary, rel_path: str) -> bool:
    return (client.path / rel_path).exists()


def evaluate_readiness(client: ClientSummary) -> None:
    required_present = 0
    recommended_present = 0

    for rel_path, label in REQUIRED_PACK_ITEMS.values():
        if path_exists(client, rel_path):
            required_present += 1
        else:
            client.missing_required.append(label)

    for rel_path, label in RECOMMENDED_PACK_ITEMS.values():
        if path_exists(client, rel_path):
            recommended_present += 1
        else:
            client.missing_recommended.append(label)

    total = len(REQUIRED_PACK_ITEMS) + len(RECOMMENDED_PACK_ITEMS)
    client.readiness_score = round(((required_present + recommended_present) / total) * 100)
    if client.missing_required:
        client.readiness_status = "not-ready"
    elif client.missing_recommended:
        client.readiness_status = "partial"
    else:
        client.readiness_status = "ready"


def safe_read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def first_nonempty_line(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip("# \t")
            if line:
                return line[:160]
    except Exception:
        return ""
    return ""


def service_taxonomy_summary(client: ClientSummary) -> dict[str, Any]:
    taxonomy_path = client.path / "raw" / "knowledge" / "service-taxonomy.md"
    if not taxonomy_path.exists():
        return {"count": 0, "items": []}

    items: list[dict[str, str]] = []
    try:
        for line in taxonomy_path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if not stripped.startswith("- "):
                continue
            body = stripped[2:].strip()
            if not body or ":" not in body:
                continue
            name, description = body.split(":", 1)
            name = name.strip()
            description = description.strip()
            if name and description:
                items.append({"name": name[:90], "description": description[:220]})
    except Exception:
        return {"count": 0, "items": []}

    return {"count": len(items), "items": items[:7]}


def discover_campaigns_and_runs(client: ClientSummary) -> None:
    campaigns_dir = client.path / "campaigns"
    if campaigns_dir.exists():
        for campaign_dir in sorted(p for p in campaigns_dir.iterdir() if p.is_dir()):
            readme = campaign_dir / "README.md"
            campaign = {
                "slug": campaign_dir.name,
                "path": campaign_dir.relative_to(ROOT).as_posix(),
                "title": first_nonempty_line(readme) or campaign_dir.name,
                "has_readme": readme.exists(),
                "draft_count": count_files(campaign_dir / "drafts"),
                "final_count": count_files(campaign_dir / "final"),
                "html_count": count_files(campaign_dir / "html"),
            }
            client.campaigns.append(campaign)

            runs_dir = campaign_dir / "runs"
            if runs_dir.exists():
                for run_dir in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
                    run = summarize_run(run_dir, campaign_dir)
                    client.runs.append(run)
                    if run["blocked"]:
                        client.blockers.append(f"{campaign_dir.name}/{run_dir.name}")


def discover_monthly_deliverables(client: ClientSummary) -> None:
    deliverables_dir = client.path / "deliverables"
    if not deliverables_dir.exists():
        return
    for registry_path in sorted(deliverables_dir.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]/registry.json")):
        registry = safe_read_json(registry_path)
        items = registry.get("deliverables", [])
        if not isinstance(items, list):
            items = []
        status_counts: dict[str, int] = {}
        upload_counts: dict[str, int] = {}
        for item in items:
            status = str(item.get("status") or "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
            drive = item.get("google_drive") if isinstance(item.get("google_drive"), dict) else {}
            upload_status = str(drive.get("upload_status") or "not-staged")
            upload_counts[upload_status] = upload_counts.get(upload_status, 0) + 1
        client.monthly_deliverables.append(
            {
                "month": registry.get("month") or registry_path.parent.name,
                "path": registry_path.relative_to(ROOT).as_posix(),
                "deliverable_count": len(items),
                "status_counts": status_counts,
                "google_drive": registry.get("google_drive", {}),
                "upload_counts": upload_counts,
            }
        )


def load_website_intelligence(client: ClientSummary) -> None:
    intel_path = client.path / "raw" / "research" / "website-intelligence.json"
    if intel_path.exists():
        client.website_intelligence = safe_read_json(intel_path)
    else:
        client.website_intelligence = {
            "status": "missing",
            "website_urls": [],
            "sitemaps": [],
            "url_count": 0,
            "product_or_service_urls": [],
            "top_terms": [],
            "blockers": ["Run python3 scripts/crawl-client-websites.py to collect website intelligence."],
        }


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for p in path.rglob("*") if p.is_file() and not p.name.startswith("."))


def summarize_run(run_dir: Path, campaign_dir: Path) -> dict[str, Any]:
    state = safe_read_json(run_dir / "state.json")
    blocked_path = run_dir / "BLOCKED.md"
    summary_path = run_dir / "RUN-SUMMARY.md"
    html_files = sorted(run_dir.glob("*.html"))
    md_files = sorted(run_dir.glob("*.md"))
    status = state.get("status") or state.get("stage") or ""
    if blocked_path.exists():
        status = "blocked"
    elif html_files:
        status = status or "rendered"
    elif summary_path.exists():
        status = status or "qa"
    else:
        status = status or "drafting"
    return {
        "slug": run_dir.name,
        "campaign": campaign_dir.name,
        "path": run_dir.relative_to(ROOT).as_posix(),
        "status": status,
        "blocked": blocked_path.exists(),
        "summary": first_nonempty_line(summary_path),
        "html_count": len(html_files),
        "md_count": len(md_files),
    }


def infer_client_status(client: ClientSummary) -> None:
    if client.registry.get("blocker") or client.blockers:
        client.inferred_status = "blocked"
        return
    if client.runs:
        statuses = {str(run["status"]) for run in client.runs}
        if "blocked" in statuses:
            client.inferred_status = "blocked"
        elif any(status in statuses for status in ("rendered", "ready", "complete", "done")):
            client.inferred_status = "qa"
        else:
            client.inferred_status = "drafting"
        return
    if client.campaigns:
        client.inferred_status = "briefing"
        return
    if client.readiness_status == "not-ready":
        client.inferred_status = "blocked"
        return
    client.inferred_status = "ready"


def build_report(registry: dict[str, Any]) -> dict[str, Any]:
    clients = discover_clients(registry)
    for client in clients:
        evaluate_readiness(client)
        discover_campaigns_and_runs(client)
        discover_monthly_deliverables(client)
        load_website_intelligence(client)
        infer_client_status(client)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "client_count": len(clients),
        "ready_count": sum(1 for c in clients if c.readiness_status == "ready"),
        "partial_count": sum(1 for c in clients if c.readiness_status == "partial"),
        "not_ready_count": sum(1 for c in clients if c.readiness_status == "not-ready"),
        "blocked_count": sum(1 for c in clients if c.status == "blocked"),
        "campaign_count": sum(len(c.campaigns) for c in clients),
        "run_count": sum(len(c.runs) for c in clients),
        "monthly_deliverable_count": sum(
            month["deliverable_count"] for c in clients for month in c.monthly_deliverables
        ),
        "monthly_registry_count": sum(len(c.monthly_deliverables) for c in clients),
        "website_intel_count": sum(1 for c in clients if c.website_intelligence.get("status") not in {"", "missing"}),
        "urgent_automation_count": sum(1 for c in clients if c.registry.get("automation_priority") == 1),
        "missing_owner_count": sum(1 for c in clients if not c.registry.get("csm")),
    }
    return {
        "summary": summary,
        "clients": [client_to_dict(client) for client in clients],
        "editable_registry": REGISTRY_PATH.relative_to(ROOT).as_posix(),
    }


def client_to_dict(client: ClientSummary) -> dict[str, Any]:
    return {
        "slug": client.slug,
        "display_name": client.display_name,
        "path": client.path.relative_to(ROOT).as_posix() if client.path.exists() else client.path.as_posix(),
        "status": client.status,
        "inferred_status": client.inferred_status,
        "priority": client.registry.get("priority") or "standard",
        "automation_priority": client.registry.get("automation_priority") or "",
        "active_monthly_volume": client.registry.get("active_monthly_volume") or "",
        "brand_voice": client.registry.get("brand_voice") or "",
        "risk_flags": client.registry.get("risk_flags") or "",
        "owner_label": client.owner_label,
        "writer": client.registry.get("writer") or "",
        "editor": client.registry.get("editor") or "",
        "csm": client.registry.get("csm") or "",
        "next_action": client.registry.get("next_action") or "",
        "blocker": client.registry.get("blocker") or "",
        "review_url": client.registry.get("review_url") or "",
        "delivery_url": client.registry.get("delivery_url") or "",
        "notes": client.registry.get("notes") or "",
        "readiness_score": client.readiness_score,
        "readiness_status": client.readiness_status,
        "missing_required": client.missing_required,
        "missing_recommended": client.missing_recommended,
        "campaigns": client.campaigns,
        "runs": client.runs,
        "monthly_deliverables": client.monthly_deliverables,
        "blockers": client.blockers,
        "service_taxonomy": service_taxonomy_summary(client),
        "website_intelligence": {
            "status": client.website_intelligence.get("status", "missing"),
            "website_urls": client.website_intelligence.get("website_urls", []),
            "sitemap_count": len(client.website_intelligence.get("sitemaps", [])),
            "url_count": client.website_intelligence.get("url_count", 0),
            "product_or_service_count": len(client.website_intelligence.get("product_or_service_urls", [])),
            "top_terms": client.website_intelligence.get("top_terms", [])[:12],
            "blockers": client.website_intelligence.get("blockers", []),
        },
    }


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def status_class(status: str) -> str:
    normalized = status.lower().replace("_", "-")
    if normalized in {"blocked", "not-ready"}:
        return "danger"
    if normalized in {"revision", "client-review", "editorial-review", "qa", "partial"}:
        return "warn"
    if normalized in {"approved", "delivered", "published", "ready"}:
        return "good"
    return "neutral"


def sort_clients_for_dashboard(clients: list[dict[str, Any]]) -> list[dict[str, Any]]:
    order = {status: index for index, status in enumerate(STATUS_ORDER)}
    return sorted(
        clients,
        key=lambda client: (
            int(client.get("automation_priority") or 9),
            order.get(str(client["status"]), 99),
            -(client["readiness_score"]),
            client["display_name"].lower(),
        ),
    )


def render_html(report: dict[str, Any]) -> str:
    summary = report["summary"]
    clients = sort_clients_for_dashboard(report["clients"])
    cards = "\n".join(render_client_card(client) for client in clients)
    rows = "\n".join(render_client_row(client) for client in clients)
    empty_queue = render_monthly_queue_notice(summary)
    generated = summary["generated_at"].replace("T", " ").replace("+00:00", " UTC")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LinkGraph Delivery Dashboard</title>
  <style>
    :root {{
      --bg: #f4f6fa;
      --ink: #162033;
      --muted: #617087;
      --line: #dce3ee;
      --panel: #ffffff;
      --navy: #12385d;
      --blue: #2458c2;
      --orange: #f47a2a;
      --green: #257350;
      --yellow: #9a6a00;
      --red: #b2463d;
      --chip: #edf1f7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--bg);
      line-height: 1.45;
    }}
    .shell {{
      width: min(1440px, calc(100% - 48px));
      margin: 0 auto;
    }}
    header {{
      padding: 22px 0 18px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}
    .topline {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--navy);
      font-weight: 800;
      letter-spacing: 0;
    }}
    .mark {{
      width: 34px;
      height: 34px;
      border-radius: 8px;
      background: var(--navy);
      color: #fff;
      display: grid;
      place-items: center;
      font-size: 18px;
      line-height: 1;
      border-bottom: 4px solid var(--orange);
    }}
    h1 {{
      margin: 18px 0 6px;
      font-size: clamp(30px, 4vw, 52px);
      line-height: 1.04;
      letter-spacing: 0;
      color: var(--ink);
    }}
    .subhead {{
      margin: 0;
      color: var(--muted);
      max-width: 860px;
      font-size: 16px;
    }}
    .header-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .button {{
      display: inline-flex;
      align-items: center;
      min-height: 38px;
      padding: 8px 12px;
      border-radius: 8px;
      background: var(--navy);
      color: #fff;
      text-decoration: none;
      font-weight: 700;
      font-size: 13px;
    }}
    .button.secondary {{
      background: #eef3fb;
      color: var(--navy);
      border: 1px solid var(--line);
    }}
    .button:hover {{ text-decoration: none; }}
    main {{
      padding: 24px 0 44px;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(360px, .95fr);
      gap: 16px;
      align-items: stretch;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 10px 28px rgba(18, 56, 93, .06);
    }}
    .workflow {{
      padding: 18px;
    }}
    .section-kicker {{
      margin: 0 0 6px;
      color: var(--orange);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .06em;
    }}
    h2 {{
      margin: 0;
      font-size: 22px;
      line-height: 1.16;
      letter-spacing: 0;
    }}
    .lede {{
      margin: 8px 0 0;
      color: var(--muted);
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    .stat {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}
    .stat strong {{
      display: block;
      font-size: 28px;
      line-height: 1;
      color: var(--navy);
    }}
    .stat span {{
      color: var(--muted);
      font-size: 13px;
    }}
    .command-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 16px;
    }}
    .command {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fbfcff;
    }}
    .command-number {{
      width: 28px;
      height: 28px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      background: var(--navy);
      color: #fff;
      font-weight: 800;
      margin-bottom: 10px;
    }}
    .command h3 {{
      margin: 0 0 6px;
      font-size: 16px;
      letter-spacing: 0;
    }}
    .command p {{
      margin: 0 0 10px;
      color: var(--muted);
      font-size: 13px;
    }}
    code {{
      display: inline-block;
      max-width: 100%;
      padding: 2px 5px;
      border-radius: 5px;
      background: #edf1f7;
      color: #263449;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
      white-space: normal;
    }}
    .empty-state {{
      margin-top: 16px;
      padding: 16px;
      border: 1px dashed #f0a269;
      border-radius: 8px;
      background: #fff7f0;
    }}
    .empty-state strong {{
      display: block;
      margin-bottom: 4px;
      color: #7c421c;
    }}
    .section-header {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 16px;
      margin: 28px 0 12px;
    }}
    .section-header p {{
      margin: 6px 0 0;
      color: var(--muted);
      max-width: 780px;
    }}
    .client-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}
    .client-card {{
      padding: 16px;
      min-height: 320px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .card-head {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: flex-start;
    }}
    .client-name {{
      font-weight: 800;
      font-size: 18px;
      color: var(--ink);
    }}
    .path {{
      color: var(--muted);
      font-size: 12px;
      margin-top: 3px;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border-radius: 999px;
      background: var(--chip);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }}
    .chip.good {{ color: var(--green); background: #e5f3ec; }}
    .chip.warn {{ color: var(--yellow); background: #fff3cf; }}
    .chip.danger {{ color: var(--red); background: #fae5e2; }}
    .chip.neutral {{ color: var(--blue); background: #e7eefc; }}
    .label {{
      margin: 0 0 4px;
      font-size: 11px;
      color: var(--muted);
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .05em;
    }}
    .value {{
      margin: 0;
      color: var(--ink);
      font-size: 14px;
    }}
    .small {{ color: var(--muted); font-size: 12px; }}
    .metric-row {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin-top: auto;
    }}
    .metric {{
      padding: 9px;
      border-radius: 8px;
      background: #f4f7fb;
      border: 1px solid #e6edf6;
    }}
    .metric strong {{
      display: block;
      color: var(--navy);
      font-size: 18px;
      line-height: 1;
    }}
    .risk-block {{
      padding: 10px;
      border-radius: 8px;
      background: #fff7f0;
      border: 1px solid #f0cfb5;
    }}
    .link-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .text-link {{
      color: var(--blue);
      font-size: 13px;
      font-weight: 800;
      text-decoration: none;
    }}
    .text-link:hover {{ text-decoration: underline; }}
    .ops-table {{
      overflow: hidden;
    }}
    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
    }}
    th, td {{
      padding: 11px 12px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      font-size: 13px;
    }}
    th {{
      background: #eef3fb;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: #3d4047;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    .missing {{ margin: 6px 0 0; padding-left: 18px; }}
    .missing li {{ margin: 2px 0; }}
    a {{ color: var(--blue); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .footer-note {{
      margin-top: 18px;
      color: var(--muted);
      font-size: 13px;
    }}
    .footer-note code {{ margin: 0 2px; }}
    @media (max-width: 900px) {{
      .shell {{ width: min(100% - 28px, 1440px); }}
      .topline, .section-header {{ align-items: flex-start; flex-direction: column; }}
      .hero-grid, .command-grid, .client-grid {{ grid-template-columns: 1fr; }}
      .stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      table, thead, tbody, th, td, tr {{ display: block; }}
      thead {{ display: none; }}
      tr {{ border-bottom: 1px solid var(--line); }}
      td {{ border-bottom: 0; padding: 8px 12px; }}
      td::before {{
        content: attr(data-label);
        display: block;
        color: var(--muted);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: .04em;
        margin-bottom: 2px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="shell">
      <div class="topline">
        <div class="brand"><span class="mark">L</span><span>LinkGraph Content Ops</span></div>
        <div class="header-actions">
          <a class="button secondary" href="client-context-dashboard/index.html">Client Context</a>
          <a class="button" href="weekly-intake-template.csv">Intake CSV</a>
        </div>
      </div>
      <h1>Delivery Command Center</h1>
      <p class="subhead">A working surface for weekly topic intake, client context, monthly production, review, and Google Drive handoff. Generated from client folders, monthly registries, website intelligence, and <code>{esc(report["editable_registry"])}</code>.</p>
    </div>
  </header>
  <main class="shell">
    <section class="hero-grid">
      <div class="panel workflow">
        <p class="section-kicker">Weekly production flow</p>
        <h2>Move topics from intake to finished client folders without losing context.</h2>
        <p class="lede">Every client should have a context pack, a monthly deliverables registry, and a Drive-ready export. The dashboard should show what exists, what is waiting, and where the next action belongs.</p>
        <div class="command-grid">
          {render_command_tile("1", "Import weekly intake", "Drop the week&apos;s topics and keywords into the intake CSV, then create client/month deliverable registries.", "python3 scripts/import-weekly-intake.py content-production/weekly-intake/YYYY-MM-DD/topics.csv")}
          {render_command_tile("2", "Produce in context", "Use each client page for voice, offerings, topical terms, source rules, and no-slop writing constraints before drafting.", "reports/client-context-dashboard/index.html")}
          {render_command_tile("3", "Export to Drive", "Package the month into a Google Drive-ready folder with client subfolders, manifests, and status summaries.", "python3 scripts/build-google-drive-export.py --month YYYY-MM")}
        </div>
        {empty_queue}
      </div>
      <div class="stats">
        <div class="stat"><strong>{summary["client_count"]}</strong><span>client accounts tracked</span></div>
        <div class="stat"><strong>{summary["urgent_automation_count"]}</strong><span>urgent automation clients</span></div>
        <div class="stat"><strong>{summary["missing_owner_count"]}</strong><span>missing CSM / POC</span></div>
        <div class="stat"><strong>{summary["website_intel_count"]}</strong><span>website intelligence packs</span></div>
        <div class="stat"><strong>{summary["monthly_deliverable_count"]}</strong><span>monthly deliverables queued</span></div>
        <div class="stat"><strong>{summary["blocked_count"]}</strong><span>clients needing attention</span></div>
      </div>
    </section>

    <section>
      <div class="section-header">
        <div>
          <p class="section-kicker">Client workspaces</p>
          <h2>Context, queue, and handoff state by client</h2>
          <p>Use these cards as the starting point for production. The client context link is where writers should check style, services, products, topical map, and compliance constraints before drafting.</p>
        </div>
      </div>
      <div class="client-grid">
        {cards}
      </div>
    </section>

    <section>
      <div class="section-header">
        <div>
          <p class="section-kicker">Operations table</p>
          <h2>Scan view</h2>
          <p>Compact status view for owners, setup gaps, website crawl state, and next actions. Edit the registry instead of editing this generated HTML.</p>
        </div>
      </div>
      <div class="panel ops-table">
        <table>
          <thead>
            <tr>
              <th>Client</th>
              <th>Automation</th>
              <th>Status</th>
              <th>Context Pack</th>
              <th>Website Intel</th>
              <th>Owners</th>
              <th>Monthly Work</th>
              <th>Next Action</th>
              <th>Context</th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </div>
    </section>
    <p class="footer-note">Last generated {esc(generated)}. Refresh website context with <code>python3 scripts/crawl-client-websites.py</code>, then rebuild with <code>python3 scripts/build-delivery-dashboard.py</code>.</p>
  </main>
</body>
</html>
"""


def render_command_tile(number: str, title: str, body: str, command: str) -> str:
    return f"""
          <div class="command">
            <div class="command-number">{esc(number)}</div>
            <h3>{esc(title)}</h3>
            <p>{body}</p>
            <code>{esc(command)}</code>
          </div>"""


def render_monthly_queue_notice(summary: dict[str, Any]) -> str:
    if summary.get("monthly_deliverable_count", 0) > 0:
        return ""
    return """
        <div class="empty-state">
          <strong>No weekly intake has been imported yet.</strong>
          Add the week&apos;s topics and keywords to <code>content-production/weekly-intake/YYYY-MM-DD/topics.csv</code>, then run the import command above. That creates each client&apos;s monthly registry and deliverable placeholders.
        </div>"""


def context_page_href(slug: str) -> str:
    return f"client-context-dashboard/{slug.replace('/', '__')}.html"


def has_context_page(slug: str) -> bool:
    return (REPORTS_DIR / context_page_href(slug)).exists()


def context_link_html(client: dict[str, Any]) -> str:
    if has_context_page(client["slug"]):
        return f'<a class="text-link" href="{esc(context_page_href(client["slug"]))}">Client context</a>'
    return '<span class="small">Context needed</span>'


def monthly_summary(client: dict[str, Any]) -> tuple[int, str, str]:
    monthly = client.get("monthly_deliverables", [])
    if not monthly:
        return 0, "No monthly queue", "Import weekly intake"
    total = sum(month.get("deliverable_count", 0) for month in monthly)
    latest = sorted(monthly, key=lambda item: item.get("month", ""))[-1]
    upload_counts = latest.get("upload_counts", {})
    upload_bits = ", ".join(f"{key}: {value}" for key, value in sorted(upload_counts.items())) or "no upload state"
    return total, f"Latest {latest.get('month', 'unknown')}", f"Drive {upload_bits}"


def next_action_for_client(client: dict[str, Any]) -> str:
    if client.get("next_action"):
        return str(client["next_action"])
    if client.get("blocker"):
        return str(client["blocker"])
    if not client.get("monthly_deliverables"):
        return "Import weekly topics to create this client's monthly queue."
    if client.get("missing_required"):
        return "Complete the required context pack items before assigning new drafts."
    return "Assign or update the next production action in the registry."


def render_offering_summary(client: dict[str, Any]) -> str:
    taxonomy = client.get("service_taxonomy", {})
    items = taxonomy.get("items", [])
    if not items:
        return "No service taxonomy found yet. Add raw/knowledge/service-taxonomy.md before assigning drafts."
    names = [str(item.get("name", "")).strip() for item in items if item.get("name")]
    return esc(", ".join(names[:6]))


def automation_priority_label(client: dict[str, Any]) -> str:
    priority = client.get("automation_priority")
    if priority in ("", None):
        return "Priority unset"
    return f"P{priority} automation"


def render_client_card(client: dict[str, Any]) -> str:
    intel = client.get("website_intelligence", {})
    total_monthly, monthly_label, drive_label = monthly_summary(client)
    website_urls = intel.get("website_urls", [])
    website_link = website_urls[0] if website_urls else ""
    notes = client.get("notes") or "No registry note yet."
    active_volume = client.get("active_monthly_volume") or "Monthly volume not set."
    brand_voice = client.get("brand_voice") or "Brand voice not set."
    risk_flags = client.get("risk_flags") or ""
    return f"""
        <article class="panel client-card">
          <div class="card-head">
            <div>
              <div class="client-name">{esc(client["display_name"])}</div>
              <div class="path">{esc(client["slug"])}</div>
            </div>
            <span class="chip {status_class(client["status"])}">{esc(client["status"])}</span>
          </div>
          <div class="chips">
            <span class="chip neutral">{esc(automation_priority_label(client))}</span>
            <span class="chip {status_class(client["readiness_status"])}">{client["readiness_score"]}% context</span>
            <span class="chip {status_class(intel.get("status", "missing"))}">{esc(intel.get("status", "missing"))} crawl</span>
          </div>
          <div>
            <p class="label">Owners</p>
            <p class="value small">CSM / POC: {esc(client.get("csm") or "Missing")}<br>Editor: {esc(client.get("editor") or "Missing")}<br>Writer: {esc(client.get("writer") or "Unassigned")}</p>
          </div>
          <div>
            <p class="label">Monthly volume</p>
            <p class="value small">{esc(active_volume)}</p>
          </div>
          <div>
            <p class="label">Brand voice</p>
            <p class="value small">{esc(brand_voice)}</p>
          </div>
          {f'<div class="risk-block"><p class="label">Flag</p><p class="value small">{esc(risk_flags)}</p></div>' if risk_flags else ''}
          <div>
            <p class="label">Next action</p>
            <p class="value">{esc(next_action_for_client(client))}</p>
          </div>
          <div>
            <p class="label">Offering context</p>
            <p class="value small">{render_offering_summary(client)}</p>
          </div>
          <div>
            <p class="label">Registry note</p>
            <p class="value small">{esc(notes)}</p>
          </div>
          <div class="metric-row">
            <div class="metric"><strong>{total_monthly}</strong><span class="small">deliverables</span></div>
            <div class="metric"><strong>{client.get("service_taxonomy", {}).get("count", 0)}</strong><span class="small">offerings</span></div>
            <div class="metric"><strong>{len(client.get("runs", []))}</strong><span class="small">runs</span></div>
          </div>
          <div class="link-row">
            {context_link_html(client)}
            {f'<a class="text-link" href="{esc(website_link)}">Website</a>' if website_link else ''}
            <span class="small">{esc(monthly_label)} · {esc(drive_label)}</span>
          </div>
        </article>"""


def render_client_row(client: dict[str, Any]) -> str:
    readiness = client["readiness_status"]
    readiness_details = ""
    missing = client["missing_required"] + client["missing_recommended"]
    if missing:
        items = "".join(f"<li>{esc(item)}</li>" for item in missing[:6])
        more = len(missing) - 6
        if more > 0:
            items += f"<li>{more} more</li>"
        readiness_details = f"<ul class=\"missing\">{items}</ul>"
    monthly_count, monthly_label, drive_label = monthly_summary(client)
    work = (
        f"{monthly_count} monthly deliverables"
        f"<br><span class=\"small\">{esc(monthly_label)}; {esc(drive_label)}</span>"
        f"<br><span class=\"small\">{len(client['campaigns'])} legacy campaigns, {len(client['runs'])} runs</span>"
    )
    intel = client.get("website_intelligence", {})
    intel_status = intel.get("status", "missing")
    websites = intel.get("website_urls", [])
    website_line = "<br>".join(f"<a href=\"{esc(url)}\">{esc(url)}</a>" for url in websites[:2]) or "Missing URL"
    intel_blockers = intel.get("blockers", [])
    intel_detail = (
        f"{website_line}"
        f"<br><span class=\"small\">{intel.get('sitemap_count', 0)} sitemaps, {intel.get('url_count', 0)} URLs, "
        f"{intel.get('product_or_service_count', 0)} product/service URLs</span>"
    )
    if intel_blockers:
        intel_detail += f"<br><span class=\"small\">Blocker: {esc(intel_blockers[0])}</span>"
    next_action = next_action_for_client(client)
    context_link = context_link_html(client)
    automation_detail = (
        f"{esc(automation_priority_label(client))}"
        f"<br><span class=\"small\">{esc(client.get('active_monthly_volume') or 'Volume not set')}</span>"
        f"<br><span class=\"small\">{esc(client.get('brand_voice') or 'Voice not set')}</span>"
    )
    if client.get("risk_flags"):
        automation_detail += f"<br><span class=\"small\">Flag: {esc(client['risk_flags'])}</span>"
    return f"""
        <tr>
          <td data-label="Client">
            <div class="client-name">{esc(client["display_name"])}</div>
            <div class="path">{esc(client["slug"])}</div>
            <div class="small">{esc(client["notes"])}</div>
          </td>
          <td data-label="Automation">{automation_detail}</td>
          <td data-label="Status"><span class="chip {status_class(client["status"])}">{esc(client["status"])}</span></td>
          <td data-label="Readiness">
            <span class="chip {status_class(readiness)}">{client["readiness_score"]}% {esc(readiness)}</span>
            {readiness_details}
          </td>
          <td data-label="Website Intel">
            <span class="chip {status_class(intel_status)}">{esc(intel_status)}</span><br>
            {intel_detail}
          </td>
          <td data-label="Owners">{esc(client["owner_label"])}</td>
          <td data-label="Monthly Work">{work}</td>
          <td data-label="Next action">{esc(next_action)}</td>
          <td data-label="Context">{context_link}<br><span class="small">{esc(client["path"])}</span></td>
        </tr>"""


def write_outputs(report: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    HTML_REPORT.write_text(render_html(report), encoding="utf-8")
    if INTAKE_TEMPLATE_SOURCE.exists():
        shutil.copyfile(INTAKE_TEMPLATE_SOURCE, INTAKE_TEMPLATE_REPORT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build LinkGraph delivery dashboard.")
    parser.add_argument("--json-only", action="store_true", help="Only write the JSON report.")
    args = parser.parse_args()

    registry = load_registry()
    report = build_report(registry)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not args.json_only:
        HTML_REPORT.write_text(render_html(report), encoding="utf-8")
        if INTAKE_TEMPLATE_SOURCE.exists():
            shutil.copyfile(INTAKE_TEMPLATE_SOURCE, INTAKE_TEMPLATE_REPORT)

    summary = report["summary"]
    print(
        "Delivery dashboard built: "
        f"{summary['client_count']} clients, "
        f"{summary['ready_count']} ready, "
        f"{summary['partial_count']} partial, "
        f"{summary['not_ready_count']} not ready"
    )
    print(f"HTML: {HTML_REPORT.relative_to(ROOT)}")
    print(f"JSON: {JSON_REPORT.relative_to(ROOT)}")
    if INTAKE_TEMPLATE_REPORT.exists():
        print(f"Intake template: {INTAKE_TEMPLATE_REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
