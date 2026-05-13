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


def find_draft_for_html(
    client_slug: str, campaign_slug: str, filename: str
) -> dict | None:
    """Map an HTML filename to its corresponding markdown draft.

    Returns ``{"path": "<relative-path>", "html": "<rendered-html>"}`` or
    ``None`` when no matching draft can be found.

    Resolution strategy:
      1. Extract the page type (``products`` / ``collections``) and URL slug
         from *filename* (e.g. ``products--burnt-sugar-zellige-tile.html``).
      2. Scan ``gdocs-content/{product,collection}-pages/*.md`` for a file
         whose ``**URL:**`` field contains the slug.
      3. Fallback for collections: scan ``drafts/*.md`` where the draft
         filename (minus numeric prefix) matches the collection name.
    """
    camp_path = get_campaign_path(client_slug, campaign_slug)
    if not camp_path:
        return None

    # Determine page type and slug from the HTML filename
    base = filename.replace(".html", "")
    if base.startswith("products--"):
        page_type = "product"
        slug = base[len("products--"):]
    elif base.startswith("collections--"):
        page_type = "collection"
        slug = base[len("collections--"):]
    else:
        return None

    # --- Strategy 1: match via **URL:** field in gdocs-content ---
    if page_type == "product":
        search_dirs = [camp_path / "gdocs-content" / "product-pages"]
    else:
        search_dirs = [camp_path / "gdocs-content" / "collection-pages"]

    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for md_file in sorted(search_dir.glob("*.md")):
            try:
                md_file.resolve().relative_to(camp_path.resolve())
            except ValueError:
                continue
            text = md_file.read_text(encoding="utf-8", errors="replace")
            # Look for **URL:** line that ends with our slug
            for line in text.splitlines()[:30]:  # URL is always near the top
                if "**URL:**" in line or "**url:**" in line.lower():
                    # Extract the URL path portion after the domain
                    # Handles both <https://...> and bare https://... formats
                    cleaned = line.replace("<", "").replace(">", "").strip()
                    # Match exact final path segment to avoid partial matches
                    # e.g. slug "cotto" must match "/cotto" at end, not "/cotto-tile-allende"
                    cleaned = cleaned.rstrip()
                    if cleaned.endswith(f"/{slug}"):
                        rel_path = str(md_file.relative_to(camp_path))
                        _md.reset()
                        rendered = _md.convert(text)
                        return {"path": rel_path, "html": rendered}
                    break  # Only check the first URL line per file

    # --- Strategy 2 (collections only): match drafts/*.md by material name ---
    if page_type == "collection":
        drafts_dir = camp_path / "drafts"
        if drafts_dir.is_dir():
            for md_file in sorted(drafts_dir.glob("*.md")):
                try:
                    md_file.resolve().relative_to(camp_path.resolve())
                except ValueError:
                    continue
                # Draft filenames: 01-zellige.md, 07-cotto.md, etc.
                stem = md_file.stem  # e.g. "01-zellige"
                # Strip numeric prefix (digits + dash)
                material = stem.lstrip("0123456789").lstrip("-")  # e.g. "zellige"
                if not material:
                    continue
                # The slug might be "zellige", "cotto", "glass-mosaics", etc.
                if material == slug or slug.startswith(material) or material.startswith(slug):
                    text = md_file.read_text(encoding="utf-8", errors="replace")
                    rel_path = str(md_file.relative_to(camp_path))
                    _md.reset()
                    rendered = _md.convert(text)
                    return {"path": rel_path, "html": rendered}

    return None


def list_clients() -> list[str]:
    root = Path(CONTENT_ROOT)
    if not root.is_dir():
        return []
    return sorted(
        d.name for d in root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "STYLE-SYSTEM.md").exists()
    )
