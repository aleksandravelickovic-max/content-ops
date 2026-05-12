#!/usr/bin/env python3
"""
Fetch original Zia Tile pages from the live site, apply content updates
from the campaign drafts, and save both original and revised HTML files.

Usage:
    python3 scripts/build-html-before-after.py [--fetch] [--limit N] [--skip-fetch]

    --fetch       Fetch original HTML from ziatile.com (rate-limited, ~90 pages)
    --skip-fetch  Skip fetching, only rebuild revised HTML from cached originals
    --limit N     Process only the first N pages (for testing)
"""

import argparse
import re
import sys
import time
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    import markdown
except ImportError as e:
    print(f"Missing dependency: {e}. Install with: pip install requests beautifulsoup4 markdown")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
CAMPAIGN_DIR = REPO_ROOT / "clients" / "zia-tile" / "campaigns" / "01-product-collection-pages"
PRODUCT_DRAFTS_DIR = CAMPAIGN_DIR / "gdocs-content" / "product-pages"
COLLECTION_DRAFTS_DIR = CAMPAIGN_DIR / "drafts"
HTML_DIR = CAMPAIGN_DIR / "html"
ORIGINAL_DIR = HTML_DIR / "original"
REVISED_DIR = HTML_DIR / "revised"
CAMPAIGN_URLS_FILE = CAMPAIGN_DIR / "campaign-urls.md"

FETCH_DELAY = 1.5  # seconds between requests
USER_AGENT = "ZiaContentOps/1.0 (internal content audit)"


# ---------------------------------------------------------------------------
# URL mapping
# ---------------------------------------------------------------------------

def parse_product_draft(path: Path) -> dict | None:
    """Extract URL, meta title, and meta description from a product draft .md file."""
    text = path.read_text(encoding="utf-8")
    url_match = re.search(r'\*\*URL:\*\*\s*<?([^>\s]+)>?', text)
    title_match = re.search(r'\*\*Meta title\*?\*?:?\s*(.+)', text)
    desc_match = re.search(r'\*\*Meta description\*?\*?:?\s*(.+)', text)

    if not url_match:
        return None

    url = url_match.group(1).strip()
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    return {
        "url": url,
        "meta_title": title_match.group(1).strip() if title_match else None,
        "meta_description": desc_match.group(1).strip() if desc_match else None,
        "draft_path": path,
        "slug": path.stem,
        "page_type": "product",
    }


def build_collection_url_map() -> dict:
    """Map collection draft filenames to live URLs from campaign-urls.md."""
    mapping = {
        "01-zellige": "https://ziatile.com/en-ca/collections/zellige",
        "02-zellige-mosaic": "https://ziatile.com/en-ca/collections/zellige-mosaics",
        "03-unglazed-natural-zellige": "https://ziatile.com/en-ca/collections/unglazed-natural-zellige",
        "04-unglazed-natural-zellige-mosaic": "https://ziatile.com/en-ca/collections/unglazed-natural-zellige-mosaics",
        "05-ceramics-matte": "https://ziatile.com/en-ca/collections/ceramics",
        "06-field-trip-japan": "https://ziatile.com/en-ca/collections/field-trip-japan",
        "07-cotto": "https://ziatile.com/en-ca/collections/cotto",
        "08-cotto-allende": "https://ziatile.com/en-ca/collections/cotto-tile-allende",
        "09-glass-mosaics": "https://ziatile.com/en-ca/collections/glass-mosaics",
        "10-terrazzo": "https://ziatile.com/en-ca/collections/terrazzo",
        "11-marble-solids": "https://ziatile.com/en-ca/collections/marble-tile",
        "12-marble-patterns": "https://ziatile.com/en-ca/collections/marble-tile",
        "13-cantera": "https://ziatile.com/en-ca/collections/cantera-tile",
        "14-limestone": "https://ziatile.com/en-ca/collections/limestone-tile",
        "15-cement": "https://ziatile.com/en-ca/collections/cement-tile",
        "16-roman-mosaics": "https://ziatile.com/en-ca/collections/roman-mosaics",
    }
    return mapping


def discover_pages() -> list[dict]:
    """Build the full list of pages to process."""
    pages = []

    # Product pages from gdocs-content
    if PRODUCT_DRAFTS_DIR.exists():
        for md_file in sorted(PRODUCT_DRAFTS_DIR.glob("*.md")):
            info = parse_product_draft(md_file)
            if info:
                pages.append(info)

    # Collection pages from drafts (use v3 if available, else base draft)
    collection_urls = build_collection_url_map()
    for slug, url in collection_urls.items():
        base_path = COLLECTION_DRAFTS_DIR / f"{slug}.md"

        v3_path_full = COLLECTION_DRAFTS_DIR / "v3" / f"{slug}.md"
        v3_suffix = slug.split("-", 1)[1] if "-" in slug else slug
        v3_candidates = list((COLLECTION_DRAFTS_DIR / "v3").glob(f"*{v3_suffix}*"))

        draft_path = None
        if v3_path_full.exists():
            draft_path = v3_path_full
        elif v3_candidates:
            draft_path = v3_candidates[0]
        elif base_path.exists():
            draft_path = base_path

        if draft_path:
            pages.append({
                "url": url,
                "meta_title": None,
                "meta_description": None,
                "draft_path": draft_path,
                "slug": slug,
                "page_type": "collection",
            })

    return pages


def url_to_filename(url: str) -> str:
    """Convert a URL to a safe filename."""
    path = url.split("//", 1)[-1]
    path = path.split("?")[0]
    path = path.replace("ziatile.com/", "").replace("en-ca/", "")
    path = path.strip("/").replace("/", "--")
    if not path:
        path = "homepage"
    return path + ".html"


# ---------------------------------------------------------------------------
# Fetch originals
# ---------------------------------------------------------------------------

def fetch_page(url: str, session: requests.Session) -> str | None:
    """Fetch a single page, return HTML or None on error."""
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def fetch_all_originals(pages: list[dict]) -> dict:
    """Fetch and cache all original HTML pages. Returns {slug: filename}."""
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    results = {}
    for i, page in enumerate(pages):
        filename = url_to_filename(page["url"])
        out_path = ORIGINAL_DIR / filename
        page["original_filename"] = filename

        if out_path.exists():
            print(f"  [{i+1}/{len(pages)}] CACHED {filename}")
            results[page["slug"]] = filename
            continue

        print(f"  [{i+1}/{len(pages)}] Fetching {page['url']} ...")
        html = fetch_page(page["url"], session)
        if html:
            out_path.write_text(html, encoding="utf-8")
            results[page["slug"]] = filename
            print(f"    → saved {filename} ({len(html):,} bytes)")
        else:
            print("    → FAILED")

        if i < len(pages) - 1:
            time.sleep(FETCH_DELAY)

    return results


# ---------------------------------------------------------------------------
# Content extraction from markdown drafts
# ---------------------------------------------------------------------------

def extract_sections_from_product_draft(path: Path) -> dict:
    """Parse a product draft .md into named sections."""
    text = path.read_text(encoding="utf-8")
    sections = {}

    # Extract frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            text = text[end + 3:].strip()

    # Meta info
    url_m = re.search(r'\*\*URL:\*\*\s*<?([^>\s]+)>?', text)
    title_m = re.search(r'\*\*Meta title\*?\*?:?\s*(.+)', text)
    desc_m = re.search(r'\*\*Meta description\*?\*?:?\s*(.+)', text)
    sections["url"] = url_m.group(1).strip() if url_m else ""
    sections["meta_title"] = title_m.group(1).strip() if title_m else ""
    sections["meta_description"] = desc_m.group(1).strip() if desc_m else ""

    # Split by H2 headers
    h2_pattern = re.compile(r'^##\s+(.+?)(?:\s*—\s*\[.*?\])?\s*$', re.MULTILINE)
    h2_matches = list(h2_pattern.finditer(text))

    for idx, match in enumerate(h2_matches):
        header = match.group(1).strip()
        start = match.end()
        end = h2_matches[idx + 1].start() if idx + 1 < len(h2_matches) else len(text)
        body = text[start:end].strip()

        key = header.lower()
        if "about" in key:
            sections["about"] = body
        elif "tile usage" in key:
            sections["tile_usage"] = body
        elif "how it" in key:
            sections["how_its_made"] = body
        elif "order" in key and "shipping" in key:
            sections["order_shipping"] = body
        elif "installation" in key:
            sections["installation_guide"] = body
        elif "faq" in key or "frequently" in key:
            sections["faq"] = body

    # Product intro (content before first H2, after meta)
    first_h2 = h2_matches[0].start() if h2_matches else len(text)
    intro_text = text[:first_h2]
    # Strip meta lines from intro
    intro_lines = []
    skip_meta = True
    for line in intro_text.split("\n"):
        if skip_meta and (line.startswith("**URL:") or line.startswith("**Meta") or not line.strip()):
            if line.startswith("**URL:") or line.startswith("**Meta"):
                continue
            if not line.strip() and not intro_lines:
                continue
        else:
            skip_meta = False
        if not skip_meta:
            intro_lines.append(line)
    sections["intro"] = "\n".join(intro_lines).strip()

    return sections


def extract_sections_from_collection_draft(path: Path) -> dict:
    """Parse a collection/material template .md into named sections."""
    text = path.read_text(encoding="utf-8")
    sections = {}

    h2_pattern = re.compile(r'^##\s+(.+?)(?:\s*\*?\[.*?\]\*?)?\s*$', re.MULTILINE)
    h2_matches = list(h2_pattern.finditer(text))

    for idx, match in enumerate(h2_matches):
        header = match.group(1).strip()
        start = match.end()
        end = h2_matches[idx + 1].start() if idx + 1 < len(h2_matches) else len(text)
        body = text[start:end].strip()

        key = header.lower()
        if "about" in key:
            sections["about"] = body
        elif "tile usage" in key:
            sections["tile_usage"] = body
        elif "how it" in key:
            sections["how_its_made"] = body
        elif "order" in key and "shipping" in key:
            sections["order_shipping"] = body
        elif "installation" in key:
            sections["installation_guide"] = body
        elif "faq" in key or "frequently" in key:
            sections["faq"] = body

    # Intro text before first H2
    first_h2 = h2_matches[0].start() if h2_matches else len(text)
    sections["intro"] = text[:first_h2].strip()

    return sections


def md_to_html(md_text: str) -> str:
    """Convert markdown text to HTML."""
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    return md.convert(md_text)


# ---------------------------------------------------------------------------
# Apply content to HTML
# ---------------------------------------------------------------------------

def apply_product_content(original_html: str, sections: dict, page_info: dict) -> str:
    """Apply content updates to a product page HTML."""
    soup = BeautifulSoup(original_html, "html.parser")

    # 1. Update <title>
    meta_title = page_info.get("meta_title") or sections.get("meta_title", "")
    if meta_title:
        title_tag = soup.find("title")
        if title_tag:
            title_tag.string = f"\n      {meta_title}\n &ndash; Zia Tile"

    # 2. Update meta description
    meta_desc = page_info.get("meta_description") or sections.get("meta_description", "")
    if meta_desc:
        for tag in soup.find_all("meta"):
            if tag.get("name") == "description":
                tag["content"] = meta_desc
            if tag.get("property") == "og:description":
                tag["content"] = meta_desc
            if tag.get("name") == "twitter:description":
                tag["content"] = meta_desc

    # 3. Update og:title
    if meta_title:
        for tag in soup.find_all("meta"):
            if tag.get("property") == "og:title":
                tag["content"] = meta_title
            if tag.get("name") == "twitter:title":
                tag["content"] = meta_title

    # 4. Replace "About" modal content
    if sections.get("about"):
        about_modal = soup.find("div", class_="product-content-modal--about")
        if about_modal:
            content_div = about_modal.find("div", class_="product-content-modal__content")
            if content_div:
                new_html = md_to_html(sections["about"])
                content_div.clear()
                content_div.append(BeautifulSoup(new_html, "html.parser"))

    # 5. Replace "How It's Made" modal content
    if sections.get("how_its_made"):
        info_modal = soup.find("div", class_="product-content-modal--info")
        if info_modal:
            content_div = info_modal.find("div", class_="product-content-modal__content")
            if content_div:
                new_html = md_to_html(sections["how_its_made"])
                content_div.clear()
                content_div.append(BeautifulSoup(new_html, "html.parser"))

    # 6. Replace "Order & Shipping" modal content
    if sections.get("order_shipping"):
        orders_modal = soup.find("div", class_="product-content-modal--orders")
        if orders_modal:
            content_div = orders_modal.find("div", class_="product-content-modal__content")
            if content_div:
                new_html = md_to_html(sections["order_shipping"])
                content_div.clear()
                content_div.append(BeautifulSoup(new_html, "html.parser"))

    # 7. Replace "Installation Guide" modal content
    if sections.get("installation_guide"):
        install_modal = soup.find("div", class_="product-content-modal--install")
        if install_modal:
            content_div = install_modal.find("div", class_="product-content-modal__content")
            if content_div:
                new_html = md_to_html(sections["installation_guide"])
                content_div.clear()
                content_div.append(BeautifulSoup(new_html, "html.parser"))

    # 8. Add a visible banner to mark this as revised
    main_tag = soup.find("main") or soup.find("div", {"role": "main"})
    if main_tag:
        banner = soup.new_tag("div", style=(
            "background: #2d5a27; color: #fff; padding: 10px 20px; "
            "font-family: sans-serif; font-size: 13px; text-align: center; "
            "position: sticky; top: 0; z-index: 9999;"
        ))
        banner.string = f"REVISED CONTENT — {page_info['slug']} — Content updates applied from campaign drafts"
        main_tag.insert(0, banner)

    return str(soup)


def apply_collection_content(original_html: str, sections: dict, page_info: dict) -> str:
    """Apply content updates to a collection page HTML."""
    soup = BeautifulSoup(original_html, "html.parser")

    # 1. Replace hero description text
    hero_secondary = soup.find("div", class_="text-block__inner--secondary")
    if hero_secondary and sections.get("intro"):
        intro_lines = sections["intro"].split("\n")
        # Filter out template placeholders
        clean_lines = [line for line in intro_lines if not line.startswith("#") and not line.startswith("[CART") and not line.startswith("[IMAGE")]
        clean_text = "\n".join(clean_lines).strip()
        if clean_text:
            new_html = md_to_html(clean_text)
            hero_secondary.clear()
            hero_secondary.append(BeautifulSoup(new_html, "html.parser"))

    # 2. Replace accordion FAQ content
    accordion_section = soup.find("div", class_="accordion-container__content")
    if accordion_section and sections.get("faq"):
        faq_html = md_to_html(sections["faq"])
        faq_soup = BeautifulSoup(faq_html, "html.parser")

        # Extract Q&A pairs from rendered HTML
        qa_pairs = []
        current_q = None
        current_a = []
        for el in faq_soup.children:
            if el.name and el.name.startswith("h"):
                if current_q:
                    qa_pairs.append((current_q, "".join(str(a) for a in current_a)))
                current_q = el.get_text(strip=True)
                current_a = []
            elif current_q:
                current_a.append(str(el))
        if current_q:
            qa_pairs.append((current_q, "".join(str(a) for a in current_a)))

        if qa_pairs:
            existing_accordions = accordion_section.find_all("div", class_="ac")
            for i, (question, answer) in enumerate(qa_pairs):
                if i < len(existing_accordions):
                    ac = existing_accordions[i]
                    trigger = ac.find("button", class_="ac-trigger")
                    if trigger:
                        trigger.string = question
                    text_div = ac.find("div", class_="ac-text")
                    if text_div:
                        text_div.clear()
                        text_div.append(BeautifulSoup(answer, "html.parser"))

    # 3. Add revision banner
    main_tag = soup.find("main") or soup.find("div", {"role": "main"})
    if main_tag:
        banner = soup.new_tag("div", style=(
            "background: #2d5a27; color: #fff; padding: 10px 20px; "
            "font-family: sans-serif; font-size: 13px; text-align: center; "
            "position: sticky; top: 0; z-index: 9999;"
        ))
        banner.string = f"REVISED CONTENT — {page_info['slug']} — Content updates applied from campaign drafts"
        main_tag.insert(0, banner)

    return str(soup)


# ---------------------------------------------------------------------------
# Determine which collection template applies to a product
# ---------------------------------------------------------------------------

def find_collection_for_product(product_slug: str, product_url: str) -> str | None:
    """Given a product slug/URL, find the matching collection draft."""
    # Map product URLs to their collection based on known patterns
    url_lower = product_url.lower()

    collection_keywords = {
        "01-zellige": ["zellige", "bejmat"],
        "02-zellige-mosaic": ["zellige-mosaic", "lattice", "mosaic"],
        "03-unglazed-natural-zellige": ["unglazed-natural"],
        "05-ceramics-matte": ["ceramic", "ceramics"],
        "06-field-trip-japan": ["nagano", "field-trip"],
        "07-cotto": ["cotto", "red-clay", "adobe", "fired-earth", "oscura", "blanco", "madera",
                      "stars-cross", "alcazar", "oaxaca", "durango", "tornillo", "toltec", "zocalo"],
        "08-cotto-allende": ["allende", "condesa", "puebla", "piedra"],
        "09-glass-mosaics": ["glass", "gambit", "vaso", "dorsay", "union", "ells", "cheque", "tesserae", "murano"],
        "10-terrazzo": ["terrazzo", "bungalow"],
        "11-marble-solids": ["marble", "basilica", "monument", "carrara"],
        "13-cantera": ["cantera", "french-cobblestone", "volcan"],
        "14-limestone": ["limestone", "buff"],
        "15-cement": ["cement", "neutra"],
        "16-roman-mosaics": ["roman"],
    }

    slug_lower = product_slug.lower()
    for collection_slug, keywords in collection_keywords.items():
        for kw in keywords:
            if kw in slug_lower or kw in url_lower:
                return collection_slug

    return None


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build_revised_pages(pages: list[dict]):
    """Build revised HTML for all pages that have cached originals."""
    REVISED_DIR.mkdir(parents=True, exist_ok=True)

    # Pre-load collection templates
    collection_sections = {}
    for slug in build_collection_url_map():
        v3_path = COLLECTION_DRAFTS_DIR / "v3" / f"{slug}.md"
        base_path = COLLECTION_DRAFTS_DIR / f"{slug}.md"
        draft_path = v3_path if v3_path.exists() else base_path
        if draft_path.exists():
            collection_sections[slug] = extract_sections_from_collection_draft(draft_path)

    stats = {"revised": 0, "skipped": 0, "errors": 0}

    for page in pages:
        filename = url_to_filename(page["url"])
        original_path = ORIGINAL_DIR / filename
        revised_path = REVISED_DIR / filename

        if not original_path.exists():
            stats["skipped"] += 1
            continue

        try:
            original_html = original_path.read_text(encoding="utf-8")

            if page["page_type"] == "product":
                # Get product-specific content
                product_sections = extract_sections_from_product_draft(page["draft_path"])

                # Find and merge collection template content for shared sections
                collection_slug = find_collection_for_product(page["slug"], page["url"])
                if collection_slug and collection_slug in collection_sections:
                    template = collection_sections[collection_slug]
                    for key in ["about", "tile_usage", "how_its_made", "order_shipping", "installation_guide"]:
                        if key not in product_sections and key in template:
                            product_sections[key] = template[key]

                revised_html = apply_product_content(original_html, product_sections, page)
            else:
                sections = extract_sections_from_collection_draft(page["draft_path"])
                revised_html = apply_collection_content(original_html, sections, page)

            revised_path.write_text(revised_html, encoding="utf-8")
            stats["revised"] += 1
            print(f"  REVISED {filename}")

        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR processing {filename}: {e}")

    return stats


def build_index_page(pages: list[dict]):
    """Generate an index.html for browsing original vs revised side by side."""
    index_path = HTML_DIR / "index.html"

    product_pages = [p for p in pages if p["page_type"] == "product"]
    collection_pages = [p for p in pages if p["page_type"] == "collection"]

    rows = []
    for page in sorted(product_pages, key=lambda p: p["slug"]):
        filename = url_to_filename(page["url"])
        original_exists = (ORIGINAL_DIR / filename).exists()
        revised_exists = (REVISED_DIR / filename).exists()
        orig_link = f'<a href="original/{filename}" target="_blank">Original</a>' if original_exists else '<span style="color:#999">—</span>'
        rev_link = f'<a href="revised/{filename}" target="_blank">Revised</a>' if revised_exists else '<span style="color:#999">—</span>'
        status = "ready" if original_exists and revised_exists else "pending" if not original_exists else "error"
        status_dot = {"ready": "🟢", "pending": "⚪", "error": "🔴"}.get(status, "⚪")
        rows.append(f"""<tr>
  <td>{status_dot}</td>
  <td><strong>{page['slug']}</strong></td>
  <td style="font-size:12px"><a href="{page['url']}" target="_blank">{page['url'].split('/')[-1]}</a></td>
  <td>{orig_link}</td>
  <td>{rev_link}</td>
</tr>""")

    collection_rows = []
    for page in sorted(collection_pages, key=lambda p: p["slug"]):
        filename = url_to_filename(page["url"])
        original_exists = (ORIGINAL_DIR / filename).exists()
        revised_exists = (REVISED_DIR / filename).exists()
        orig_link = f'<a href="original/{filename}" target="_blank">Original</a>' if original_exists else '<span style="color:#999">—</span>'
        rev_link = f'<a href="revised/{filename}" target="_blank">Revised</a>' if revised_exists else '<span style="color:#999">—</span>'
        status = "ready" if original_exists and revised_exists else "pending"
        status_dot = {"ready": "🟢", "pending": "⚪"}.get(status, "⚪")
        collection_rows.append(f"""<tr>
  <td>{status_dot}</td>
  <td><strong>{page['slug']}</strong></td>
  <td style="font-size:12px"><a href="{page['url']}" target="_blank">{page['url'].split('/')[-1]}</a></td>
  <td>{orig_link}</td>
  <td>{rev_link}</td>
</tr>""")

    product_count = sum(1 for p in product_pages if (REVISED_DIR / url_to_filename(p["url"])).exists())
    collection_count = sum(1 for p in collection_pages if (REVISED_DIR / url_to_filename(p["url"])).exists())

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Zia Tile — Content Before & After</title>
<style>
  :root {{ --bg: #f6f1e8; --paper: #fbf7ee; --ink: #1c1a17; --accent: #8a3324; --rule: #d9cfb9; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--ink); line-height: 1.6; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 40px 24px; }}
  h1 {{ font-family: Georgia, serif; font-size: 36px; margin-bottom: 8px; }}
  .subtitle {{ color: #666; margin-bottom: 32px; font-size: 15px; }}
  .stats {{ display: flex; gap: 24px; margin-bottom: 32px; }}
  .stat {{ background: var(--paper); border: 1px solid var(--rule); padding: 16px 24px; border-radius: 6px; }}
  .stat-num {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
  .stat-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #888; }}
  h2 {{ font-family: Georgia, serif; font-size: 24px; margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--rule); }}
  table {{ width: 100%; border-collapse: collapse; background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; overflow: hidden; }}
  th {{ text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent); padding: 12px 14px; border-bottom: 2px solid var(--rule); }}
  td {{ padding: 10px 14px; border-bottom: 1px solid var(--rule); font-size: 14px; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover {{ background: #f0ebe0; }}
  a {{ color: var(--accent); }}
  .instructions {{ background: var(--paper); border: 1px solid var(--rule); padding: 20px; margin-bottom: 32px; border-radius: 6px; font-size: 14px; }}
  .instructions code {{ background: #efe6d2; padding: 2px 6px; border-radius: 3px; font-size: 13px; }}
</style>
</head>
<body>
<div class="container">
  <h1>Zia Tile — Content Before & After</h1>
  <p class="subtitle">Campaign: 01 Product & Collection Pages · Generated {time.strftime('%Y-%m-%d %H:%M')}</p>

  <div class="stats">
    <div class="stat"><div class="stat-num">{product_count}</div><div class="stat-label">Product Pages</div></div>
    <div class="stat"><div class="stat-num">{collection_count}</div><div class="stat-label">Collection Pages</div></div>
    <div class="stat"><div class="stat-num">{product_count + collection_count}</div><div class="stat-label">Total Revised</div></div>
  </div>

  <div class="instructions">
    <strong>How to use:</strong> Click <em>Original</em> to see the page as it appears on ziatile.com today.
    Click <em>Revised</em> to see the same page with campaign content updates applied.
    Revised pages show a green banner at the top to confirm content has been swapped.
  </div>

  <h2>Product Pages ({len(product_pages)})</h2>
  <table>
    <thead><tr><th></th><th>Product</th><th>URL</th><th>Original</th><th>Revised</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>

  <h2>Collection Pages ({len(collection_pages)})</h2>
  <table>
    <thead><tr><th></th><th>Collection</th><th>URL</th><th>Original</th><th>Revised</th></tr></thead>
    <tbody>{"".join(collection_rows)}</tbody>
  </table>
</div>
</body>
</html>"""

    index_path.write_text(html, encoding="utf-8")
    print(f"\n  Index page: {index_path}")


def main():
    parser = argparse.ArgumentParser(description="Build HTML before/after for Zia Tile content updates")
    parser.add_argument("--fetch", action="store_true", help="Fetch original HTML from ziatile.com")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip fetching, rebuild from cache")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of pages to process")
    args = parser.parse_args()

    print("Discovering pages...")
    pages = discover_pages()
    if args.limit:
        pages = pages[:args.limit]

    product_count = sum(1 for p in pages if p["page_type"] == "product")
    collection_count = sum(1 for p in pages if p["page_type"] == "collection")
    print(f"  Found {len(pages)} pages ({product_count} products, {collection_count} collections)")

    if args.fetch and not args.skip_fetch:
        print(f"\nFetching originals (delay={FETCH_DELAY}s between requests)...")
        fetch_all_originals(pages)
    elif not args.skip_fetch:
        print("\nTip: Run with --fetch to download original HTML from ziatile.com")
        print("     Run with --skip-fetch to rebuild revised HTML from cached originals")

    cached = sum(1 for p in pages if (ORIGINAL_DIR / url_to_filename(p["url"])).exists())
    print(f"\nCached originals: {cached}/{len(pages)}")

    if cached > 0:
        print("\nBuilding revised pages...")
        stats = build_revised_pages(pages)
        print(f"\n  Revised: {stats['revised']}  Skipped: {stats['skipped']}  Errors: {stats['errors']}")

    print("\nBuilding index page...")
    build_index_page(pages)

    print("\nDone!")
    print(f"  Original HTML: {ORIGINAL_DIR}/")
    print(f"  Revised HTML:  {REVISED_DIR}/")
    print(f"  Index:         {HTML_DIR}/index.html")


if __name__ == "__main__":
    main()
