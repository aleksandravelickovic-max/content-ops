#!/usr/bin/env python3
"""
Collect website intelligence for LinkGraph clients.

This script uses the repo's client folders as the source of truth, then fetches
public website sitemaps and representative pages. It writes one editable JSON
and one readable Markdown file per client:

    clients/{client}/raw/research/website-intelligence.json
    clients/{client}/raw/research/website-intelligence.md

It also writes aggregate reports:

    reports/client-website-intelligence.json
    reports/client-website-intelligence.html

Usage:
    python3 scripts/crawl-client-websites.py
    python3 scripts/crawl-client-websites.py --client zia-tile --max-pages 20
"""

from __future__ import annotations

import argparse
import html
import json
import re
import socket
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
REPORTS_DIR = ROOT / "reports"
REGISTRY_PATH = ROOT / "dashboard" / "delivery-registry.json"
AGG_JSON = REPORTS_DIR / "client-website-intelligence.json"
AGG_HTML = REPORTS_DIR / "client-website-intelligence.html"
EXCLUDED_CLIENT_SLUGS = {"searchatlas"}

USER_AGENT = "LinkGraphContentOpsWebsiteIntelligence/1.0 (+https://linkgraph.io)"
REQUEST_TIMEOUT = 8
MAX_SITEMAPS = 8
MAX_URLS_PER_CLIENT = 1200
DEFAULT_MAX_PAGES = 14
DEFAULT_MAX_OFFERING_PAGES = 40

STOPWORDS = {
    "about", "after", "again", "against", "also", "and", "are", "available",
    "based", "because", "been", "before", "being", "best", "between", "blog",
    "business", "can", "care", "center", "client", "company", "contact",
    "content", "does", "each", "from", "get", "guide", "have", "help",
    "home", "into", "learn", "more", "near", "needs", "new", "our", "page",
    "people", "product", "products", "read", "service", "services", "site",
    "solution", "solutions", "that", "the", "their", "them", "this", "through",
    "use", "using", "what", "when", "where", "with", "your",
}

FALLBACK_WEBSITES = {
    "searchatlas": ["https://www.searchatlas.com/"],
    "zia-tile": ["https://www.ziatile.com/"],
}

PRODUCT_PATH_HINTS = {
    "product", "products", "collections", "collection", "shop", "store",
    "category", "categories", "treatments", "treatment", "services",
    "service", "solutions", "solution", "features", "feature", "tours",
    "tour", "charters", "charter", "storage", "locations", "location",
}


@dataclass
class ClientTarget:
    slug: str
    display_name: str
    path: Path
    style_system: Path
    website_urls: list[str] = field(default_factory=list)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.headings: list[str] = []
        self.links: list[str] = []
        self._tag_stack: list[str] = []
        self._title_parts: list[str] = []
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        self._tag_stack.append(tag)
        if tag == "meta" and attr.get("name", "").lower() == "description":
            self.meta_description = clean_text(attr.get("content", ""))
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag in {"h1", "h2", "h3"}:
            self._heading_tag = tag
            self._heading_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title = clean_text(" ".join(self._title_parts))
        if tag == self._heading_tag:
            heading = clean_text(" ".join(self._heading_parts))
            if heading:
                self.headings.append(heading)
            self._heading_tag = None
            self._heading_parts = []
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._tag_stack and self._tag_stack[-1] == "title":
            self._title_parts.append(data)
        if self._heading_tag:
            self._heading_parts.append(data)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def normalize_url(value: str) -> str:
    value = value.strip().strip(".,;)")
    if not value:
        return ""
    if value.startswith("//"):
        value = "https:" + value
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    parsed = urllib.parse.urlparse(value)
    if not parsed.netloc or "." not in parsed.netloc:
        return ""
    path = parsed.path or "/"
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))


def same_domain(url: str, base_url: str) -> bool:
    return urllib.parse.urlparse(url).netloc.lower().replace("www.", "") == urllib.parse.urlparse(base_url).netloc.lower().replace("www.", "")


def fetch(url: str) -> tuple[int, str, bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xml,text/xml,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=ssl.create_default_context()) as response:
            status = getattr(response, "status", 200)
            content_type = response.headers.get("Content-Type", "")
            body = response.read(3_000_000)
            final_url = response.geturl()
            return status, content_type, body, final_url
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), exc.read(200_000), url
    except (urllib.error.URLError, socket.timeout, TimeoutError, ssl.SSLError) as exc:
        raise RuntimeError(str(exc)) from exc


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"clients": {}}
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"clients": {}}


def discover_clients(client_filter: str | None = None) -> list[ClientTarget]:
    registry = load_registry()
    clients: list[ClientTarget] = []
    for style_system in sorted(CLIENTS_DIR.rglob("STYLE-SYSTEM.md")):
        slug = style_system.parent.relative_to(CLIENTS_DIR).as_posix()
        if slug in EXCLUDED_CLIENT_SLUGS:
            continue
        if client_filter and slug != client_filter:
            continue
        entry = registry.get("clients", {}).get(slug, {})
        display_name = entry.get("display_name") or slug.replace("/", " / ").replace("-", " ").title()
        website_urls = []
        for raw_url in entry.get("website_urls", []) if isinstance(entry.get("website_urls"), list) else []:
            normalized = normalize_url(raw_url)
            if normalized:
                website_urls.append(normalized)
        website_urls.extend(extract_website_urls(style_system))
        website_urls.extend(extract_website_urls_from_raw(style_system.parent))
        website_urls.extend(FALLBACK_WEBSITES.get(slug, []))
        clients.append(ClientTarget(slug, display_name, style_system.parent, style_system, unique_urls(website_urls)))
    return clients


def extract_website_urls(style_system: Path) -> list[str]:
    text = style_system.read_text(encoding="utf-8", errors="replace")
    urls: list[str] = []
    for line in text.splitlines():
        lowered = line.lower()
        if "website" not in lowered and "| website |" not in lowered:
            continue
        urls.extend(extract_urls_from_line(line))
    return urls


def extract_website_urls_from_raw(client_dir: Path) -> list[str]:
    urls: list[str] = []
    for path in sorted((client_dir / "raw").rglob("*.md")) if (client_dir / "raw").exists() else []:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:40]
        except Exception:
            continue
        for line in lines:
            if "website" in line.lower():
                urls.extend(extract_urls_from_line(line))
    return urls


def extract_urls_from_line(line: str) -> list[str]:
    found = re.findall(r"https?://[^\s)\]>,|]+", line)
    domains = re.findall(r"(?<!@)\b(?:www\.)?[a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)+\b", line, flags=re.I)
    urls = [normalize_url(url) for url in found]
    for domain in domains:
        if any(domain in url for url in urls):
            continue
        if domain.lower().endswith((".com", ".io", ".ca", ".org", ".net")):
            urls.append(normalize_url(domain))
    blocked_hosts = {"app.clickup.com", "docs.google.com", "t9011399348.p.clickup-attachments.com"}
    return [url for url in urls if url and urllib.parse.urlparse(url).netloc not in blocked_hosts]


def unique_urls(urls: list[str]) -> list[str]:
    seen = set()
    out = []
    for url in urls:
        normalized = normalize_url(url)
        if normalized and normalized not in seen:
            seen.add(normalized)
            out.append(normalized)
    return out


def discover_sitemaps(base_url: str) -> tuple[list[str], list[str]]:
    parsed = urllib.parse.urlparse(base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    candidates = []
    errors = []
    try:
        status, _, body, _ = fetch(f"{origin}/robots.txt")
        if status < 400:
            text = body.decode("utf-8", errors="replace")
            for line in text.splitlines():
                if line.lower().startswith("sitemap:"):
                    candidates.append(normalize_url(line.split(":", 1)[1].strip()))
    except RuntimeError as exc:
        errors.append(f"robots.txt: {exc}")
    candidates.extend(
        normalize_url(url)
        for url in [
            f"{origin}/sitemap.xml",
            f"{origin}/sitemap_index.xml",
            f"{origin}/wp-sitemap.xml",
            f"{origin}/sitemap-pages.xml",
            f"{origin}/sitemap_products_1.xml",
            f"{origin}/sitemap_collections_1.xml",
        ]
    )
    return unique_urls([url for url in candidates if url]), errors


def parse_sitemap(url: str, seen: set[str] | None = None, depth: int = 0) -> tuple[list[str], list[str], list[str]]:
    seen = seen or set()
    if url in seen or depth > 2 or len(seen) >= MAX_SITEMAPS:
        return [], [], []
    seen.add(url)
    try:
        status, content_type, body, final_url = fetch(url)
    except RuntimeError as exc:
        return [], [], [f"{url}: {exc}"]
    if status >= 400:
        return [], [], [f"{url}: HTTP {status}"]
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return [], [], [f"{url}: not XML ({content_type})"]

    urls = []
    sitemaps = [final_url]
    errors = []
    tag = strip_ns(root.tag)
    if tag == "sitemapindex":
        for loc in root.findall(".//{*}loc"):
            if len(seen) >= MAX_SITEMAPS:
                break
            child = clean_text(loc.text or "")
            if child:
                child_urls, child_sitemaps, child_errors = parse_sitemap(child, seen, depth + 1)
                urls.extend(child_urls)
                sitemaps.extend(child_sitemaps)
                errors.extend(child_errors)
                if len(urls) >= MAX_URLS_PER_CLIENT:
                    break
    elif tag == "urlset":
        for loc in root.findall(".//{*}loc"):
            page_url = clean_text(loc.text or "")
            if page_url:
                urls.append(page_url)
            if len(urls) >= MAX_URLS_PER_CLIENT:
                break
    return unique_urls(urls), unique_urls(sitemaps), errors


def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1].lower()


def classify_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path.lower()
    segments = [segment for segment in path.split("/") if segment]
    if not segments:
        return "home"
    if any(segment in {"blog", "resources", "articles", "news"} for segment in segments):
        return "content"
    if any(segment in {"product", "products", "collections", "collection", "shop"} for segment in segments):
        return "product"
    if any(segment in {"service", "services", "treatment", "treatments", "solutions", "solution", "features"} for segment in segments):
        return "service"
    if any(segment in {"location", "locations", "near-me"} for segment in segments):
        return "location"
    return "page"


def choose_sample_urls(urls: list[str], base_url: str, max_pages: int) -> list[str]:
    same_site = [url for url in urls if same_domain(url, base_url)]
    if not same_site:
        same_site = [base_url]
    scored = []
    for url in same_site:
        path = urllib.parse.urlparse(url).path.lower()
        score = 0
        for hint in PRODUCT_PATH_HINTS:
            if f"/{hint}" in path:
                score += 3
        if classify_url(url) in {"product", "service"}:
            score += 4
        if path in {"", "/"}:
            score += 2
        if "blog" in path:
            score -= 1
        scored.append((score, len(path), url))
    scored.sort(key=lambda row: (-row[0], row[1], row[2]))
    sample = [url for _, _, url in scored[:max_pages]]
    if base_url not in sample:
        sample.insert(0, base_url)
    return unique_urls(sample)[:max_pages]


def parse_page(url: str) -> dict[str, Any]:
    started = time.time()
    try:
        status, content_type, body, final_url = fetch(url)
    except RuntimeError as exc:
        return {"url": url, "status": "error", "error": str(exc), "elapsed_ms": round((time.time() - started) * 1000)}
    text = body.decode("utf-8", errors="replace")
    parser = PageParser()
    if "html" in content_type or text.lstrip().startswith(("<!doctype", "<html", "<")):
        try:
            parser.feed(text)
        except Exception:
            pass
    return {
        "url": final_url,
        "requested_url": url,
        "status_code": status,
        "content_type": content_type,
        "page_type": classify_url(final_url),
        "title": parser.title,
        "meta_description": parser.meta_description,
        "headings": parser.headings[:12],
        "links_seen": len(parser.links),
        "elapsed_ms": round((time.time() - started) * 1000),
    }


def summarize_terms(pages: list[dict[str, Any]]) -> list[str]:
    counter: Counter[str] = Counter()
    for page in pages:
        text = " ".join([page.get("title", ""), page.get("meta_description", ""), " ".join(page.get("headings", []))])
        for token in re.findall(r"[A-Za-z][A-Za-z0-9&-]{2,}", text):
            token = token.strip("-").lower()
            if token and token not in STOPWORDS and len(token) > 2:
                counter[token] += 1
    return [term for term, _ in counter.most_common(30)]


def summarize_client(client: ClientTarget, max_pages: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "client": client.slug,
        "display_name": client.display_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "website_urls": client.website_urls,
        "status": "pending",
        "sitemaps": [],
        "sitemap_errors": [],
        "url_count": 0,
        "page_type_counts": {},
        "sample_pages": [],
        "offering_pages": [],
        "top_terms": [],
        "product_or_service_urls": [],
        "blockers": [],
    }
    if not client.website_urls:
        result["status"] = "blocked"
        result["blockers"].append("No website URL found in STYLE-SYSTEM.md, raw overview files, registry, or fallback map.")
        return result

    all_urls: list[str] = []
    all_sitemaps: list[str] = []
    for base_url in client.website_urls:
        sitemap_candidates, robots_errors = discover_sitemaps(base_url)
        result["sitemap_errors"].extend(robots_errors)
        base_urls: list[str] = []
        for sitemap_url in sitemap_candidates:
            urls, sitemaps, errors = parse_sitemap(sitemap_url)
            base_urls.extend(urls)
            all_sitemaps.extend(sitemaps)
            result["sitemap_errors"].extend(errors)
            if base_urls:
                break
        if not base_urls:
            base_urls = [base_url]
            result["blockers"].append(f"No usable sitemap found for {base_url}; sampled homepage only.")
        all_urls.extend(base_urls)

    all_urls = unique_urls(all_urls)[:MAX_URLS_PER_CLIENT]
    result["sitemaps"] = unique_urls(all_sitemaps)
    result["url_count"] = len(all_urls)
    page_type_counts = Counter(classify_url(url) for url in all_urls)
    result["page_type_counts"] = dict(sorted(page_type_counts.items()))
    result["product_or_service_urls"] = [
        url for url in all_urls if classify_url(url) in {"product", "service"}
    ][:80]

    sample_urls: list[str] = []
    for base_url in client.website_urls:
        sample_urls.extend(choose_sample_urls(all_urls, base_url, max_pages))
    sample_urls = unique_urls(sample_urls)[:max_pages]
    result["sample_pages"] = [parse_page(url) for url in sample_urls]
    offering_urls = result["product_or_service_urls"][:DEFAULT_MAX_OFFERING_PAGES]
    result["offering_pages"] = [parse_page(url) for url in offering_urls if url not in sample_urls]
    result["top_terms"] = summarize_terms(result["sample_pages"] + result["offering_pages"])
    result["status"] = "ok" if result["url_count"] > 1 else "partial"
    return result


def write_client_outputs(client: ClientTarget, result: dict[str, Any]) -> None:
    research_dir = client.path / "raw" / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    (research_dir / "website-intelligence.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (research_dir / "website-intelligence.md").write_text(render_client_markdown(result), encoding="utf-8")


def render_client_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['display_name']} Website Intelligence",
        "",
        f"Generated: {result['generated_at']}",
        f"Status: {result['status']}",
        "",
        "## Website URLs",
        "",
    ]
    if result["website_urls"]:
        lines.extend(f"- {url}" for url in result["website_urls"])
    else:
        lines.append("- Missing")
    lines.extend(["", "## Sitemaps", ""])
    if result["sitemaps"]:
        lines.extend(f"- {url}" for url in result["sitemaps"][:20])
    else:
        lines.append("- No usable sitemap found")
    lines.extend(
        [
            "",
            "## URL Inventory",
            "",
            f"- Total URLs discovered: {result['url_count']}",
        ]
    )
    for page_type, count in result.get("page_type_counts", {}).items():
        lines.append(f"- {page_type}: {count}")
    lines.extend(["", "## Product / Service URL Samples", ""])
    samples = result.get("product_or_service_urls", [])[:30]
    if samples:
        lines.extend(f"- {url}" for url in samples)
    else:
        lines.append("- None detected from sitemap paths")
    lines.extend(["", "## Page Context Samples", ""])
    for page in result.get("sample_pages", []):
        lines.append(f"### {page.get('title') or page.get('url')}")
        lines.append("")
        lines.append(f"- URL: {page.get('url')}")
        lines.append(f"- Type: {page.get('page_type', 'unknown')}")
        if page.get("meta_description"):
            lines.append(f"- Meta: {page['meta_description']}")
        if page.get("headings"):
            lines.append("- Headings:")
            lines.extend(f"  - {heading}" for heading in page["headings"][:8])
        if page.get("error"):
            lines.append(f"- Error: {page['error']}")
        lines.append("")
    lines.extend(["## Top Context Terms", ""])
    if result.get("top_terms"):
        lines.append(", ".join(result["top_terms"][:30]))
    else:
        lines.append("No terms extracted.")
    lines.extend(["", "## Blockers", ""])
    if result.get("blockers"):
        lines.extend(f"- {blocker}" for blocker in result["blockers"])
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def render_aggregate_html(results: list[dict[str, Any]]) -> str:
    rows = "\n".join(render_aggregate_row(result) for result in sorted(results, key=lambda item: item["display_name"].lower()))
    generated = datetime.now(timezone.utc).isoformat()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Client Website Intelligence</title>
  <style>
    body {{ margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f7f7f3; color: #202124; }}
    header {{ padding: 28px 32px 18px; background: #fff; border-bottom: 1px solid #d9d8cf; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    main {{ padding: 24px 32px 36px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d9d8cf; }}
    th, td {{ padding: 11px 12px; border-bottom: 1px solid #d9d8cf; text-align: left; vertical-align: top; font-size: 14px; }}
    th {{ background: #eeede5; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }}
    .chip {{ display: inline-block; padding: 3px 8px; border-radius: 999px; background: #ecebe3; font-size: 12px; font-weight: 700; }}
    .ok {{ color: #2f7d4f; background: #e7f3ea; }}
    .partial {{ color: #9a6a00; background: #fff3cf; }}
    .blocked {{ color: #a43b35; background: #f8dfdc; }}
    .muted {{ color: #666a73; font-size: 12px; }}
    a {{ color: #2457a6; text-decoration: none; }}
  </style>
</head>
<body>
  <header>
    <h1>Client Website Intelligence</h1>
    <div class="muted">Generated {html.escape(generated)}. Edit per-client research in <code>clients/{{client}}/raw/research/website-intelligence.md</code>.</div>
  </header>
  <main>
    <table>
      <thead><tr><th>Client</th><th>Status</th><th>Website</th><th>Sitemaps</th><th>URLs</th><th>Products / Services</th><th>Context</th><th>Blockers</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </main>
</body>
</html>
"""


def render_aggregate_row(result: dict[str, Any]) -> str:
    status = result.get("status", "unknown")
    site_links = "<br>".join(f"<a href=\"{html.escape(url)}\">{html.escape(url)}</a>" for url in result.get("website_urls", [])[:3]) or "Missing"
    sitemap_count = len(result.get("sitemaps", []))
    product_count = len(result.get("product_or_service_urls", []))
    terms = ", ".join(result.get("top_terms", [])[:10])
    blockers = "<br>".join(html.escape(item) for item in result.get("blockers", [])[:3]) or "None"
    return f"""
      <tr>
        <td><strong>{html.escape(result['display_name'])}</strong><br><span class="muted">{html.escape(result['client'])}</span></td>
        <td><span class="chip {html.escape(status)}">{html.escape(status)}</span></td>
        <td>{site_links}</td>
        <td>{sitemap_count}</td>
        <td>{result.get('url_count', 0)}</td>
        <td>{product_count}</td>
        <td>{html.escape(terms)}</td>
        <td>{blockers}</td>
      </tr>"""


def write_aggregate(results: list[dict[str, Any]]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    aggregate = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "client_count": len(results),
        "ok_count": sum(1 for result in results if result.get("status") == "ok"),
        "partial_count": sum(1 for result in results if result.get("status") == "partial"),
        "blocked_count": sum(1 for result in results if result.get("status") == "blocked"),
        "results": results,
    }
    AGG_JSON.write_text(json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    AGG_HTML.write_text(render_aggregate_html(results), encoding="utf-8")


def load_all_client_results() -> list[dict[str, Any]]:
    results = []
    for path in sorted(CLIENTS_DIR.rglob("raw/research/website-intelligence.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("client"):
            results.append(data)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Crawl client websites and write sitemap/product/context intelligence.")
    parser.add_argument("--client", help="Only crawl one client slug, such as zia-tile or the-hope-house/thehopehouse.")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES, help="Representative pages to fetch per client.")
    args = parser.parse_args()

    clients = discover_clients(args.client)
    if not clients:
        raise SystemExit("No clients found.")

    results = []
    for index, client in enumerate(clients, 1):
        print(f"[{index}/{len(clients)}] {client.slug}", flush=True)
        result = summarize_client(client, max_pages=args.max_pages)
        write_client_outputs(client, result)
        results.append(result)
        print(f"  {result['status']}: {result['url_count']} URLs, {len(result['product_or_service_urls'])} product/service URLs", flush=True)
    aggregate_results = load_all_client_results() if args.client else results
    write_aggregate(aggregate_results)
    print(f"Aggregate JSON: {AGG_JSON.relative_to(ROOT)}")
    print(f"Aggregate HTML: {AGG_HTML.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
