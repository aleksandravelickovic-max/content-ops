#!/usr/bin/env python3
"""
build-content-navigator.py

Scans client directories, generates/updates registry.json files,
reads content from all tracked files, and builds a self-contained
HTML Content Navigator with an inline preview pane.

Usage:
    python3 scripts/build-content-navigator.py
"""

import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
REPORTS_DIR = ROOT / "reports"

MAX_CONTENT_CHARS = 50_000
TRUNCATION_NOTE = "\n\n---\n*[Content truncated for preview — open the source file for the full document.]*"


# ── Helpers ──────────────────────────────────────────────────────────

def human_size(n):
    if n < 1024:
        return f"{n} B"
    elif n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    else:
        return f"{n / (1024 * 1024):.1f} MB"


def slug_to_display(slug):
    name = slug.replace(".md", "").replace(".html", "")
    name = re.sub(r"^\d+-", "", name)
    name = name.replace("-", " ").replace("_", " ")
    return name.title()


def detect_type(rel_path):
    p = str(rel_path).lower()
    if "html/revised/" in p:
        return "html-revised"
    if "html/original/" in p:
        return "html-original"
    if p == "html/index.html":
        return "html-index"
    if "product-pages/" in p:
        return "product-page"
    if "collection-pages/" in p:
        return "collection-page"
    if "drafts/v3/" in p:
        return "draft-v3"
    if "drafts/" in p:
        return "draft"
    if "campaign-urls" in p:
        return "campaign-urls"
    if "audit-report" in p:
        return "audit"
    if "brief" in p:
        return "brief"
    if "knowledge/products/" in p:
        return "product-spec"
    if "knowledge/competitors/" in p:
        return "competitor"
    if "knowledge/facts/" in p:
        return "fact"
    if "knowledge/proof/" in p:
        return "proof"
    if "knowledge/testimonials/" in p:
        return "testimonial"
    if "transcripts/" in p:
        return "transcript"
    if "research/" in p:
        return "research"
    if "reference-site/" in p:
        return "reference"
    if "style-system" in p.lower():
        return "style-system"
    return "other"


def detect_category(rel_path, file_type):
    if file_type == "collection-page":
        name = Path(rel_path).stem
        if name.startswith("color-"):
            return "color"
        if name.startswith("shape-"):
            return "shape"
        if name.startswith("space-"):
            return "space"
        if name in ("homepage", "trade-program"):
            return "special"
        return "material"
    if file_type == "product-page":
        name = Path(rel_path).stem
        mat_map = {
            "zellige": "zellige", "bejmat": "zellige",
            "cotto": "cotto", "allende": "cotto-allende",
            "ceramic": "ceramics", "linen": "ceramics", "eucalyptus": "ceramics",
            "terrazzo": "terrazzo", "bungalow": "terrazzo",
            "marble": "marble", "carrara": "marble", "basilica": "marble",
            "monument": "marble", "neutra": "terrazzo",
            "limestone": "limestone",
            "cantera": "cantera", "condesa": "cantera", "puebla": "cantera",
            "piedra": "cantera", "volcan": "cantera", "durango": "cantera",
            "glass": "glass-mosaic", "lattice": "zellige-mosaic",
            "roman": "roman-mosaic", "gambit": "roman-mosaic",
            "french-cobblestone": "roman-mosaic",
            "red-clay": "cotto", "toltec": "cotto", "stars-cross": "cotto",
            "pomelo": "cotto", "cement": "cement",
        }
        for kw, cat in mat_map.items():
            if kw in name:
                return cat
        return "other"
    return file_type


PLACEHOLDER_TITLES = {"product name", "collection name", "page title", "title", "untitled"}


def extract_title(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    title = line[2:].strip()
                    if title.lower() not in PLACEHOLDER_TITLES:
                        return title
                    return None
                m = re.match(r"^title:\s*(.+)", line, re.IGNORECASE)
                if m:
                    title = m.group(1).strip().strip('"').strip("'")
                    if title.lower() not in PLACEHOLDER_TITLES:
                        return title
                    return None
        return None
    except Exception:
        return None


def read_content(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        if len(text) > MAX_CONTENT_CHARS:
            return text[:MAX_CONTENT_CHARS] + TRUNCATION_NOTE
        return text
    except Exception:
        return "(Unable to read file)"


# ── Git-based comparison helpers ─────────────────────────────────────

PRE_PATCH_COMMIT = "520d22e"  # commit before style patches
PATCH_COMMIT = "2ee3699"  # the style-audit patch commit


def get_changed_files():
    """Get set of files changed in the style patch commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{PRE_PATCH_COMMIT}..{PATCH_COMMIT}", "--", "clients/"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        if result.returncode == 0 and result.stdout.strip():
            return set(result.stdout.strip().split("\n"))
        return set()
    except Exception:
        return set()


def get_pre_patch_content(rel_path):
    """Get file content from before the style patches were applied."""
    try:
        result = subprocess.run(
            ["git", "show", f"{PRE_PATCH_COMMIT}:{rel_path}"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        if result.returncode == 0:
            content = result.stdout
            if len(content) > MAX_CONTENT_CHARS:
                return content[:MAX_CONTENT_CHARS] + TRUNCATION_NOTE
            return content
        return None
    except Exception:
        return None


# ── URL / HTML Mapping ──────────────────────────────────────────────

def extract_url_from_content(path):
    """Extract the URL field from markdown content."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.search(r'\*\*URL:\*\*\s*<?([^>\s]+)>?', line)
                if m:
                    return m.group(1).strip()
    except Exception:
        pass
    return None


def url_to_html_filename(url):
    """Convert a ziatile.com URL to the HTML filename used in html/original/ and html/revised/."""
    path = url.split("//", 1)[-1]
    path = path.split("?")[0]  # Strip query params
    path = path.replace("ziatile.com/", "").replace("en-ca/", "")
    path = path.strip("/").replace("/", "--")
    return (path or "homepage") + ".html"


def build_html_mapping():
    """Build a mapping from markdown content paths to their original/revised HTML counterparts."""
    html_dir = CLIENTS_DIR / "zia-tile" / "campaigns" / "01-product-collection-pages" / "html"
    original_dir = html_dir / "original"
    revised_dir = html_dir / "revised"

    if not original_dir.exists():
        return {}

    available_originals = {f.name for f in original_dir.iterdir() if f.suffix == ".html"}
    available_revised = {f.name for f in revised_dir.iterdir() if f.suffix == ".html"} if revised_dir.exists() else set()

    mapping = {}
    gdocs_dir = CLIENTS_DIR / "zia-tile" / "campaigns" / "01-product-collection-pages" / "gdocs-content"

    if not gdocs_dir.exists():
        return mapping

    for md_file in gdocs_dir.rglob("*.md"):
        url = extract_url_from_content(md_file)
        if not url:
            continue
        html_name = url_to_html_filename(url)

        # Build the content store key for this markdown file
        rel_from_campaign = md_file.relative_to(CLIENTS_DIR / "zia-tile" / "campaigns" / "01-product-collection-pages")
        store_key = f"clients/zia-tile/campaigns/01-product-collection-pages/{rel_from_campaign}"

        # Relative paths from reports/ directory (where the navigator HTML lives)
        html_rel_base = "../clients/zia-tile/campaigns/01-product-collection-pages/html"

        entry = {"siteUrl": url}
        if html_name in available_originals:
            entry["htmlOriginalPath"] = f"{html_rel_base}/original/{html_name}"
        if html_name in available_revised:
            entry["htmlRevisedPath"] = f"{html_rel_base}/revised/{html_name}"

        mapping[store_key] = entry

    return mapping


# ── Registry Generation ──────────────────────────────────────────────

def scan_directory(base_path, rel_root, allowed_exts=None):
    if allowed_exts is None:
        allowed_exts = {".md", ".html", ".json", ".py", ".js", ".css", ".txt"}
    entries = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in sorted(files):
            if fname.startswith(".") or fname == "registry.json":
                continue
            ext = Path(fname).suffix.lower()
            if ext not in allowed_exts:
                continue
            full = Path(root) / fname
            rel = full.relative_to(rel_root)
            ftype = detect_type(rel)
            cat = detect_category(rel, ftype)
            title = extract_title(full) if ext == ".md" else None
            display = title or slug_to_display(fname)
            size = full.stat().st_size
            mtime = datetime.fromtimestamp(full.stat().st_mtime).strftime("%Y-%m-%d")
            entries.append({
                "id": Path(fname).stem,
                "filename": fname,
                "displayName": display,
                "type": ftype,
                "category": cat,
                "status": "delivered",
                "version": 3 if "/v3/" in str(rel) else 1,
                "path": str(rel),
                "sizeBytes": size,
                "sizeHuman": human_size(size),
                "lastModified": mtime,
            })
    return entries


def generate_campaign_registry(client_name, campaign_path):
    campaign_name = campaign_path.name
    entries = scan_directory(campaign_path, campaign_path)
    registry = {
        "client": client_name,
        "campaign": campaign_name,
        "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "totalFiles": len(entries),
        "entries": entries,
    }
    out = campaign_path / "registry.json"
    with open(out, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"  Campaign registry: {out.relative_to(ROOT)} ({len(entries)} entries)")
    return registry


def generate_client_registry(client_name, client_path):
    entries = []
    style = client_path / "STYLE-SYSTEM.md"
    if style.exists():
        title = extract_title(style)
        entries.append({
            "id": "style-system",
            "filename": "STYLE-SYSTEM.md",
            "displayName": title or f"{slug_to_display(client_name)} Style System",
            "type": "style-system",
            "category": "style-system",
            "status": "active",
            "version": 1,
            "path": "STYLE-SYSTEM.md",
            "sizeBytes": style.stat().st_size,
            "sizeHuman": human_size(style.stat().st_size),
            "lastModified": datetime.fromtimestamp(style.stat().st_mtime).strftime("%Y-%m-%d"),
        })
    raw_dir = client_path / "raw"
    if raw_dir.exists():
        entries.extend(scan_directory(raw_dir, client_path))
    ref_dir = client_path / "reference-site"
    if ref_dir.exists():
        entries.extend(scan_directory(ref_dir, client_path))
    registry = {
        "client": client_name,
        "scope": "client",
        "generatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "totalFiles": len(entries),
        "entries": entries,
    }
    out = client_path / "registry.json"
    with open(out, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"  Client registry: {out.relative_to(ROOT)} ({len(entries)} entries)")
    return registry


def generate_all_registries():
    all_registries = {}
    for client_dir in sorted(CLIENTS_DIR.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith("."):
            continue
        client_name = client_dir.name
        print(f"\n[{client_name}]")
        client_reg = generate_client_registry(client_name, client_dir)
        campaign_regs = []
        campaigns_dir = client_dir / "campaigns"
        if campaigns_dir.exists():
            for camp_dir in sorted(campaigns_dir.iterdir()):
                if camp_dir.is_dir() and not camp_dir.name.startswith("."):
                    campaign_regs.append(generate_campaign_registry(client_name, camp_dir))
        all_registries[client_name] = {
            "client": client_reg,
            "campaigns": campaign_regs,
        }
    return all_registries


# ── Content Store ────────────────────────────────────────────────────

def build_content_store(registries):
    store = {}
    changed_files = get_changed_files()
    comparison_count = 0

    for client_name, data in registries.items():
        client_dir = CLIENTS_DIR / client_name
        for entry in data["client"]["entries"]:
            fpath = client_dir / entry["path"]
            ext = Path(entry["filename"]).suffix.lower()
            if ext in (".md", ".html", ".txt", ".css", ".js", ".py"):
                key = f"clients/{client_name}/{entry['path']}"
                store[key] = {
                    "displayName": entry["displayName"],
                    "type": entry["type"],
                    "category": entry["category"],
                    "status": entry["status"],
                    "size": entry["sizeHuman"],
                    "lastModified": entry["lastModified"],
                    "content": read_content(fpath),
                    "isHtml": ext == ".html",
                }
                if ext == ".md" and key in changed_files:
                    original = get_pre_patch_content(key)
                    if original and original != store[key]["content"]:
                        store[key]["originalContent"] = original
                        store[key]["hasComparison"] = True
                        comparison_count += 1
        for camp_reg in data["campaigns"]:
            camp_name = camp_reg["campaign"]
            camp_dir = client_dir / "campaigns" / camp_name
            for entry in camp_reg["entries"]:
                fpath = camp_dir / entry["path"]
                ext = Path(entry["filename"]).suffix.lower()
                if ext in (".md", ".html", ".txt"):
                    key = f"clients/{client_name}/campaigns/{camp_name}/{entry['path']}"
                    store[key] = {
                        "displayName": entry["displayName"],
                        "type": entry["type"],
                        "category": entry["category"],
                        "status": entry["status"],
                        "size": entry["sizeHuman"],
                        "lastModified": entry["lastModified"],
                        "content": read_content(fpath),
                        "isHtml": ext == ".html",
                    }
                    if ext == ".md" and key in changed_files:
                        original = get_pre_patch_content(key)
                        if original and original != store[key]["content"]:
                            store[key]["originalContent"] = original
                            store[key]["hasComparison"] = True
                            comparison_count += 1

    if comparison_count:
        print(f"  {comparison_count} files have before/after comparisons")

    # Attach HTML original/revised paths
    html_map = build_html_mapping()
    matched = 0
    for key, meta in html_map.items():
        if key in store:
            store[key].update(meta)
            matched += 1
    if matched:
        print(f"  {matched} files mapped to site HTML (original/revised)")

    return store


# ── HTML Builder ─────────────────────────────────────────────────────

def build_html(registries, content_store):
    reg_json = json.dumps(registries, ensure_ascii=False).replace("</", "<\\/")
    store_json = json.dumps(content_store, ensure_ascii=False).replace("</", "<\\/")

    today = datetime.now().strftime("%Y-%m-%d")

    # Count stats
    total_files = 0
    total_bytes = 0
    total_campaigns = 0
    for data in registries.values():
        total_files += data["client"]["totalFiles"]
        for c in data["campaigns"]:
            total_files += c["totalFiles"]
            total_campaigns += 1
        for entry in data["client"]["entries"]:
            total_bytes += entry["sizeBytes"]
        for c in data["campaigns"]:
            for entry in c["entries"]:
                total_bytes += entry["sizeBytes"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Content Ops — Client Navigator</title>
<style>
:root {{
  --bg: #ffffff;
  --bg-alt: #f8f9fa;
  --bg-hover: #f0f1f3;
  --border: #e2e4e8;
  --text: #1a1a1a;
  --text-muted: #6b7280;
  --accent: #2563eb;
  --accent-light: #dbeafe;
  --green: #059669;
  --green-light: #d1fae5;
  --orange: #d97706;
  --orange-light: #fef3c7;
  --purple: #7c3aed;
  --purple-light: #ede9fe;
  --red: #dc2626;
  --red-light: #fee2e2;
  --cyan: #0891b2;
  --cyan-light: #cffafe;
  --pink: #be185d;
  --pink-light: #fce7f3;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-lg: 0 4px 12px rgba(0,0,0,0.1);
  --preview-width: 52%;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  background: var(--bg-alt); color: var(--text); line-height: 1.55; font-size: 14px;
}}

/* ── Header ── */
.header {{
  background: var(--bg); border-bottom: 1px solid var(--border);
  padding: 16px 28px; position: sticky; top: 0; z-index: 100; box-shadow: var(--shadow);
}}
.header-inner {{
  max-width: 1600px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
}}
.header h1 {{ font-size: 18px; font-weight: 700; white-space: nowrap; }}
.header h1 span {{ color: var(--text-muted); font-weight: 400; }}
.search-box {{ flex: 1; max-width: 380px; position: relative; }}
.search-box input {{
  width: 100%; padding: 7px 12px 7px 34px;
  border: 1px solid var(--border); border-radius: var(--radius);
  font-size: 13px; background: var(--bg-alt); color: var(--text); outline: none;
}}
.search-box input:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-light); }}
.search-icon {{ position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 14px; opacity: 0.45; }}
.gen-date {{ font-size: 11px; color: var(--text-muted); white-space: nowrap; }}
.kbd {{ display: inline-block; padding: 1px 5px; border: 1px solid var(--border); border-radius: 3px; font-size: 11px; color: var(--text-muted); background: var(--bg-alt); margin-left: 6px; }}

/* ── Layout ── */
.container {{ max-width: 1600px; margin: 0 auto; padding: 20px 28px; transition: padding-right 0.3s; }}
body.preview-open .container {{ padding-right: calc(var(--preview-width) + 28px); }}

/* ── Stats ── */
.stats-bar {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px; }}
.stat-card {{ background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px; box-shadow: var(--shadow); }}
.stat-card .sv {{ font-size: 26px; font-weight: 700; line-height: 1.1; }}
.stat-card .sl {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.4px; margin-top: 3px; }}

/* ── Client sections ── */
.client-section {{ background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: 16px; box-shadow: var(--shadow); overflow: hidden; }}
.client-hdr {{ display: flex; align-items: center; gap: 14px; padding: 16px 20px; cursor: pointer; user-select: none; }}
.client-hdr:hover {{ background: var(--bg-hover); }}
.client-logo {{ width: 42px; height: 42px; border-radius: var(--radius); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: #fff; flex-shrink: 0; }}
.client-hdr-text {{ flex: 1; }}
.client-hdr-text h2 {{ font-size: 16px; font-weight: 600; }}
.client-hdr-text p {{ font-size: 12px; color: var(--text-muted); }}
.badges {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.badge {{ display: inline-flex; align-items: center; gap: 3px; padding: 3px 9px; border-radius: 16px; font-size: 11px; font-weight: 500; white-space: nowrap; }}
.b-green {{ background: var(--green-light); color: var(--green); }}
.b-blue {{ background: var(--accent-light); color: var(--accent); }}
.b-orange {{ background: var(--orange-light); color: var(--orange); }}
.b-purple {{ background: var(--purple-light); color: var(--purple); }}
.b-pink {{ background: var(--pink-light); color: var(--pink); }}
.b-cyan {{ background: var(--cyan-light); color: var(--cyan); }}
.chev {{ font-size: 16px; transition: transform 0.2s; color: var(--text-muted); }}
.client-section.open .chev {{ transform: rotate(90deg); }}
.client-body {{ display: none; border-top: 1px solid var(--border); }}
.client-section.open .client-body {{ display: block; }}

/* ── Tabs ── */
.tab-nav {{ display: flex; border-bottom: 1px solid var(--border); padding: 0 20px; background: var(--bg-alt); overflow-x: auto; }}
.tab-btn {{ padding: 9px 14px; font-size: 12px; font-weight: 500; color: var(--text-muted); border: none; background: none; cursor: pointer; border-bottom: 2px solid transparent; white-space: nowrap; }}
.tab-btn:hover {{ color: var(--text); }}
.tab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
.tc {{ display: inline-flex; align-items: center; justify-content: center; min-width: 16px; height: 16px; padding: 0 4px; border-radius: 8px; background: var(--border); font-size: 10px; font-weight: 600; margin-left: 5px; }}
.tab-btn.active .tc {{ background: var(--accent-light); color: var(--accent); }}
.tab-panel {{ display: none; padding: 16px 20px; }}
.tab-panel.active {{ display: block; }}

/* ── Type Cards (Overview) ── */
.type-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; }}
.type-card {{
  border: 1px solid var(--border); border-radius: var(--radius); padding: 14px;
  cursor: pointer; transition: box-shadow 0.15s, border-color 0.15s;
}}
.type-card:hover {{ box-shadow: var(--shadow-lg); border-color: var(--accent); }}
.type-card.expanded {{ border-color: var(--accent); background: var(--accent-light); }}
.type-card h4 {{ font-size: 13px; font-weight: 600; margin-bottom: 2px; }}
.type-card .tn {{ font-size: 24px; font-weight: 700; line-height: 1.2; }}
.type-card .td {{ font-size: 11px; color: var(--text-muted); }}
.type-section-label {{ font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); padding: 8px 0 4px; }}

/* ── Category Expansion ── */
.cat-expansion {{
  grid-column: 1 / -1; border: 1px solid var(--accent); border-radius: var(--radius);
  background: var(--bg); padding: 12px; margin-top: 4px; display: none;
  max-height: 500px; overflow: hidden; display: flex; flex-direction: column;
}}
.cat-expansion.open {{ display: flex; }}
.cat-filter {{
  width: 100%; padding: 6px 10px; border: 1px solid var(--border); border-radius: 4px;
  font-size: 12px; margin-bottom: 8px; outline: none;
}}
.cat-filter:focus {{ border-color: var(--accent); }}
.cat-file-list {{ overflow-y: auto; flex: 1; max-height: 420px; }}
.cat-file {{
  display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 4px;
  cursor: pointer; font-size: 12px; transition: background 0.1s;
}}
.cat-file:hover {{ background: var(--bg-hover); }}
.cat-file.active {{ background: var(--accent-light); }}
.cat-file .cf-name {{ flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 500; }}
.cat-file .cf-size {{ font-size: 11px; color: var(--text-muted); font-variant-numeric: tabular-nums; }}
.cat-file .cf-type {{ font-size: 9px; padding: 1px 5px; border-radius: 3px; font-weight: 600; text-transform: uppercase; }}

/* ── File Tree ── */
.file-tree {{ font-size: 13px; }}
.tree-folder {{ margin-bottom: 2px; }}
.tfh {{ display: flex; align-items: center; gap: 6px; padding: 5px 8px; border-radius: 4px; cursor: pointer; user-select: none; }}
.tfh:hover {{ background: var(--bg-hover); }}
.tfh .fi {{ font-size: 13px; transition: transform 0.15s; width: 14px; text-align: center; }}
.tree-folder.open > .tfh .fi {{ transform: rotate(90deg); }}
.tfh .fn {{ font-weight: 500; }}
.tfh .fc {{ font-size: 11px; color: var(--text-muted); margin-left: auto; }}
.tree-children {{ display: none; padding-left: 18px; border-left: 1px solid var(--border); margin-left: 10px; }}
.tree-folder.open > .tree-children {{ display: block; }}
.tf {{
  display: flex; align-items: center; gap: 7px; padding: 4px 8px; border-radius: 4px;
  cursor: pointer; transition: background 0.1s;
}}
.tf:hover {{ background: var(--bg-hover); }}
.tf.active {{ background: var(--accent-light); }}
.tf .fi {{ font-size: 12px; width: 14px; text-align: center; opacity: 0.55; }}
.tf .fn {{ flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.tf .fs {{ font-size: 11px; color: var(--text-muted); font-variant-numeric: tabular-nums; white-space: nowrap; }}
.ft {{ font-size: 9px; padding: 1px 5px; border-radius: 3px; font-weight: 600; text-transform: uppercase; }}
.ft-md {{ background: #dbeafe; color: #1d4ed8; }}
.ft-html {{ background: #fce7f3; color: #be185d; }}
.ft-py {{ background: #d1fae5; color: #065f46; }}
.ft-js {{ background: #fef9c3; color: #854d0e; }}
.ft-css {{ background: #ede9fe; color: #5b21b6; }}
.ft-json {{ background: #fef3c7; color: #92400e; }}

/* ── Preview Pane ── */
.preview-pane {{
  position: fixed; top: 0; right: 0; width: var(--preview-width); height: 100vh;
  background: var(--bg); border-left: 1px solid var(--border);
  box-shadow: -4px 0 24px rgba(0,0,0,0.08);
  z-index: 200; display: flex; flex-direction: column;
  transform: translateX(100%); transition: transform 0.25s ease;
}}
.preview-pane.open {{ transform: translateX(0); }}
.preview-header {{
  padding: 14px 20px; border-bottom: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 8px; flex-shrink: 0; background: var(--bg-alt);
}}
.preview-top {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }}
.preview-title {{ font-size: 15px; font-weight: 600; flex: 1; line-height: 1.3; }}
.close-btn {{
  width: 28px; height: 28px; border: 1px solid var(--border); border-radius: 4px;
  background: var(--bg); font-size: 16px; cursor: pointer; display: flex;
  align-items: center; justify-content: center; flex-shrink: 0; color: var(--text-muted);
}}
.close-btn:hover {{ background: var(--bg-hover); color: var(--text); }}
.preview-meta {{ display: flex; align-items: center; gap: 6px; flex-wrap: wrap; font-size: 11px; }}
.preview-nav {{
  display: flex; align-items: center; gap: 8px; padding-top: 6px; border-top: 1px solid var(--border);
}}
.nav-btn {{
  padding: 4px 10px; border: 1px solid var(--border); border-radius: 4px;
  background: var(--bg); font-size: 12px; cursor: pointer; color: var(--text);
}}
.nav-btn:hover {{ background: var(--bg-hover); }}
.nav-btn:disabled {{ opacity: 0.3; cursor: default; }}
.nav-pos {{ font-size: 11px; color: var(--text-muted); flex: 1; text-align: center; }}
.preview-path {{
  font-size: 11px; color: var(--text-muted); font-family: 'SF Mono', 'Fira Code', monospace;
  word-break: break-all;
}}
.preview-body {{
  flex: 1; overflow-y: auto; padding: 20px 24px;
}}

/* ── Rendered Markdown ── */
.preview-body h1 {{ font-size: 22px; font-weight: 700; margin: 0 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }}
.preview-body h2 {{ font-size: 18px; font-weight: 600; margin: 20px 0 8px; }}
.preview-body h3 {{ font-size: 15px; font-weight: 600; margin: 16px 0 6px; }}
.preview-body h4 {{ font-size: 13px; font-weight: 600; margin: 14px 0 4px; }}
.preview-body p {{ margin: 0 0 10px; line-height: 1.65; }}
.preview-body ul, .preview-body ol {{ margin: 0 0 10px; padding-left: 24px; }}
.preview-body li {{ margin-bottom: 4px; line-height: 1.55; }}
.preview-body blockquote {{ border-left: 3px solid var(--accent); padding: 8px 16px; margin: 0 0 12px; color: var(--text-muted); background: var(--bg-alt); border-radius: 0 4px 4px 0; }}
.preview-body code {{ font-family: 'SF Mono', 'Fira Code', monospace; font-size: 12px; background: var(--bg-alt); padding: 1px 4px; border-radius: 3px; }}
.preview-body pre {{ background: #1e293b; color: #e2e8f0; padding: 14px; border-radius: var(--radius); overflow-x: auto; margin: 0 0 12px; font-size: 12px; line-height: 1.5; }}
.preview-body pre code {{ background: none; padding: 0; color: inherit; }}
.preview-body table {{ border-collapse: collapse; width: 100%; margin: 0 0 12px; font-size: 13px; }}
.preview-body th {{ text-align: left; padding: 8px 10px; border-bottom: 2px solid var(--border); font-weight: 600; background: var(--bg-alt); }}
.preview-body td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); }}
.preview-body hr {{ border: none; border-top: 1px solid var(--border); margin: 16px 0; }}
.preview-body a {{ color: var(--accent); text-decoration: none; }}
.preview-body a:hover {{ text-decoration: underline; }}
.preview-body strong {{ font-weight: 600; }}
.preview-body img {{ max-width: 100%; border-radius: 4px; }}

/* Raw preview (HTML files or no marked.js) */
.raw-preview {{ font-family: 'SF Mono', 'Fira Code', monospace; font-size: 12px; white-space: pre-wrap; word-wrap: break-word; line-height: 1.5; color: var(--text); }}

/* ── Preview Tabs ── */
.preview-tabs {{
  display: flex; border-bottom: 1px solid var(--border);
  background: var(--bg); flex-shrink: 0;
}}
.preview-tab-btn {{
  padding: 8px 16px; font-size: 12px; font-weight: 500;
  color: var(--text-muted); border: none; background: none;
  cursor: pointer; border-bottom: 2px solid transparent;
  white-space: nowrap; transition: color 0.15s;
}}
.preview-tab-btn:hover {{ color: var(--text); }}
.preview-tab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
.preview-tab-btn .change-dot {{
  display: inline-block; width: 6px; height: 6px;
  background: var(--orange); border-radius: 50%; margin-left: 4px; vertical-align: middle;
}}
.md-source {{
  font-family: 'SF Mono', 'Fira Code', monospace; font-size: 12px;
  white-space: pre-wrap; word-wrap: break-word; line-height: 1.6;
  color: var(--text); background: var(--bg-alt); padding: 16px;
  border-radius: var(--radius);
}}

/* ── Preview Actions (HTML page links) ── */
.preview-actions {{
  display: flex; gap: 8px; padding: 10px 20px; border-bottom: 1px solid var(--border);
  background: var(--bg-alt); flex-shrink: 0; flex-wrap: wrap; align-items: center;
}}
.page-link-btn {{
  display: inline-flex; align-items: center; gap: 5px;
  padding: 6px 14px; border: 1px solid var(--border); border-radius: var(--radius);
  background: var(--bg); font-size: 12px; font-weight: 500; color: var(--text);
  cursor: pointer; text-decoration: none; transition: all 0.15s;
}}
.page-link-btn:hover {{ border-color: var(--accent); color: var(--accent); box-shadow: var(--shadow); }}
.page-link-btn.original {{ border-left: 3px solid var(--orange); }}
.page-link-btn.revised {{ border-left: 3px solid var(--green); }}
.page-link-btn.not-revised {{
  border-left: 3px solid var(--red); color: var(--text-muted);
  cursor: default; font-style: italic;
}}
.page-link-btn .icon {{ font-size: 14px; }}
.revise-btn {{
  display: inline-flex; align-items: center; gap: 5px;
  padding: 6px 14px; border: 1px solid var(--accent); border-radius: var(--radius);
  background: var(--accent); font-size: 12px; font-weight: 600; color: #fff;
  cursor: pointer; transition: all 0.15s; margin-left: auto;
}}
.revise-btn:hover {{ background: #1d4ed8; }}
.actions-label {{
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px;
  color: var(--text-muted); font-weight: 600; margin-right: 4px;
}}
.revision-modal {{
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); z-index: 1000;
  display: flex; align-items: center; justify-content: center;
}}
.revision-modal-content {{
  background: var(--bg); border-radius: var(--radius); padding: 24px;
  max-width: 600px; width: 90%; box-shadow: var(--shadow-lg);
}}
.revision-modal h3 {{ font-size: 16px; margin-bottom: 12px; }}
.revision-modal p {{ font-size: 13px; color: var(--text-muted); margin-bottom: 12px; }}
.revision-modal pre {{
  background: #1e293b; color: #e2e8f0; padding: 12px; border-radius: var(--radius);
  font-size: 12px; white-space: pre-wrap; word-break: break-all; margin-bottom: 16px;
}}
.revision-modal .btn-row {{ display: flex; gap: 8px; justify-content: flex-end; }}
.revision-modal button {{
  padding: 6px 16px; border-radius: var(--radius); font-size: 13px; cursor: pointer;
}}
.revision-modal .copy-btn {{ background: var(--accent); color: #fff; border: none; font-weight: 600; }}
.revision-modal .close-modal-btn {{ background: var(--bg-alt); border: 1px solid var(--border); color: var(--text); }}

/* ── Empty state ── */
.empty {{ padding: 40px; text-align: center; color: var(--text-muted); font-size: 13px; }}

/* ── Responsive ── */
@media (max-width: 900px) {{
  :root {{ --preview-width: 85%; }}
  .header-inner {{ flex-wrap: wrap; }}
  .search-box {{ max-width: 100%; order: 10; }}
  .container {{ padding: 14px; }}
  .stats-bar {{ grid-template-columns: repeat(3, 1fr); }}
}}
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <h1>Content Ops <span>Client Navigator</span></h1>
    <div class="search-box">
      <span class="search-icon">&#128269;</span>
      <input type="text" id="globalSearch" placeholder="Search files and content..." autocomplete="off">
      <span class="kbd">/</span>
    </div>
    <div class="gen-date">Generated {today}</div>
  </div>
</div>

<div class="container" id="container">
  <div class="stats-bar">
    <div class="stat-card"><div class="sv">{len(registries)}</div><div class="sl">Clients</div></div>
    <div class="stat-card"><div class="sv">{total_campaigns}</div><div class="sl">Campaigns</div></div>
    <div class="stat-card"><div class="sv">{total_files}</div><div class="sl">Files</div></div>
    <div class="stat-card"><div class="sv">{human_size(total_bytes)}</div><div class="sl">Total Content</div></div>
    <div class="stat-card"><div class="sv">{len(content_store)}</div><div class="sl">Previewable</div></div>
  </div>
  <div id="clientSections"></div>
</div>

<div class="preview-pane" id="previewPane">
  <div class="preview-header">
    <div class="preview-top">
      <div class="preview-title" id="previewTitle"></div>
      <button class="close-btn" onclick="closePreview()" title="Close (Esc)">&times;</button>
    </div>
    <div class="preview-meta" id="previewMeta"></div>
    <div class="preview-path" id="previewPath"></div>
    <div class="preview-nav">
      <button class="nav-btn" id="prevBtn" onclick="navPreview(-1)">&larr; Prev</button>
      <span class="nav-pos" id="navPos"></span>
      <button class="nav-btn" id="nextBtn" onclick="navPreview(1)">Next &rarr;</button>
    </div>
  </div>
  <div class="preview-actions" id="previewActions" style="display:none"></div>
  <div class="preview-tabs" id="previewTabs" style="display:none"></div>
  <div class="preview-body" id="previewBody"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script>
// Fallback if marked.js fails to load
if (typeof marked === 'undefined') {{
  window.marked = {{ parse: function(md) {{ return '<pre class="raw-preview">' + md.replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</pre>'; }} }};
}} else {{
  marked.use({{ breaks: true, gfm: true }});
}}

// ── Data (injected at build time) ──
const REGISTRIES = {reg_json};
const CONTENT = {store_json};

// ── Render helpers ──
const TYPE_COLORS = {{
  'product-page': 'var(--purple)', 'collection-page': 'var(--accent)',
  'draft': 'var(--green)', 'draft-v3': 'var(--green)',
  'transcript': 'var(--orange)', 'research': 'var(--cyan)',
  'product-spec': 'var(--accent)', 'competitor': 'var(--red)',
  'fact': 'var(--green)', 'proof': 'var(--orange)',
  'testimonial': 'var(--purple)', 'reference': 'var(--pink)',
  'style-system': 'var(--purple)', 'brief': 'var(--cyan)',
  'audit': 'var(--orange)', 'blog': 'var(--green)',
  'campaign-urls': 'var(--text-muted)', 'other': 'var(--text-muted)',
}};

const TYPE_LABELS = {{
  'product-page': 'Product Pages', 'collection-page': 'Collection Pages',
  'draft': 'Drafts', 'draft-v3': 'V3 Revisions',
  'transcript': 'Transcripts', 'research': 'Research',
  'product-spec': 'Products', 'competitor': 'Competitors',
  'fact': 'Facts', 'proof': 'Proof Studies',
  'testimonial': 'Testimonials', 'reference': 'Reference Site',
  'style-system': 'Style System', 'brief': 'Briefs',
  'audit': 'Audit Reports', 'campaign-urls': 'URL Maps',
  'blog': 'Blog Posts', 'other': 'Other',
}};

const TYPE_DESCS = {{
  'product-page': 'Individual SKU product detail pages',
  'collection-page': 'Category, color, shape, and space filter pages',
  'draft': 'Working drafts of collection page templates',
  'draft-v3': 'Revised v3 drafts for collections 09-16',
  'transcript': 'Client meeting transcripts',
  'research': 'Website, editorial, and technical research',
  'product-spec': 'Product specification sheets',
  'competitor': 'Competitor profile and positioning data',
  'fact': 'Verified claims, metrics, and specs',
  'proof': 'Case studies and proof points',
  'testimonial': 'Customer quotes with context',
  'reference': 'HTML reference pages and assets',
  'style-system': 'Brand style system and guidelines',
  'brief': 'Campaign briefs',
  'audit': 'Content audit findings',
  'campaign-urls': 'Target URL mappings',
}};

const CLIENT_META = {{
  'zia-tile': {{ name: 'Zia Tile', desc: 'Premium artisanal tile & stone retailer', color: '#7c3aed', initials: 'ZT' }},
  'searchatlas': {{ name: 'SearchAtlas', desc: 'B2B SEO & AI visibility platform', color: '#2563eb', initials: 'SA' }},
}};

function badgeClass(type) {{
  const map = {{'product-page':'b-purple','collection-page':'b-blue','draft':'b-green','draft-v3':'b-green','transcript':'b-orange','research':'b-cyan','product-spec':'b-blue','competitor':'b-pink','fact':'b-green','proof':'b-orange','testimonial':'b-purple','reference':'b-pink','style-system':'b-purple','brief':'b-cyan','audit':'b-orange'}};
  return map[type] || 'b-blue';
}}

function ftClass(ext) {{
  return {{'md':'ft-md','html':'ft-html','py':'ft-py','js':'ft-js','css':'ft-css','json':'ft-json'}}[ext] || 'ft-md';
}}

// ── State ──
let currentList = [];
let currentIndex = 0;
let activeFileEl = null;

// ── Build client sections ──
function buildUI() {{
  const container = document.getElementById('clientSections');
  let html = '';

  for (const [clientId, data] of Object.entries(REGISTRIES)) {{
    const meta = CLIENT_META[clientId] || {{ name: clientId, desc: '', color: '#666', initials: clientId.substring(0,2).toUpperCase() }};
    const allEntries = [...data.client.entries];
    data.campaigns.forEach(c => allEntries.push(...c.entries));
    const totalFiles = allEntries.length;
    const totalSize = allEntries.reduce((s, e) => s + e.sizeBytes, 0);

    // Group by type
    const byType = {{}};
    allEntries.forEach(e => {{
      if (!byType[e.type]) byType[e.type] = [];
      byType[e.type].push(e);
    }});

    const isFirst = clientId === Object.keys(REGISTRIES)[0];

    html += `<div class="client-section ${{isFirst ? 'open' : ''}}" id="cs-${{clientId}}">`;
    html += `<div class="client-hdr" onclick="this.closest('.client-section').classList.toggle('open')">`;
    html += `<div class="client-logo" style="background:${{meta.color}}">${{meta.initials}}</div>`;
    html += `<div class="client-hdr-text"><h2>${{meta.name}}</h2><p>${{meta.desc}}</p></div>`;
    html += `<div class="badges"><span class="badge b-green">Active</span><span class="badge b-purple">${{totalFiles}} files</span><span class="badge b-orange">${{humanSize(totalSize)}}</span></div>`;
    html += `<span class="chev">&#9654;</span></div>`;

    // Tabs
    const tabDefs = [{{ id: 'overview', label: 'Overview' }}];
    data.campaigns.forEach((c, i) => {{
      tabDefs.push({{ id: `camp-${{i}}`, label: c.campaign.replace(/^\\d+-/, '').replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase()), count: c.totalFiles }});
    }});
    // Add type-based tabs for raw materials
    const rawTypes = ['product-spec','competitor','fact','proof','testimonial','transcript','research','reference'];
    rawTypes.forEach(t => {{
      if (byType[t] && byType[t].length > 0) {{
        tabDefs.push({{ id: `type-${{t}}`, label: TYPE_LABELS[t] || t, count: byType[t].length }});
      }}
    }});

    html += `<div class="client-body">`;
    html += `<div class="tab-nav">`;
    tabDefs.forEach((td, i) => {{
      html += `<button class="tab-btn ${{i === 0 ? 'active' : ''}}" onclick="switchTab(this,'${{clientId}}-${{td.id}}')">${{td.label}}${{td.count ? '<span class=tc>' + td.count + '</span>' : ''}}</button>`;
    }});
    html += `</div>`;

    // Overview panel
    html += `<div class="tab-panel active" id="${{clientId}}-overview">`;

    const contentTypes = ['product-page','collection-page','draft','draft-v3','blog'];
    const vaultTypes = ['transcript','research','reference','product-spec','competitor','fact','proof','testimonial','brief','audit','campaign-urls','style-system','other'];
    const typeOrder = [...contentTypes, ...vaultTypes];

    // Pages & Content section
    const hasContent = contentTypes.some(t => byType[t] && byType[t].length > 0);
    if (hasContent) {{
      html += `<div class="type-section-label">Pages & Content</div>`;
      html += `<div class="type-grid" id="tg-${{clientId}}-content">`;
      contentTypes.forEach(t => {{
        if (!byType[t] || byType[t].length === 0) return;
        const color = TYPE_COLORS[t] || 'var(--text-muted)';
        html += `<div class="type-card" onclick="expandCategory('${{clientId}}','${{t}}')" id="tc-${{clientId}}-${{t}}">`;
        html += `<div class="tn" style="color:${{color}}">${{byType[t].length}}</div>`;
        html += `<h4>${{TYPE_LABELS[t] || t}}</h4>`;
        html += `<div class="td">${{TYPE_DESCS[t] || ''}}</div>`;
        html += `</div>`;
      }});
      html += `</div>`;
    }}

    // Brand Vault section
    const hasVault = vaultTypes.some(t => byType[t] && byType[t].length > 0);
    if (hasVault) {{
      html += `<div class="type-section-label" style="margin-top:16px">Brand Vault</div>`;
      html += `<div class="type-grid" id="tg-${{clientId}}-vault">`;
      vaultTypes.forEach(t => {{
        if (!byType[t] || byType[t].length === 0) return;
        const color = TYPE_COLORS[t] || 'var(--text-muted)';
        html += `<div class="type-card" onclick="expandCategory('${{clientId}}','${{t}}')" id="tc-${{clientId}}-${{t}}">`;
        html += `<div class="tn" style="color:${{color}}">${{byType[t].length}}</div>`;
        html += `<h4>${{TYPE_LABELS[t] || t}}</h4>`;
        html += `<div class="td">${{TYPE_DESCS[t] || ''}}</div>`;
        html += `</div>`;
      }});
      html += `</div>`;
    }}

    html += `<div id="cat-exp-${{clientId}}" style="margin-top:10px"></div>`;
    html += `</div>`;

    // Campaign panels
    data.campaigns.forEach((c, i) => {{
      html += `<div class="tab-panel" id="${{clientId}}-camp-${{i}}">`;
      // Group campaign entries by type
      const campByType = {{}};
      c.entries.forEach(e => {{
        if (!campByType[e.type]) campByType[e.type] = [];
        campByType[e.type].push(e);
      }});
      html += `<div class="file-tree">`;
      typeOrder.forEach(t => {{
        if (!campByType[t] || campByType[t].length === 0) return;
        html += `<div class="tree-folder open"><div class="tfh" onclick="this.closest('.tree-folder').classList.toggle('open')"><span class="fi">&#9654;</span><span class="fn">${{TYPE_LABELS[t] || t}}</span><span class="fc">${{campByType[t].length}} files</span></div>`;
        html += `<div class="tree-children">`;
        campByType[t].forEach(e => {{
          const key = `clients/${{clientId}}/campaigns/${{c.campaign}}/${{e.path}}`;
          const ext = e.filename.split('.').pop();
          html += `<div class="tf" onclick="openPreviewFromEntry('${{clientId}}','${{c.campaign}}','${{t}}',${{JSON.stringify(e.id).replace(/'/g,"\\\\'")}},this)" data-key="${{encodeKey(key)}}">`;
          html += `<span class="fi">&#128196;</span><span class="fn">${{e.displayName}}</span><span class="ft ${{ftClass(ext)}}">${{ext}}</span><span class="fs">${{e.sizeHuman}}</span>`;
          html += `</div>`;
        }});
        html += `</div></div>`;
      }});
      html += `</div></div>`;
    }});

    // Type panels (for raw material tabs)
    rawTypes.forEach(t => {{
      if (!byType[t] || byType[t].length === 0) return;
      html += `<div class="tab-panel" id="${{clientId}}-type-${{t}}">`;
      html += `<div class="file-tree"><div class="tree-folder open">`;
      html += `<div class="tfh"><span class="fi">&#9654;</span><span class="fn">${{TYPE_LABELS[t]}}</span><span class="fc">${{byType[t].length}} files</span></div>`;
      html += `<div class="tree-children">`;
      byType[t].forEach(e => {{
        const key = `clients/${{clientId}}/${{e.path}}`;
        const ext = e.filename.split('.').pop();
        html += `<div class="tf" onclick="openPreviewDirect('${{encodeKey(key)}}',this)" data-key="${{encodeKey(key)}}">`;
        html += `<span class="fi">&#128196;</span><span class="fn">${{e.displayName}}</span><span class="ft ${{ftClass(ext)}}">${{ext}}</span><span class="fs">${{e.sizeHuman}}</span>`;
        html += `</div>`;
      }});
      html += `</div></div></div></div>`;
    }});

    html += `</div></div>`;
  }}
  container.innerHTML = html;
}}

function humanSize(n) {{
  if (n < 1024) return n + ' B';
  if (n < 1024*1024) return (n/1024).toFixed(1) + ' KB';
  return (n/(1024*1024)).toFixed(1) + ' MB';
}}

function encodeKey(k) {{ return btoa(unescape(encodeURIComponent(k))); }}
function decodeKey(k) {{ return decodeURIComponent(escape(atob(k))); }}

// ── Tab switching ──
function switchTab(btn, panelId) {{
  const body = btn.closest('.client-body');
  body.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  body.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  const panel = document.getElementById(panelId);
  if (panel) panel.classList.add('active');
}}

// ── Category expansion (in overview) ──
let openCat = null;
function expandCategory(clientId, type) {{
  const expContainer = document.getElementById('cat-exp-' + clientId);
  const cardId = 'tc-' + clientId + '-' + type;
  const card = document.getElementById(cardId);

  // Toggle off if same category
  if (openCat === cardId) {{
    expContainer.innerHTML = '';
    card.classList.remove('expanded');
    openCat = null;
    return;
  }}

  // Clear previous
  if (openCat) {{
    const prev = document.getElementById(openCat);
    if (prev) prev.classList.remove('expanded');
  }}
  card.classList.add('expanded');
  openCat = cardId;

  // Gather entries of this type for this client
  const data = REGISTRIES[clientId];
  const entries = [];
  data.client.entries.forEach(e => {{
    if (e.type === type) entries.push({{ ...e, scope: 'client', campaign: null }});
  }});
  data.campaigns.forEach(c => {{
    c.entries.forEach(e => {{
      if (e.type === type) entries.push({{ ...e, scope: 'campaign', campaign: c.campaign }});
    }});
  }});

  let html = '<div class="cat-expansion open">';
  html += `<input type="text" class="cat-filter" placeholder="Filter ${{entries.length}} ${{TYPE_LABELS[type] || type}}..." oninput="filterCatFiles(this)">`;
  html += '<div class="cat-file-list">';
  entries.forEach((e, i) => {{
    const key = e.scope === 'campaign'
      ? `clients/${{clientId}}/campaigns/${{e.campaign}}/${{e.path}}`
      : `clients/${{clientId}}/${{e.path}}`;
    html += `<div class="cat-file" onclick="openFromCat('${{clientId}}','${{type}}',${{i}},this)" data-key="${{encodeKey(key)}}" data-name="${{e.displayName.toLowerCase()}}">`;
    html += `<span class="cf-name">${{e.displayName}}</span>`;
    html += `<span class="badge ${{badgeClass(type)}}" style="font-size:10px">${{e.category}}</span>`;
    html += `<span class="cf-size">${{e.sizeHuman}}</span>`;
    html += '</div>';
  }});
  html += '</div></div>';
  expContainer.innerHTML = html;

  // Store list for nav
  window._catEntries = entries;
  window._catClientId = clientId;
  window._catType = type;
}}

function filterCatFiles(input) {{
  const q = input.value.toLowerCase();
  input.closest('.cat-expansion').querySelectorAll('.cat-file').forEach(f => {{
    f.style.display = f.dataset.name.includes(q) ? '' : 'none';
  }});
}}

function openFromCat(clientId, type, index, el) {{
  // Build the navigable list from category entries
  const entries = window._catEntries || [];
  currentList = entries.map(e => {{
    return e.scope === 'campaign'
      ? `clients/${{clientId}}/campaigns/${{e.campaign}}/${{e.path}}`
      : `clients/${{clientId}}/${{e.path}}`;
  }});
  currentIndex = index;
  setActiveEl(el);
  openPreview(currentList[currentIndex]);
}}

// ── Preview from file tree ──
function openPreviewFromEntry(clientId, campaign, type, entryId, el) {{
  // Build list of sibling files of same type in this campaign
  const campData = REGISTRIES[clientId].campaigns.find(c => c.campaign === campaign);
  if (!campData) return;
  const siblings = campData.entries.filter(e => e.type === type);
  currentList = siblings.map(e => `clients/${{clientId}}/campaigns/${{campaign}}/${{e.path}}`);
  currentIndex = siblings.findIndex(e => e.id === entryId);
  if (currentIndex < 0) currentIndex = 0;
  setActiveEl(el);
  openPreview(currentList[currentIndex]);
}}

function openPreviewDirect(encodedKey, el) {{
  const key = decodeKey(encodedKey);
  // Find siblings in the same folder
  const parentFolder = el.closest('.tree-children');
  if (parentFolder) {{
    const siblings = Array.from(parentFolder.querySelectorAll('.tf'));
    currentList = siblings.map(s => decodeKey(s.dataset.key));
    currentIndex = currentList.indexOf(key);
    if (currentIndex < 0) currentIndex = 0;
  }} else {{
    currentList = [key];
    currentIndex = 0;
  }}
  setActiveEl(el);
  openPreview(key);
}}

function setActiveEl(el) {{
  if (activeFileEl) activeFileEl.classList.remove('active');
  activeFileEl = el;
  if (el) el.classList.add('active');
}}

// ── Preview pane ──
function openPreview(key) {{
  const pane = document.getElementById('previewPane');
  const data = CONTENT[key];

  document.getElementById('previewTitle').textContent = data ? data.displayName : key.split('/').pop();
  document.getElementById('previewPath').textContent = key;

  // Meta badges
  let metaHtml = '';
  if (data) {{
    metaHtml += `<span class="badge ${{badgeClass(data.type)}}">${{TYPE_LABELS[data.type] || data.type}}</span>`;
    metaHtml += `<span class="badge b-blue">${{data.category}}</span>`;
    metaHtml += `<span class="badge b-orange">${{data.size}}</span>`;
    metaHtml += `<span style="color:var(--text-muted)">Modified ${{data.lastModified}}</span>`;
  }}
  document.getElementById('previewMeta').innerHTML = metaHtml;

  // Nav
  updateNav();

  // Content & tabs
  const body = document.getElementById('previewBody');
  const tabBar = document.getElementById('previewTabs');
  const actionsBar = document.getElementById('previewActions');

  window._previewData = data;
  window._previewKey = key;

  // Build actions bar (HTML page links)
  if (data && (data.htmlOriginalPath || data.htmlRevisedPath || data.siteUrl)) {{
    let actHtml = '<span class="actions-label">Site Pages</span>';

    if (data.htmlOriginalPath) {{
      actHtml += '<a class="page-link-btn original" href="' + data.htmlOriginalPath + '" target="_blank" title="Open original site page"><span class="icon">&#127760;</span> Original HTML</a>';
    }}

    if (data.htmlRevisedPath) {{
      actHtml += '<a class="page-link-btn revised" href="' + data.htmlRevisedPath + '" target="_blank" title="Open revised site page"><span class="icon">&#9989;</span> Revised HTML</a>';
    }} else if (data.htmlOriginalPath) {{
      actHtml += '<span class="page-link-btn not-revised"><span class="icon">&#9888;</span> Not Yet Revised</span>';
      actHtml += '<button class="revise-btn" onclick="showRevisionModal()"><span class="icon">&#9881;</span> Create Revision</button>';
    }}

    actionsBar.innerHTML = actHtml;
    actionsBar.style.display = 'flex';
  }} else {{
    actionsBar.style.display = 'none';
  }}

  // Preview tabs for markdown content
  if (!data) {{
    tabBar.style.display = 'none';
    body.innerHTML = '<div class="empty">Content not available for preview.</div>';
  }} else if (data.hasComparison) {{
    // 3-tab view: Original | Markdown | Revised
    tabBar.style.display = 'flex';
    tabBar.innerHTML =
      '<button class="preview-tab-btn active" onclick="switchPreviewTab(\\'original\\')">Original</button>' +
      '<button class="preview-tab-btn" onclick="switchPreviewTab(\\'markdown\\')">Markdown</button>' +
      '<button class="preview-tab-btn" onclick="switchPreviewTab(\\'revised\\')">Revised<span class="change-dot"></span></button>';
    switchPreviewTab('original');
  }} else if (!data.isHtml) {{
    // 2-tab view: Markdown | Rendered
    tabBar.style.display = 'flex';
    tabBar.innerHTML =
      '<button class="preview-tab-btn" onclick="switchPreviewTab(\\'markdown\\')">Markdown</button>' +
      '<button class="preview-tab-btn active" onclick="switchPreviewTab(\\'revised\\')">Rendered</button>';
    switchPreviewTab('revised');
  }} else {{
    // HTML file — single view, no tabs
    tabBar.style.display = 'none';
    body.innerHTML = '<pre class="raw-preview">' + escapeHtml(data.content) + '</pre>';
  }}
  body.scrollTop = 0;

  pane.classList.add('open');
  document.body.classList.add('preview-open');
}}

function closePreview() {{
  document.getElementById('previewPane').classList.remove('open');
  document.body.classList.remove('preview-open');
  if (activeFileEl) {{ activeFileEl.classList.remove('active'); activeFileEl = null; }}
}}

function switchPreviewTab(tab) {{
  const body = document.getElementById('previewBody');
  const tabBar = document.getElementById('previewTabs');
  const data = window._previewData;

  // Update active tab button
  tabBar.querySelectorAll('.preview-tab-btn').forEach(btn => {{
    btn.classList.toggle('active', btn.textContent.toLowerCase().startsWith(tab));
  }});

  if (!data) return;

  if (tab === 'original') {{
    const content = data.originalContent || data.content;
    try {{
      body.innerHTML = marked.parse(content);
    }} catch(e) {{
      body.innerHTML = '<pre class="raw-preview">' + escapeHtml(content) + '</pre>';
    }}
  }} else if (tab === 'markdown') {{
    body.innerHTML = '<pre class="md-source">' + escapeHtml(data.content) + '</pre>';
  }} else if (tab === 'revised') {{
    try {{
      body.innerHTML = marked.parse(data.content);
    }} catch(e) {{
      body.innerHTML = '<pre class="raw-preview">' + escapeHtml(data.content) + '</pre>';
    }}
  }}
  body.scrollTop = 0;
}}

function showRevisionModal() {{
  const data = window._previewData;
  if (!data) return;

  const key = window._previewKey;
  const cmd = 'python3 scripts/build-html-before-after.py --skip-fetch';

  const modal = document.createElement('div');
  modal.className = 'revision-modal';
  modal.onclick = function(e) {{ if (e.target === modal) modal.remove(); }};

  const content = document.createElement('div');
  content.className = 'revision-modal-content';
  content.innerHTML =
    '<h3>Create Revised HTML</h3>' +
    '<p>Run this command in your terminal to generate the revised HTML version with your markdown content applied to the original site page.</p>' +
    '<pre id="revisionCmd">' + escapeHtml(cmd) + '</pre>' +
    '<p style="font-size:11px;color:var(--text-muted)">Source: ' + escapeHtml(key) + '</p>' +
    '<div class="btn-row">' +
    '<button class="copy-btn" onclick="copyRevisionCmd(this)">Copy Command</button>' +
    '</div>';

  modal.appendChild(content);
  document.body.appendChild(modal);
}}

function copyRevisionCmd(btn) {{
  const cmd = document.getElementById('revisionCmd').textContent;
  navigator.clipboard.writeText(cmd).then(function() {{
    btn.textContent = 'Copied!';
    setTimeout(function() {{ btn.textContent = 'Copy Command'; }}, 2000);
  }});
}}

function navPreview(delta) {{
  const next = currentIndex + delta;
  if (next < 0 || next >= currentList.length) return;
  currentIndex = next;
  // Update active element in the list
  const key = currentList[currentIndex];
  const encoded = encodeKey(key);
  const el = document.querySelector(`[data-key="${{encoded}}"]`);
  setActiveEl(el);
  if (el) el.scrollIntoView({{ block: 'nearest' }});
  openPreview(key);
}}

function updateNav() {{
  document.getElementById('navPos').textContent = `${{currentIndex + 1}} of ${{currentList.length}}`;
  document.getElementById('prevBtn').disabled = currentIndex <= 0;
  document.getElementById('nextBtn').disabled = currentIndex >= currentList.length - 1;
}}

function escapeHtml(t) {{
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

// ── Global Search ──
document.getElementById('globalSearch').addEventListener('input', function() {{
  const q = this.value.toLowerCase().trim();
  // Search file tree entries
  document.querySelectorAll('.tf, .cat-file').forEach(f => {{
    const name = (f.querySelector('.fn, .cf-name') || {{}}).textContent || '';
    f.style.display = (!q || name.toLowerCase().includes(q)) ? '' : 'none';
  }});
  // Open all sections when searching
  if (q) {{
    document.querySelectorAll('.client-section').forEach(s => s.classList.add('open'));
    document.querySelectorAll('.tree-folder').forEach(f => f.classList.add('open'));
  }}
}});

// Keyboard: / to focus search, Esc to close preview, arrow keys for nav
document.addEventListener('keydown', function(e) {{
  if (e.key === '/' && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)) {{
    e.preventDefault();
    document.getElementById('globalSearch').focus();
  }}
  if (e.key === 'Escape') {{
    if (document.getElementById('previewPane').classList.contains('open')) {{
      closePreview();
    }} else {{
      document.getElementById('globalSearch').blur();
    }}
  }}
  if (document.getElementById('previewPane').classList.contains('open')) {{
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {{ e.preventDefault(); navPreview(-1); }}
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {{ e.preventDefault(); navPreview(1); }}
  }}
}});

// ── Init ──
buildUI();
</script>
</body>
</html>"""

    REPORTS_DIR.mkdir(exist_ok=True)
    out_path = REPORTS_DIR / "content-navigator.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    size = out_path.stat().st_size
    print(f"\nReport: {out_path.relative_to(ROOT)} ({human_size(size)})")
    return out_path


# ── Main ─────────────────────────────────────────────────────────────

def main():
    print("=== Content Navigator Builder ===\n")
    print("Generating registries...")
    registries = generate_all_registries()

    print("\nReading content store...")
    content_store = build_content_store(registries)
    print(f"  {len(content_store)} files loaded for preview")

    print("\nBuilding HTML report...")
    out = build_html(registries, content_store)
    print(f"\nDone! Open: {out}")


if __name__ == "__main__":
    main()
