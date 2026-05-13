#!/usr/bin/env python3
"""
Fetch original HTML for all Zia Tile product URLs that are missing
from html/original/. Skips pages already cached on disk.

Usage:
    python3 scripts/fetch-missing-originals.py [--dry-run] [--limit N]
"""

import argparse
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing dependency: pip install requests")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
CAMPAIGN_DIR = REPO_ROOT / "clients" / "zia-tile" / "campaigns" / "01-product-collection-pages"
CAMPAIGN_URLS_FILE = CAMPAIGN_DIR / "campaign-urls.md"
ORIGINAL_DIR = CAMPAIGN_DIR / "html" / "original"

FETCH_DELAY = 1.5
USER_AGENT = "ZiaContentOps/1.0 (internal content audit)"


def extract_ziatile_urls(campaign_file: Path) -> list[str]:
    text = campaign_file.read_text(encoding="utf-8")
    urls = re.findall(r'https://ziatile\.com/(?:en-ca/)?products/[^\s>|)]+', text)
    urls = [u.rstrip(">") for u in urls]
    return sorted(set(urls))


def url_to_filename(url: str) -> str:
    path = url.split("//", 1)[-1]
    path = path.split("?")[0]
    path = path.replace("ziatile.com/", "").replace("en-ca/", "")
    path = path.strip("/").replace("/", "--")
    if not path:
        path = "homepage"
    return path + ".html"


def find_missing(urls: list[str]) -> list[dict]:
    missing = []
    for url in urls:
        filename = url_to_filename(url)
        if not (ORIGINAL_DIR / filename).exists():
            missing.append({"url": url, "filename": filename})
    return missing


def fetch_page(url: str, session: requests.Session) -> str | None:
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"  ERROR: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Fetch missing original HTMLs for Zia Tile product pages")
    parser.add_argument("--dry-run", action="store_true", help="List missing pages without fetching")
    parser.add_argument("--limit", type=int, default=0, help="Fetch only first N missing pages (0 = all)")
    args = parser.parse_args()

    all_urls = extract_ziatile_urls(CAMPAIGN_URLS_FILE)
    print(f"Total unique product URLs in campaign sheet: {len(all_urls)}")

    missing = find_missing(all_urls)
    print(f"Already cached: {len(all_urls) - len(missing)}")
    print(f"Missing originals to fetch: {len(missing)}")

    if args.dry_run:
        print("\n--- DRY RUN: would fetch these ---")
        for m in missing:
            print(f"  {m['url']}  →  {m['filename']}")
        return

    to_fetch = missing[:args.limit] if args.limit else missing
    if not to_fetch:
        print("Nothing to fetch — all originals already cached.")
        return

    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    fetched = 0
    failed = 0
    for i, page in enumerate(to_fetch):
        print(f"[{i+1}/{len(to_fetch)}] Fetching {page['url']} ...")
        html = fetch_page(page["url"], session)
        if html:
            (ORIGINAL_DIR / page["filename"]).write_text(html, encoding="utf-8")
            print(f"  → saved {page['filename']} ({len(html):,} bytes)")
            fetched += 1
        else:
            failed += 1

        if i < len(to_fetch) - 1:
            time.sleep(FETCH_DELAY)

    print(f"\nDone. Fetched: {fetched}, Failed: {failed}, Total originals now: {len(all_urls) - len(missing) + fetched}")


if __name__ == "__main__":
    main()
