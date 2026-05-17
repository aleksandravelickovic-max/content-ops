#!/usr/bin/env python3
"""
Build editable HTML content previews for the Altify May 2026 campaign.
Uses stdlib only — no external dependencies required.

Usage:
    python3 scripts/build-altify-html.py [--fetch] [--skip-fetch]

    --fetch       Fetch original HTML from altify.com and inject content into the real layout
    --skip-fetch  Build clean standalone HTML files (default when no originals cached)
"""

import argparse
import html
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CAMPAIGN_DIR = REPO_ROOT / "clients" / "altify" / "campaigns" / "01-may-content-optimization"
DRAFTS_DIR = CAMPAIGN_DIR / "drafts"
HTML_DIR = CAMPAIGN_DIR / "html"
ORIGINAL_DIR = HTML_DIR / "original"
REVISED_DIR = HTML_DIR / "revised"

FETCH_DELAY = 2.0
USER_AGENT = "AltifyContentOps/1.0 (internal content audit)"

PAGES = [
    {
        "slug": "01-account-planning-challenges",
        "url": "https://altify.com/blog/the-biggest-account-planning-challenges-how-you-can-fix-them-part-1/",
        "draft": "01-account-planning-challenges.md",
        "label": "Strategic Account Planning Challenges (Consolidated)",
    },
    {
        "slug": "02-maxai-guided-selling",
        "url": "https://altify.com/maxai/",
        "draft": "02-maxai-guided-selling.md",
        "label": "MaxAI — Guided Selling in Salesforce",
    },
    {
        "slug": "03-relationship-mapping",
        "url": "https://altify.com/blog/forecast-management-challenges-you-have-a-relationship-problem/",
        "draft": "03-relationship-mapping.md",
        "label": "Relationship Mapping for Enterprise B2B Sales",
    },
    {
        "slug": "04-strategic-account-planning",
        "url": "https://altify.com/blog/strategic-account-planning-enterprise-sales/",
        "draft": "04-strategic-account-planning.md",
        "label": "Strategic Account Planning for Enterprise Sales",
    },
    {
        "slug": "05-revenue-execution-salesforce",
        "url": "",
        "draft": "05-revenue-execution-salesforce.md",
        "label": "Revenue Execution in Salesforce: Enterprise Guide",
    },
]


# ---------------------------------------------------------------------------
# Minimal markdown → HTML converter (handles what we need)
# ---------------------------------------------------------------------------

def md_to_html(text: str) -> str:
    lines = text.split("\n")
    out = []
    in_ul = False
    in_ol = False
    in_p = False
    para_lines = []

    def flush_para():
        nonlocal in_p, para_lines
        if para_lines:
            content = inline_md(" ".join(para_lines).strip())
            if content:
                out.append(f"<p>{content}</p>")
        para_lines = []
        in_p = False

    def close_list():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for line in lines:
        # Blank line
        if not line.strip():
            flush_para()
            close_list()
            continue

        # HR
        if re.match(r'^---+$', line.strip()):
            flush_para()
            close_list()
            out.append("<hr>")
            continue

        # Headings
        h_match = re.match(r'^(#{1,6})\s+(.+)', line)
        if h_match:
            flush_para()
            close_list()
            level = len(h_match.group(1))
            content = inline_md(h_match.group(2).strip())
            slug = re.sub(r'[^a-z0-9]+', '-', content.lower()).strip('-')
            out.append(f'<h{level} id="{slug}">{content}</h{level}>')
            continue

        # Unordered list
        ul_match = re.match(r'^[-*]\s+(.+)', line)
        if ul_match:
            flush_para()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(ul_match.group(1).strip())}</li>")
            continue

        # Ordered list
        ol_match = re.match(r'^\d+\.\s+(.+)', line)
        if ol_match:
            flush_para()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline_md(ol_match.group(1).strip())}</li>")
            continue

        # Normal paragraph line
        flush_para() if (in_ul or in_ol) else None
        close_list() if line.strip() and not ul_match and not ol_match and (in_ul or in_ol) else None
        para_lines.append(line)

    flush_para()
    close_list()
    return "\n".join(out)


def inline_md(text: str) -> str:
    # Escape HTML first (but preserve existing entities from our links)
    # Process links: [text](url)
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>',
        text
    )
    # Bold+italic: ***text***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code: `text`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


# ---------------------------------------------------------------------------
# Parse draft frontmatter
# ---------------------------------------------------------------------------

def parse_draft(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    meta_title_m = re.search(r'\*\*Meta Title[:\*]*\s*(.+)', text, re.IGNORECASE)
    meta_desc_m = re.search(r'\*\*Meta Description[:\*]*\s*(.+)', text, re.IGNORECASE)

    lines = text.split("\n")
    body_start = 0
    for idx, line in enumerate(lines):
        if line.startswith("#"):
            body_start = idx
            break
    body = "\n".join(lines[body_start:]).strip()

    return {
        "meta_title": meta_title_m.group(1).strip() if meta_title_m else "",
        "meta_description": meta_desc_m.group(1).strip() if meta_desc_m else "",
        "body_md": body,
        "body_html": md_to_html(body),
    }


# ---------------------------------------------------------------------------
# Fetch originals
# ---------------------------------------------------------------------------

def fetch_page(url: str) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def fetch_all_originals(pages: list[dict]):
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(pages):
        out_path = ORIGINAL_DIR / f"{page['slug']}.html"
        if out_path.exists():
            print(f"  [{i+1}/{len(pages)}] CACHED {page['slug']}.html")
            continue
        print(f"  [{i+1}/{len(pages)}] Fetching {page['url']} ...")
        html_content = fetch_page(page["url"])
        if html_content:
            out_path.write_text(html_content, encoding="utf-8")
            print(f"    → saved ({len(html_content):,} bytes)")
        else:
            print("    → FAILED")
        if i < len(pages) - 1:
            time.sleep(FETCH_DELAY)


# ---------------------------------------------------------------------------
# Inject content into live page HTML (stdlib only — regex-based)
# ---------------------------------------------------------------------------

def inject_into_live_page(original_html: str, draft: dict, page: dict) -> str:
    result = original_html

    # Update <title>
    if draft["meta_title"]:
        result = re.sub(
            r'<title>[^<]*</title>',
            f'<title>{html.escape(draft["meta_title"])}</title>',
            result, count=1
        )

    # Update meta description
    if draft["meta_description"]:
        result = re.sub(
            r'(<meta[^>]+name=["\']description["\'][^>]+content=["\'])[^"\']*(["\'])',
            lambda m: m.group(1) + html.escape(draft["meta_description"]) + m.group(2),
            result
        )
        result = re.sub(
            r'(<meta[^>]+content=["\'])[^"\']*(["\'][^>]+name=["\']description["\'])',
            lambda m: m.group(1) + html.escape(draft["meta_description"]) + m.group(2),
            result
        )

    # Try to replace article / main content area
    new_content = f"""<div contenteditable="true" spellcheck="true" style="
  outline:none;border:2px dashed transparent;border-radius:4px;
  transition:border-color 0.2s;padding:4px;
" onfocus="this.style.borderColor='#4F6AF0'" onblur="this.style.borderColor='transparent'">
{draft["body_html"]}
</div>"""

    # Try <article> first
    replaced = False
    for pattern in [
        r'(<article[^>]*>)(.*?)(</article>)',
        r'(<div[^>]+class=["\'][^"\']*entry-content[^"\']*["\'][^>]*>)(.*?)(</div>)',
        r'(<div[^>]+class=["\'][^"\']*post-content[^"\']*["\'][^>]*>)(.*?)(</div>)',
        r'(<div[^>]+class=["\'][^"\']*article-body[^"\']*["\'][^>]*>)(.*?)(</div>)',
        r'(<main[^>]*>)(.*?)(</main>)',
    ]:
        m = re.search(pattern, result, re.DOTALL | re.IGNORECASE)
        if m:
            result = result[:m.start(2)] + new_content + result[m.end(2):]
            replaced = True
            break

    if not replaced:
        # Inject before </body>
        result = result.replace("</body>", f"<div style='max-width:820px;margin:60px auto;padding:0 32px'>{new_content}</div></body>")

    # Inject banner + print style before </head>
    banner = build_banner_html(page)
    result = result.replace("</head>", f"<style>@media print{{#altify-banner{{display:none!important}}}}</style></head>")
    result = result.replace("<body>", f"<body>{banner}")
    if "<body>" not in result:
        result = result.replace("<body ", f"<body ", 1)
        body_m = re.search(r'<body[^>]*>', result)
        if body_m:
            pos = body_m.end()
            result = result[:pos] + banner + result[pos:]

    return result


def build_banner_html(page: dict) -> str:
    return f"""<div id="altify-banner" style="position:fixed;top:0;left:0;right:0;z-index:99999;
  background:#1B3A6B;color:#fff;display:flex;align-items:center;
  justify-content:space-between;padding:0 20px;height:44px;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,0.25)">
  <div style="display:flex;align-items:center;gap:12px">
    <span style="background:#FF6B35;color:#fff;font-size:10px;font-weight:700;
      letter-spacing:0.08em;padding:3px 8px;border-radius:3px;text-transform:uppercase">DRAFT</span>
    <span style="opacity:0.9">{page["label"]}</span>
    <span style="opacity:0.5;font-size:11px">· Content Optimization · May 2026</span>
  </div>
  <div style="display:flex;align-items:center;gap:16px;font-size:12px;opacity:0.85">
    <span>✏️ Click text to edit</span>
    <button onclick="window.print()" style="background:rgba(255,255,255,0.15);
      border:1px solid rgba(255,255,255,0.3);color:#fff;padding:4px 12px;
      border-radius:4px;cursor:pointer;font-size:12px">Print / Save PDF</button>
  </div>
</div>
<div style="height:44px"></div>"""


# ---------------------------------------------------------------------------
# Standalone HTML (no live page)
# ---------------------------------------------------------------------------

ALTIFY_CSS = """
*, *::before, *::after { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 17px;
  line-height: 1.75;
  color: #1a1a2e;
  background: #f0f2f7;
}
.page-wrapper {
  max-width: 820px;
  margin: 0 auto;
  padding: 48px 40px 80px;
  background: #fff;
  min-height: 100vh;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.06), 0 4px 24px rgba(0,0,0,0.06);
}
.meta-box {
  background: #f0f4ff;
  border: 1px solid #cdd5f5;
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 36px;
  font-size: 13px;
  color: #444;
  line-height: 1.6;
}
.meta-box strong { color: #1B3A6B; }
.meta-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #1B3A6B;
  margin-bottom: 4px;
}
h1 {
  font-size: 34px;
  font-weight: 800;
  line-height: 1.2;
  color: #1B3A6B;
  margin: 0 0 32px;
  padding-bottom: 24px;
  border-bottom: 3px solid #e8ecf4;
}
h2 {
  font-size: 26px;
  font-weight: 700;
  color: #1B3A6B;
  margin: 52px 0 16px;
  border-bottom: 1px solid #e8ecf4;
  padding-bottom: 8px;
}
h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1B3A6B;
  margin: 36px 0 12px;
}
h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2d4a7a;
  margin: 24px 0 8px;
}
p { margin: 0 0 18px; }
ul, ol {
  margin: 0 0 18px;
  padding-left: 26px;
}
li { margin-bottom: 8px; }
a { color: #4F6AF0; text-decoration: none; }
a:hover { text-decoration: underline; }
strong { color: #111; font-weight: 600; }
em { color: #333; }
hr { border: none; border-top: 2px solid #e8ecf4; margin: 48px 0; }
code {
  background: #f0f2f7;
  border-radius: 3px;
  padding: 2px 6px;
  font-size: 14px;
  font-family: 'SF Mono', 'Fira Code', monospace;
}
[contenteditable]:focus {
  outline: 2px solid #4F6AF0;
  outline-offset: 6px;
  border-radius: 4px;
}
@media print {
  #altify-banner { display: none !important; }
  body { background: #fff; }
  .page-wrapper { box-shadow: none; padding: 0; }
  [contenteditable]:focus { outline: none; }
}
"""


def build_standalone_html(draft: dict, page: dict) -> str:
    banner = build_banner_html(page)
    meta_title_esc = html.escape(draft["meta_title"])
    meta_desc_esc = html.escape(draft["meta_description"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta_title_esc}</title>
<meta name="description" content="{meta_desc_esc}">
<style>{ALTIFY_CSS}</style>
</head>
<body>
{banner}
<div class="page-wrapper">
  <div class="meta-box">
    <div class="meta-label">Meta title</div>
    <div contenteditable="true" spellcheck="true" style="font-weight:600;color:#1B3A6B;margin-bottom:10px">{draft["meta_title"]}</div>
    <div class="meta-label">Meta description</div>
    <div contenteditable="true" spellcheck="true">{draft["meta_description"]}</div>
  </div>
  <div contenteditable="true" spellcheck="true">
{draft["body_html"]}
  </div>
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

def build_index(pages: list[dict]):
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for page in pages:
        original_exists = (ORIGINAL_DIR / f"{page['slug']}.html").exists()
        revised_exists = (REVISED_DIR / f"{page['slug']}.html").exists()
        orig_link = f'<a href="original/{page["slug"]}.html" target="_blank">Original</a>' if original_exists else '<span style="color:#bbb">—</span>'
        rev_link = f'<a href="revised/{page["slug"]}.html" target="_blank">Revised ✏️</a>' if revised_exists else '<span style="color:#bbb">—</span>'
        status = "🟢" if revised_exists else "⚪"
        rows.append(f"""<tr>
  <td style="width:32px">{status}</td>
  <td><strong style="color:#1B3A6B">{page["slug"]}</strong></td>
  <td>{page["label"]}</td>
  <td><a href="{page["url"]}" target="_blank" style="font-size:12px;color:#888">{page["url"]}</a></td>
  <td>{orig_link}</td>
  <td>{rev_link}</td>
</tr>""")

    revised_count = sum(1 for p in pages if (REVISED_DIR / f"{p['slug']}.html").exists())
    original_count = sum(1 for p in pages if (ORIGINAL_DIR / f"{p['slug']}.html").exists())
    ts = time.strftime("%Y-%m-%d %H:%M")

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Altify — Content Optimization · May 2026</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f0f2f7; color: #1a1a2e; line-height: 1.6; }}
.container {{ max-width: 1140px; margin: 0 auto; padding: 48px 24px; }}
.header {{ margin-bottom: 6px; display: flex; align-items: center; gap: 14px; }}
.badge {{ background: #FF6B35; color: #fff; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; padding: 4px 10px; border-radius: 3px; text-transform: uppercase; }}
h1 {{ font-size: 28px; font-weight: 800; color: #1B3A6B; }}
.subtitle {{ color: #888; font-size: 13px; margin-bottom: 32px; }}
.stats {{ display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }}
.stat {{ background: #fff; border: 1px solid #e0e4ef; padding: 16px 24px; border-radius: 10px; min-width: 130px; }}
.stat-num {{ font-size: 30px; font-weight: 800; color: #1B3A6B; }}
.stat-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: #aaa; margin-top: 2px; }}
.instructions {{ background: #f0f4ff; border: 1px solid #cdd5f5; padding: 14px 18px; border-radius: 8px; margin-bottom: 28px; font-size: 14px; color: #444; }}
table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #e0e4ef; border-radius: 10px; overflow: hidden; }}
th {{ text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #1B3A6B; padding: 12px 16px; border-bottom: 2px solid #e8ecf4; background: #f8f9fc; }}
td {{ padding: 14px 16px; border-bottom: 1px solid #f0f2f7; font-size: 14px; vertical-align: middle; }}
tr:last-child td {{ border-bottom: none; }}
tr:hover {{ background: #f8f9ff; }}
a {{ color: #4F6AF0; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <span class="badge">Draft</span>
    <h1>Altify — Content Optimization</h1>
  </div>
  <p class="subtitle">Campaign: 01 May 2026 · Generated {ts} · CSM: Chanakya Thakkar</p>
  <div class="stats">
    <div class="stat"><div class="stat-num">4</div><div class="stat-label">Pieces</div></div>
    <div class="stat"><div class="stat-num">{revised_count}</div><div class="stat-label">Revised</div></div>
    <div class="stat"><div class="stat-num">{original_count}</div><div class="stat-label">Live Layouts</div></div>
  </div>
  <div class="instructions">
    <strong>How to use:</strong> Click <strong>Revised ✏️</strong> to open the optimized page — click any text to edit it directly in the browser.
    Use <em>Print / Save PDF</em> to export for the client. Run <code>python3 scripts/build-altify-html.py --fetch</code> to pull the real Altify layouts.
  </div>
  <table>
    <thead>
      <tr><th></th><th>Topic</th><th>Page</th><th>Live URL</th><th>Original</th><th>Revised</th></tr>
    </thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>
</body>
</html>"""

    (HTML_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Index: {HTML_DIR / 'index.html'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_revised_pages(pages: list[dict]):
    REVISED_DIR.mkdir(parents=True, exist_ok=True)
    stats = {"revised": 0, "standalone": 0, "errors": 0}

    for page in pages:
        draft_path = DRAFTS_DIR / page["draft"]
        if not draft_path.exists():
            print(f"  MISSING draft: {page['draft']}")
            stats["errors"] += 1
            continue

        draft = parse_draft(draft_path)
        original_path = ORIGINAL_DIR / f"{page['slug']}.html"
        revised_path = REVISED_DIR / f"{page['slug']}.html"

        try:
            if original_path.exists():
                original_html = original_path.read_text(encoding="utf-8")
                revised_html = inject_into_live_page(original_html, draft, page)
                mode = "REVISED (live layout)"
                stats["revised"] += 1
            else:
                revised_html = build_standalone_html(draft, page)
                mode = "STANDALONE"
                stats["standalone"] += 1

            revised_path.write_text(revised_html, encoding="utf-8")
            print(f"  {mode}: {page['slug']}.html")

        except Exception as e:
            import traceback
            print(f"  ERROR {page['slug']}: {e}")
            traceback.print_exc()
            stats["errors"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--skip-fetch", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    pages = PAGES[:args.limit] if args.limit else PAGES

    if args.fetch and not args.skip_fetch:
        print(f"Fetching {len(pages)} pages from altify.com...")
        fetch_all_originals(pages)

    print(f"\nBuilding revised pages...")
    stats = build_revised_pages(pages)
    print(f"  Revised: {stats['revised']}  Standalone: {stats['standalone']}  Errors: {stats['errors']}")

    print("\nBuilding index...")
    build_index(pages)

    print(f"\nDone! Open: {HTML_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
