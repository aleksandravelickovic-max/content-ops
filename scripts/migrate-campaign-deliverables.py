#!/usr/bin/env python3
"""
Move campaign deliverable files into each client's canonical deliverables folder.

The old campaign folders keep briefs, research, registries, and other planning files.
Only files inside known delivery stage folders are moved:

    campaigns/{campaign}/drafts/*        -> deliverables/drafts/{campaign}/
    campaigns/{campaign}/final/*         -> deliverables/final/{campaign}/
    campaigns/{campaign}/html/*          -> deliverables/html/{campaign}/
    campaigns/{campaign}/gdocs-content/* -> deliverables/review/{campaign}/
    campaigns/{campaign}/runs/*          -> deliverables/review/{campaign}/runs/

Run without --apply for a dry run.
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
EXCLUDED_CLIENT_SLUGS = {"searchatlas"}

STAGE_MAP = {
    "drafts": ("drafts", (".md", ".docx", ".txt", ".html")),
    "final": ("final", (".md", ".docx", ".pdf", ".html", ".txt")),
    "html": ("html", (".html", ".htm", ".css", ".js", ".json", ".png", ".jpg", ".jpeg", ".webp", ".svg")),
    "gdocs-content": ("review", (".md", ".html", ".json", ".txt", ".docx")),
    "runs": ("review", (".md", ".json", ".txt", ".html")),
}


@dataclass
class MovePlan:
    client: str
    campaign: str
    stage: str
    source: Path
    target: Path


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def discover_moves() -> list[MovePlan]:
    moves: list[MovePlan] = []
    for style_path in sorted(CLIENTS_DIR.rglob("STYLE-SYSTEM.md")):
        client_dir = style_path.parent
        client_slug = client_dir.relative_to(CLIENTS_DIR).as_posix()
        if client_slug in EXCLUDED_CLIENT_SLUGS:
            continue
        campaigns_dir = client_dir / "campaigns"
        if not campaigns_dir.exists():
            continue
        for stage_name, (target_stage, suffixes) in STAGE_MAP.items():
            for stage_dir in sorted(campaigns_dir.glob(f"*/{stage_name}")):
                if not stage_dir.is_dir():
                    continue
                campaign = stage_dir.parent.name
                for source in sorted(stage_dir.rglob("*")):
                    if not source.is_file() or source.name.startswith("."):
                        continue
                    if source.suffix.lower() not in suffixes:
                        continue
                    nested = source.relative_to(stage_dir)
                    if stage_name == "runs":
                        target = client_dir / "deliverables" / target_stage / campaign / "runs" / nested
                    else:
                        target = client_dir / "deliverables" / target_stage / campaign / nested
                    moves.append(MovePlan(client_slug, campaign, stage_name, source, unique_target(target)))
    return moves


def unique_target(target: Path) -> Path:
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    index = 2
    while True:
        candidate = parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def apply_moves(moves: list[MovePlan]) -> dict[str, list[dict[str, Any]]]:
    manifests: dict[str, list[dict[str, Any]]] = {}
    for move in moves:
        move.target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(move.source), str(move.target))
        manifests.setdefault(move.client, []).append(
            {
                "campaign": move.campaign,
                "stage": move.stage,
                "from": rel(move.source),
                "to": rel(move.target),
            }
        )
    return manifests


def write_manifests(manifests: dict[str, list[dict[str, Any]]]) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    for client, moves in manifests.items():
        path = CLIENTS_DIR / client / "deliverables" / "MIGRATION-MANIFEST.json"
        existing: list[dict[str, Any]] = []
        if path.exists():
            try:
                existing = json.loads(path.read_text(encoding="utf-8")).get("moves", [])
            except Exception:
                existing = []
        payload = {
            "client": client,
            "generated_at": generated_at,
            "move_count": len(existing) + len(moves),
            "moves": existing + moves,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Move campaign deliverable files into client deliverables folders.")
    parser.add_argument("--apply", action="store_true", help="Actually move files. Without this flag, prints a dry run.")
    args = parser.parse_args()

    moves = discover_moves()
    print(f"Discovered {len(moves)} deliverable files to move.")
    by_client: dict[str, int] = {}
    for move in moves:
        by_client[move.client] = by_client.get(move.client, 0) + 1
    for client, count in sorted(by_client.items()):
        print(f"- {client}: {count}")

    if not args.apply:
        print("Dry run only. Re-run with --apply to move files.")
        for move in moves[:20]:
            print(f"  {rel(move.source)} -> {rel(move.target)}")
        if len(moves) > 20:
            print(f"  ... {len(moves) - 20} more")
        return 0

    manifests = apply_moves(moves)
    write_manifests(manifests)
    print(f"Moved {len(moves)} files and wrote migration manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
