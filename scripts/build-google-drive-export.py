#!/usr/bin/env python3
"""
Build a Google Drive export queue for monthly LinkGraph deliverables.

This does not call the Google Drive API. It creates a Drive-ready staging folder
and manifest that an upload adapter can use later.

Outputs:
    reports/google-drive-export/{YYYY-MM}/manifest.json
    reports/google-drive-export/{YYYY-MM}/upload-plan.md
    reports/google-drive-export/{YYYY-MM}/files/{client}/{deliverable}/...
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
OUT_ROOT = ROOT / "reports" / "google-drive-export"
STAGES = ("brief", "draft", "review", "final", "platform_upload")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_registries(month: str, client_filter: str | None) -> list[Path]:
    registries = []
    for path in sorted(CLIENTS_DIR.rglob(f"deliverables/{month}/registry.json")):
        slug = path.parent.parent.parent.relative_to(CLIENTS_DIR).as_posix()
        if client_filter and slug != client_filter:
            continue
        registries.append(path)
    return registries


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stage_file(src: Path, dst_dir: Path) -> str:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    return dst.relative_to(ROOT).as_posix()


def collect_file_entries(item: dict[str, Any], staging_dir: Path) -> list[dict[str, Any]]:
    entries = []
    paths = item.get("paths", {})
    for stage in STAGES:
        rel_path = paths.get(stage)
        if not rel_path:
            continue
        src = ROOT / rel_path
        exists = src.exists()
        staged_path = ""
        if exists and src.is_file():
            staged_path = stage_file(src, staging_dir / stage)
        entries.append(
            {
                "stage": stage,
                "source_path": rel_path,
                "exists": exists,
                "staged_path": staged_path,
            }
        )
    return entries


def build_manifest(month: str, client_filter: str | None) -> dict[str, Any]:
    export_dir = OUT_ROOT / month
    files_root = export_dir / "files"
    export_dir.mkdir(parents=True, exist_ok=True)

    clients = []
    upload_items = []
    for registry_path in find_registries(month, client_filter):
        registry = load_json(registry_path)
        client_slug = registry["client"]
        client_folder = registry.get("google_drive", {}).get("root_folder_name") or (
            f"LinkGraph Delivery/{month}/{registry.get('display_name') or client_slug}"
        )
        client_summary = {
            "client": client_slug,
            "display_name": registry.get("display_name") or client_slug,
            "registry_path": registry_path.relative_to(ROOT).as_posix(),
            "drive_folder_name": client_folder,
            "drive_folder_url": registry.get("google_drive", {}).get("folder_url", ""),
            "deliverable_count": len(registry.get("deliverables", [])),
        }
        clients.append(client_summary)

        for item in registry.get("deliverables", []):
            item_stage_dir = files_root / client_slug.replace("/", "__") / item["id"]
            file_entries = collect_file_entries(item, item_stage_dir)
            upload_items.append(
                {
                    "id": item["id"],
                    "client": client_slug,
                    "month": month,
                    "type": item.get("type", ""),
                    "topic": item.get("topic", ""),
                    "primary_keyword": item.get("primary_keyword", ""),
                    "status": item.get("status", ""),
                    "priority": item.get("priority", ""),
                    "due_date": item.get("due_date", ""),
                    "drive_folder_name": f"{client_folder}/{item['id']}",
                    "drive_folder_url": item.get("google_drive", {}).get("folder_url", ""),
                    "upload_status": item.get("google_drive", {}).get("upload_status", "not-staged"),
                    "files": file_entries,
                }
            )

    manifest = {
        "generated_at": now_iso(),
        "month": month,
        "client_filter": client_filter or "",
        "export_dir": export_dir.relative_to(ROOT).as_posix(),
        "google_drive_target": "Google Drive",
        "upload_mode": "manifest-first",
        "note": "Use this manifest as the queue for a Google Drive API adapter or manual upload.",
        "clients": clients,
        "upload_items": upload_items,
        "summary": {
            "client_count": len(clients),
            "deliverable_count": len(upload_items),
            "existing_file_count": sum(
                1 for item in upload_items for file_entry in item["files"] if file_entry["exists"]
            ),
            "missing_file_count": sum(
                1 for item in upload_items for file_entry in item["files"] if not file_entry["exists"]
            ),
        },
    }
    return manifest


def write_plan(manifest: dict[str, Any]) -> None:
    out_dir = ROOT / manifest["export_dir"]
    lines = [
        f"# Google Drive Upload Plan: {manifest['month']}",
        "",
        f"Generated: {manifest['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Clients: {manifest['summary']['client_count']}",
        f"- Deliverables: {manifest['summary']['deliverable_count']}",
        f"- Existing files staged: {manifest['summary']['existing_file_count']}",
        f"- Missing expected files: {manifest['summary']['missing_file_count']}",
        "",
        "## Folder Plan",
        "",
    ]
    for client in manifest["clients"]:
        lines.append(f"- {client['drive_folder_name']} ({client['deliverable_count']} deliverables)")
    lines += ["", "## Upload Items", ""]
    for item in manifest["upload_items"]:
        lines.append(f"### {item['id']} - {item['topic']}")
        lines.append("")
        lines.append(f"- Client: {item['client']}")
        lines.append(f"- Type: {item['type']}")
        lines.append(f"- Primary keyword: {item['primary_keyword']}")
        lines.append(f"- Status: {item['status']}")
        lines.append(f"- Drive folder: {item['drive_folder_name']}")
        for file_entry in item["files"]:
            mark = "x" if file_entry["exists"] else " "
            staged = f" -> `{file_entry['staged_path']}`" if file_entry["staged_path"] else ""
            lines.append(f"- [{mark}] {file_entry['stage']}: `{file_entry['source_path']}`{staged}")
        lines.append("")
    (out_dir / "upload-plan.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Google Drive export queue for monthly deliverables.")
    parser.add_argument("--month", required=True, help="Month in YYYY-MM format.")
    parser.add_argument("--client", help="Optional client slug filter.")
    args = parser.parse_args()

    manifest = build_manifest(args.month, args.client)
    out_dir = ROOT / manifest["export_dir"]
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_plan(manifest)
    summary = manifest["summary"]
    print(
        "Built Google Drive export for {deliverable_count} deliverables across {client_count} clients. "
        "Staged {existing_file_count} files; {missing_file_count} expected files missing.".format(**summary)
    )
    print(f"Manifest: {(out_dir / 'manifest.json').relative_to(ROOT).as_posix()}")
    print(f"Plan: {(out_dir / 'upload-plan.md').relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
