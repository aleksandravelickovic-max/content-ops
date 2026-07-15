#!/usr/bin/env python3
"""
Import weekly LinkGraph topic and keyword intake into monthly client registries.

Input CSV columns:
    client, month, type, topic, primary_keyword, secondary_keywords, notes,
    priority, due_date

Outputs:
    clients/{client}/deliverables/{YYYY-MM}/registry.json
    clients/{client}/deliverables/{YYYY-MM}/briefs/{deliverable_id}.md
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
DEFAULT_STATUS = "intake"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"


def discover_clients() -> dict[str, Path]:
    clients: dict[str, Path] = {}
    for style_path in CLIENTS_DIR.rglob("STYLE-SYSTEM.md"):
        slug = style_path.parent.relative_to(CLIENTS_DIR).as_posix()
        clients[slug] = style_path.parent
    return clients


def resolve_client(raw_client: str, clients: dict[str, Path]) -> str:
    cleaned = raw_client.strip()
    if cleaned in clients:
        return cleaned
    slug = slugify(cleaned)
    if slug in clients:
        return slug
    normalized = slug.replace("-", "")
    matches = [candidate for candidate in clients if candidate.replace("/", "-").replace("-", "") == normalized]
    if len(matches) == 1:
        return matches[0]
    raise SystemExit(f"Unknown client '{raw_client}'. Expected one of: {', '.join(sorted(clients))}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"No rows found in {path}")
    required = {"client", "topic", "primary_keyword"}
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"Missing required CSV columns: {', '.join(sorted(missing))}")
    return rows


def split_secondary_keywords(value: str) -> list[str]:
    parts = re.split(r"[;,]\s*|\n+", value or "")
    return [part.strip() for part in parts if part.strip()]


def load_registry(path: Path, client_slug: str, client_dir: Path, month: str) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    display_name = client_slug.replace("/", " / ").replace("-", " ").title()
    return {
        "client": client_slug,
        "display_name": display_name,
        "month": month,
        "generated_at": now_iso(),
        "google_drive": {
            "root_folder_name": f"LinkGraph Delivery/{month}/{display_name}",
            "folder_url": "",
            "upload_status": "not-uploaded",
            "last_export_manifest": "",
        },
        "deliverables": [],
    }


def next_deliverable_id(client_slug: str, month: str, registry: dict[str, Any]) -> str:
    prefix = f"{client_slug.replace('/', '-')}-{month}"
    used = {item.get("id", "") for item in registry.get("deliverables", [])}
    index = 1
    while True:
        candidate = f"{prefix}-{index:03d}"
        if candidate not in used:
            return candidate
        index += 1


def find_existing(registry: dict[str, Any], row: dict[str, str]) -> dict[str, Any] | None:
    explicit_id = (row.get("id") or "").strip()
    if explicit_id:
        for item in registry.get("deliverables", []):
            if item.get("id") == explicit_id:
                return item
    topic_key = slugify(row.get("topic", ""))
    keyword_key = slugify(row.get("primary_keyword", ""))
    for item in registry.get("deliverables", []):
        if slugify(item.get("topic", "")) == topic_key and slugify(item.get("primary_keyword", "")) == keyword_key:
            return item
    return None


def ensure_month_dirs(month_dir: Path) -> None:
    for name in ("intake", "briefs", "drafts", "reviews", "final", "platform-uploads"):
        (month_dir / name).mkdir(parents=True, exist_ok=True)


def build_paths(client_slug: str, month: str, deliverable_id: str) -> dict[str, str]:
    base = f"clients/{client_slug}/deliverables/{month}"
    return {
        "brief": f"{base}/briefs/{deliverable_id}.md",
        "draft": f"{base}/drafts/{deliverable_id}.md",
        "review": f"{base}/reviews/{deliverable_id}.md",
        "final": f"{base}/final/{deliverable_id}.md",
        "platform_upload": f"{base}/platform-uploads/{deliverable_id}.json",
    }


def upsert_deliverable(
    registry: dict[str, Any],
    row: dict[str, str],
    client_slug: str,
    month: str,
    intake_path: Path,
) -> dict[str, Any]:
    item = find_existing(registry, row)
    created = False
    if item is None:
        deliverable_id = (row.get("id") or "").strip() or next_deliverable_id(client_slug, month, registry)
        item = {
            "id": deliverable_id,
            "client": client_slug,
            "month": month,
            "created_at": now_iso(),
            "status": DEFAULT_STATUS,
            "production_environment": "codex-or-claude-code",
            "google_drive": {"upload_status": "not-staged", "folder_url": "", "file_url": ""},
        }
        registry.setdefault("deliverables", []).append(item)
        created = True

    deliverable_id = item["id"]
    item.update(
        {
            "updated_at": now_iso(),
            "type": (row.get("type") or "blog").strip(),
            "topic": row.get("topic", "").strip(),
            "primary_keyword": row.get("primary_keyword", "").strip(),
            "secondary_keywords": split_secondary_keywords(row.get("secondary_keywords", "")),
            "notes": row.get("notes", "").strip(),
            "priority": row.get("priority", "").strip() or "standard",
            "due_date": row.get("due_date", "").strip(),
            "source_intake": intake_path.relative_to(ROOT).as_posix(),
            "paths": build_paths(client_slug, month, deliverable_id),
        }
    )
    if created:
        item["status"] = (row.get("status") or DEFAULT_STATUS).strip() or DEFAULT_STATUS
    return item


def write_brief_stub(client_slug: str, month: str, item: dict[str, Any]) -> None:
    brief_path = ROOT / item["paths"]["brief"]
    if brief_path.exists():
        return
    secondary = ", ".join(item.get("secondary_keywords", [])) or "TBD"
    content = f"""# {item.get("topic") or item["id"]}

Client: {client_slug}
Month: {month}
Deliverable ID: {item["id"]}
Type: {item.get("type") or "blog"}
Status: {item.get("status") or DEFAULT_STATUS}

## Topic And Keywords

- Topic: {item.get("topic") or "TBD"}
- Primary keyword: {item.get("primary_keyword") or "TBD"}
- Secondary keywords: {secondary}
- Priority: {item.get("priority") or "standard"}
- Due date: {item.get("due_date") or "TBD"}

## Client Context To Load

- `clients/{client_slug}/STYLE-SYSTEM.md`
- `clients/{client_slug}/raw/knowledge/service-taxonomy.md`
- `clients/{client_slug}/client-intelligence/offerings.md`
- `clients/{client_slug}/raw/research/website-intelligence.md`

## Notes

{item.get("notes") or "Add angle, SERP notes, internal links, or source constraints here."}

## Production Paths

- Draft: `{item["paths"]["draft"]}`
- Review: `{item["paths"]["review"]}`
- Final: `{item["paths"]["final"]}`
- Upload receipt: `{item["paths"]["platform_upload"]}`
"""
    brief_path.write_text(content, encoding="utf-8")


def import_rows(path: Path, rows: list[dict[str, str]], default_month: str | None) -> dict[str, int]:
    clients = discover_clients()
    counts = {"rows": 0, "clients": 0, "registries": 0, "deliverables": 0}
    touched: set[Path] = set()
    touched_clients: set[str] = set()

    for row in rows:
        client_slug = resolve_client(row.get("client", ""), clients)
        month = (row.get("month") or default_month or "").strip()
        if not re.match(r"^\d{4}-\d{2}$", month):
            raise SystemExit(f"Row for {client_slug} has invalid or missing month: {month!r}")

        client_dir = clients[client_slug]
        month_dir = client_dir / "deliverables" / month
        ensure_month_dirs(month_dir)
        registry_path = month_dir / "registry.json"
        registry = load_registry(registry_path, client_slug, client_dir, month)
        item = upsert_deliverable(registry, row, client_slug, month, path)
        write_brief_stub(client_slug, month, item)
        registry["generated_at"] = now_iso()
        registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        counts["rows"] += 1
        counts["deliverables"] += 1
        touched.add(registry_path)
        touched_clients.add(client_slug)

    counts["clients"] = len(touched_clients)
    counts["registries"] = len(touched)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Import weekly topic intake into client monthly deliverable registries.")
    parser.add_argument("csv_path", help="CSV file with client/topic/keyword rows.")
    parser.add_argument("--month", help="Default YYYY-MM month when a row does not include one.")
    args = parser.parse_args()

    path = Path(args.csv_path)
    if not path.is_absolute():
        path = ROOT / path
    rows = read_csv(path)
    counts = import_rows(path, rows, args.month)
    print(
        "Imported {rows} rows into {registries} monthly registries across {clients} clients.".format(**counts)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
