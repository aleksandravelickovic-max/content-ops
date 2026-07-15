#!/usr/bin/env python3
"""
Create the canonical per-client content ops folders.

For every client with a STYLE-SYSTEM.md, this script creates:

    client-intelligence/
      README.md
      STYLE-GUIDE.md
      offerings.md
      offerings.json
      source-files.md

    deliverables/
      README.md
      index.json
      drafts/
      final/
      html/
      review/
      shipped/

The companion migration script moves existing campaign deliverables. This
script indexes the canonical deliverables folder first, then any legacy
campaign deliverables that have not been migrated yet.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
CONTEXT_DATA = ROOT / "reports" / "client-context-dashboard" / "data.json"
EXCLUDED_CLIENT_SLUGS = {"searchatlas"}

DELIVERABLE_DIR_NAMES = {"drafts", "final", "html", "gdocs-content", "runs"}
CANONICAL_DELIVERABLE_STAGES = {"drafts", "final", "html", "review", "shipped"}


def load_context_data() -> dict[str, Any]:
    try:
        data = json.loads(CONTEXT_DATA.read_text(encoding="utf-8"))
    except Exception:
        return {"clients": []}
    return {client["slug"]: client for client in data.get("clients", [])}


def discover_clients() -> list[tuple[str, Path]]:
    clients = []
    for style_path in sorted(CLIENTS_DIR.rglob("STYLE-SYSTEM.md")):
        slug = style_path.parent.relative_to(CLIENTS_DIR).as_posix()
        if slug in EXCLUDED_CLIENT_SLUGS:
            continue
        clients.append((slug, style_path.parent))
    return clients


def display_name_from_style(style_path: Path, slug: str) -> str:
    try:
        for line in style_path.read_text(encoding="utf-8", errors="replace").splitlines()[:20]:
            if line.startswith("# "):
                return line[2:].replace("Style System", "").replace("—", "").strip() or title_from_slug(slug)
    except Exception:
        pass
    return title_from_slug(slug)


def title_from_slug(slug: str) -> str:
    return slug.replace("/", " / ").replace("-", " ").title()


def write_text_if_changed(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8", errors="replace") == text:
        return
    path.write_text(text, encoding="utf-8")


def copy_style_system(client_dir: Path) -> None:
    source = client_dir / "STYLE-SYSTEM.md"
    target = client_dir / "client-intelligence" / "STYLE-GUIDE.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or source.read_text(encoding="utf-8", errors="replace") != target.read_text(encoding="utf-8", errors="replace"):
        shutil.copyfile(source, target)


def collect_deliverables(client_dir: Path) -> list[dict[str, Any]]:
    deliverables = []
    canonical = client_dir / "deliverables"
    if canonical.exists():
        for path in sorted(canonical.rglob("*")):
            if not path.is_file() or path.name.startswith("."):
                continue
            rel_parts = path.relative_to(canonical).parts
            if not rel_parts or rel_parts[0] not in CANONICAL_DELIVERABLE_STAGES:
                continue
            if path.suffix.lower() not in {".md", ".html", ".htm", ".json", ".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg", ".webp", ".svg"}:
                continue
            deliverables.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "campaign": rel_parts[1] if len(rel_parts) > 2 else "",
                    "stage": rel_parts[0],
                    "type": path.suffix.lower().lstrip("."),
                    "name": path.name,
                    "size": path.stat().st_size,
                    "source": "canonical",
                }
            )
    campaigns = client_dir / "campaigns"
    if not campaigns.exists():
        return deliverables
    for path in sorted(campaigns.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        rel_parts = path.relative_to(campaigns).parts
        if not any(part in DELIVERABLE_DIR_NAMES for part in rel_parts):
            continue
        stage = next((part for part in rel_parts if part in DELIVERABLE_DIR_NAMES), "other")
        if path.suffix.lower() not in {".md", ".html", ".json", ".pdf", ".docx"}:
            continue
        deliverables.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "campaign": rel_parts[0] if rel_parts else "",
                "stage": stage,
                "type": path.suffix.lower().lstrip("."),
                "name": path.name,
                "size": path.stat().st_size,
                "source": "legacy-campaign",
            }
        )
    return deliverables


def render_client_intelligence_readme(slug: str, display_name: str) -> str:
    return f"""# {display_name} Client Intelligence

This folder is the writer-facing source of truth for client context.

## Files

- `STYLE-GUIDE.md` — copy of the canonical client style system.
- `offerings.md` — extracted products, services, goods, treatments, collections, or solution areas.
- `offerings.json` — machine-readable version of the offerings index.
- `source-files.md` — local source material available in this repo.

## Source of truth

The canonical style system still lives at:

```text
clients/{slug}/STYLE-SYSTEM.md
```

Run this to refresh this folder:

```bash
python3 scripts/build-client-context-dashboard.py
python3 scripts/organize-client-folders.py
```
"""


def render_deliverables_readme(slug: str, display_name: str, deliverables: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for item in deliverables:
        counts[item["stage"]] = counts.get(item["stage"], 0) + 1
    count_lines = "\n".join(f"- {stage}: {count}" for stage, count in sorted(counts.items())) or "- No indexed deliverables yet."
    return f"""# {display_name} Deliverables

This folder is the canonical delivery workspace for {display_name}.

## Subfolders

- `drafts/` — active working drafts.
- `final/` — approved markdown or source deliverables.
- `html/` — rendered HTML and browser-ready delivery files.
- `review/` — review links, notes, and client feedback exports.
- `shipped/` — delivered or published final artifacts.

## Existing deliverables indexed from campaigns

{count_lines}

See `index.json` for the machine-readable deliverables list.

## Current rule

New delivery work should land here first, then link back to campaign strategy, briefs, or research when needed.

Refresh:

```bash
python3 scripts/organize-client-folders.py
```
"""


def render_offerings_md(display_name: str, offerings: list[dict[str, Any]]) -> str:
    lines = [f"# {display_name} Offerings", ""]
    if not offerings:
        lines.extend(["No offerings extracted yet.", ""])
        return "\n".join(lines)
    for item in offerings:
        lines.append(f"## {item.get('name', 'Untitled')}")
        desc = item.get("description") or "No short description extracted yet."
        lines.append("")
        lines.append(desc)
        sources = item.get("sources") or []
        if sources:
            lines.append("")
            lines.append("Sources:")
            lines.extend(f"- `{source}`" for source in sources[:8])
        lines.append("")
    return "\n".join(lines)


def render_source_files_md(display_name: str, source_files: list[str]) -> str:
    lines = [f"# {display_name} Source Files", ""]
    if not source_files:
        lines.append("No source files indexed.")
    else:
        lines.extend(f"- `{path}`" for path in source_files)
    lines.append("")
    return "\n".join(lines)


def organize_client(slug: str, client_dir: Path, context: dict[str, Any]) -> None:
    display_name = context.get("display_name") or display_name_from_style(client_dir / "STYLE-SYSTEM.md", slug)
    intelligence_dir = client_dir / "client-intelligence"
    deliverables_dir = client_dir / "deliverables"

    for directory in [
        intelligence_dir,
        deliverables_dir / "drafts",
        deliverables_dir / "final",
        deliverables_dir / "html",
        deliverables_dir / "review",
        deliverables_dir / "shipped",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    copy_style_system(client_dir)

    offerings = context.get("offerings", [])
    source_files = context.get("source_files", [])
    deliverables = collect_deliverables(client_dir)
    generated_at = datetime.now(timezone.utc).isoformat()

    write_text_if_changed(intelligence_dir / "README.md", render_client_intelligence_readme(slug, display_name))
    write_text_if_changed(intelligence_dir / "offerings.md", render_offerings_md(display_name, offerings))
    write_text_if_changed(intelligence_dir / "source-files.md", render_source_files_md(display_name, source_files))
    write_text_if_changed(
        intelligence_dir / "offerings.json",
        json.dumps(
            {
                "client": slug,
                "display_name": display_name,
                "generated_at": generated_at,
                "offerings": offerings,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )
    write_text_if_changed(deliverables_dir / "README.md", render_deliverables_readme(slug, display_name, deliverables))
    write_text_if_changed(
        deliverables_dir / "index.json",
        json.dumps(
            {
                "client": slug,
                "display_name": display_name,
                "generated_at": generated_at,
                "existing_campaign_deliverables": deliverables,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )


def main() -> int:
    contexts = load_context_data()
    clients = discover_clients()
    for slug, client_dir in clients:
        organize_client(slug, client_dir, contexts.get(slug, {}))
    print(f"Organized {len(clients)} clients")
    print("Created/updated client-intelligence/ and deliverables/ folders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
