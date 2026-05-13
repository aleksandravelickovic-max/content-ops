"""Reads campaign content from the filesystem using registry.json files."""

import json
from pathlib import Path

import markdown

from .config import CONTENT_ROOT

_md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "meta"])


def get_campaign_path(client_slug: str, campaign_slug: str) -> Path | None:
    p = Path(CONTENT_ROOT) / client_slug / "campaigns" / campaign_slug
    return p if p.is_dir() else None


def load_registry(client_slug: str, campaign_slug: str) -> dict | None:
    camp_path = get_campaign_path(client_slug, campaign_slug)
    if not camp_path:
        return None
    reg_file = camp_path / "registry.json"
    if not reg_file.exists():
        return None
    with open(reg_file, encoding="utf-8") as f:
        return json.load(f)


def load_client_registry(client_slug: str) -> dict | None:
    p = Path(CONTENT_ROOT) / client_slug / "registry.json"
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def get_content_html(client_slug: str, campaign_slug: str, content_path: str) -> str | None:
    camp_path = get_campaign_path(client_slug, campaign_slug)
    if not camp_path:
        return None
    full_path = camp_path / content_path
    if not full_path.exists() or not full_path.is_file():
        return None
    # Prevent path traversal
    try:
        full_path.resolve().relative_to(camp_path.resolve())
    except ValueError:
        return None

    text = full_path.read_text(encoding="utf-8", errors="replace")

    if full_path.suffix.lower() == ".html":
        return text
    if full_path.suffix.lower() == ".md":
        _md.reset()
        return _md.convert(text)
    return f"<pre>{text}</pre>"


def get_content_raw(client_slug: str, campaign_slug: str, content_path: str) -> str | None:
    camp_path = get_campaign_path(client_slug, campaign_slug)
    if not camp_path:
        return None
    full_path = camp_path / content_path
    if not full_path.exists() or not full_path.is_file():
        return None
    try:
        full_path.resolve().relative_to(camp_path.resolve())
    except ValueError:
        return None
    return full_path.read_text(encoding="utf-8", errors="replace")


def list_campaigns(client_slug: str) -> list[str]:
    camp_dir = Path(CONTENT_ROOT) / client_slug / "campaigns"
    if not camp_dir.is_dir():
        return []
    return sorted(d.name for d in camp_dir.iterdir() if d.is_dir() and not d.name.startswith("."))


def get_compare_pairs(registry: dict) -> list[dict]:
    originals = {
        e["path"].split("/")[-1]: e
        for e in registry.get("entries", [])
        if e.get("type") == "html-original"
    }
    revised_set = {
        e["path"].split("/")[-1]
        for e in registry.get("entries", [])
        if e.get("type") == "html-revised"
    }
    pairs = []
    for filename, entry in sorted(originals.items()):
        pairs.append({
            "filename": filename,
            "display_name": filename.replace("--", " / ").replace(".html", "").replace("-", " ").title(),
            "has_revised": filename in revised_set,
            "page_type": "collection" if filename.startswith("collections") else "product",
        })
    return pairs


def list_clients() -> list[str]:
    root = Path(CONTENT_ROOT)
    if not root.is_dir():
        return []
    return sorted(
        d.name for d in root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "STYLE-SYSTEM.md").exists()
    )
