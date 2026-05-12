#!/usr/bin/env python3
"""Build the Zia Tile knowledge static site from source markdown files.

Run from repo root: python3 zia/knowledge-site/_build.py
"""

from pathlib import Path
import markdown
import re
import html

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_DIR = REPO_ROOT / "zia" / "knowledge-site"
KNOWLEDGE_DIR = REPO_ROOT / "knowledge" / "products" / "zia-tile"

PAGES = [
    {
        "slug": "index",
        "title": "Overview",
        "nav_label": "Overview",
        "section": None,
        "source": None,
        "intro": True,
    },
    {
        "slug": "style-guide",
        "title": "Style Guide v2.0",
        "nav_label": "Style Guide v2.0",
        "section": "Editorial",
        "source": KNOWLEDGE_DIR / "style-guide-v2.md",
        "subtitle": "Source of truth for product page copy. April 2026.",
    },
    {
        "slug": "editorial-voice",
        "title": "Editorial Voice Research",
        "nav_label": "Editorial Voice",
        "section": "Editorial",
        "source": KNOWLEDGE_DIR / "editorial-voice-research-2026-05-04.md",
        "subtitle": "Voice cheat-sheet for collection pages and blogs. AD-style references.",
    },
    {
        "slug": "website-research-2026-05-04",
        "title": "Website Research — May 2026",
        "nav_label": "Website Research (May 2026)",
        "section": "Reference",
        "source": KNOWLEDGE_DIR / "website-research-2026-05-04.md",
        "subtitle": "Verbatim hero copy, colorways, shapes, finishes for every collection.",
    },
    {
        "slug": "website-research-original",
        "title": "Website Research — Original",
        "nav_label": "Website Research (Original)",
        "section": "Reference",
        "source": KNOWLEDGE_DIR / "website-research.md",
        "subtitle": "Earlier draft of the website research file.",
    },
    {
        "slug": "installation-guides",
        "title": "Installation Guides Research",
        "nav_label": "Installation Guides",
        "section": "Reference",
        "source": KNOWLEDGE_DIR / "installation-guides-research.md",
        "subtitle": "Notes on installation guide structure across collections.",
    },
    {
        "slug": "workspace",
        "title": "Workspace README",
        "nav_label": "Workspace README",
        "section": "Workspace",
        "source": REPO_ROOT / "zia" / "README.md",
        "subtitle": "Project landing page for the Zia Tile workspace.",
    },
]

CSS = """
:root {
  --bg: #f6f1e8;
  --paper: #fbf7ee;
  --ink: #1c1a17;
  --ink-soft: #4a463f;
  --rule: #d9cfb9;
  --accent: #8a3324;
  --accent-soft: #c47a52;
  --sidebar-bg: #1c1a17;
  --sidebar-ink: #efe6d2;
  --sidebar-ink-dim: #948a73;
  --code-bg: #efe6d2;
  --serif: "Cormorant Garamond", "Playfair Display", Georgia, "Times New Roman", serif;
  --sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;
}

* { box-sizing: border-box; }

html, body { margin: 0; padding: 0; }

body {
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.65;
  color: var(--ink);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  background: var(--sidebar-bg);
  color: var(--sidebar-ink);
  padding: 36px 28px 28px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  border-right: 1px solid #000;
}

.brand-mark {
  font-family: var(--serif);
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 0.5px;
  line-height: 1;
}

.brand-sub {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--sidebar-ink-dim);
  margin-top: 6px;
}

.sidebar nav { margin-top: 32px; }
.sidebar nav ul { list-style: none; padding: 0; margin: 0; }
.sidebar nav li { margin: 0; }

.sidebar nav a {
  display: block;
  color: var(--sidebar-ink);
  text-decoration: none;
  padding: 8px 0;
  font-size: 14px;
  border-bottom: 1px solid transparent;
  transition: color 0.15s;
}

.sidebar nav a:hover { color: var(--accent-soft); }

.sidebar nav a.active {
  color: var(--accent-soft);
  font-weight: 500;
}

.nav-section {
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--sidebar-ink-dim);
  margin-top: 24px;
  margin-bottom: 4px;
  padding-top: 12px;
  border-top: 1px solid #2c2925;
}

.sidebar .meta {
  margin-top: 36px;
  padding-top: 16px;
  border-top: 1px solid #2c2925;
  font-size: 11px;
  color: var(--sidebar-ink-dim);
}

/* Main */
main {
  padding: 64px 72px 96px;
  max-width: 920px;
}

.page-header {
  margin-bottom: 48px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--rule);
}

.eyebrow {
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 12px;
}

h1.page-title {
  font-family: var(--serif);
  font-weight: 600;
  font-size: 48px;
  line-height: 1.1;
  margin: 0 0 12px;
  letter-spacing: -0.01em;
}

.subtitle {
  font-family: var(--serif);
  font-style: italic;
  font-size: 20px;
  color: var(--ink-soft);
  margin: 0;
  font-weight: 400;
}

/* Prose */
.prose h1, .prose h2, .prose h3, .prose h4 {
  font-family: var(--serif);
  font-weight: 600;
  color: var(--ink);
  letter-spacing: -0.005em;
}

.prose h1 {
  font-size: 36px;
  margin-top: 56px;
  margin-bottom: 16px;
  line-height: 1.15;
}

.prose h2 {
  font-size: 28px;
  margin-top: 48px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--rule);
  line-height: 1.2;
}

.prose h3 {
  font-size: 21px;
  margin-top: 36px;
  margin-bottom: 8px;
  line-height: 1.3;
}

.prose h4 {
  font-size: 17px;
  margin-top: 28px;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
}

.prose p {
  margin: 0 0 16px;
}

.prose a {
  color: var(--accent);
  text-decoration: underline;
  text-decoration-color: var(--accent-soft);
  text-underline-offset: 3px;
}

.prose a:hover { color: var(--accent-soft); }

.prose ul, .prose ol {
  margin: 0 0 18px;
  padding-left: 22px;
}

.prose li { margin: 4px 0; }

.prose blockquote {
  margin: 24px 0;
  padding: 4px 0 4px 20px;
  border-left: 3px solid var(--accent-soft);
  font-family: var(--serif);
  font-style: italic;
  font-size: 19px;
  color: var(--ink-soft);
}

.prose code {
  font-family: var(--mono);
  font-size: 0.88em;
  background: var(--code-bg);
  padding: 1px 6px;
  border-radius: 3px;
  color: #5a3a1c;
}

.prose pre {
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: 16px 18px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 13px;
  margin: 18px 0;
}

.prose pre code {
  background: none;
  padding: 0;
  color: var(--ink);
}

.prose hr {
  border: none;
  border-top: 1px solid var(--rule);
  margin: 40px 0;
}

.prose strong { color: var(--ink); font-weight: 600; }

.prose .repo-link {
  color: var(--ink-soft);
  border-bottom: 1px dotted var(--rule);
  cursor: help;
}

.prose .repo-tag {
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent-soft);
  font-style: normal;
  margin-left: 4px;
}

/* Tables */
.prose table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0 28px;
  font-size: 14px;
  background: var(--paper);
}

.prose th {
  text-align: left;
  font-family: var(--sans);
  font-weight: 600;
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
  padding: 12px 14px;
  border-bottom: 2px solid var(--rule);
  background: transparent;
}

.prose td {
  padding: 12px 14px;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}

.prose tr:last-child td { border-bottom: none; }

.prose table code { font-size: 12px; }

/* Index page cards */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin: 32px 0 40px;
}

.card {
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: 24px;
  text-decoration: none;
  color: inherit;
  display: block;
  transition: border-color 0.15s, transform 0.15s;
}

.card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.card .card-eyebrow {
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 8px;
}

.card h3 {
  font-family: var(--serif);
  font-size: 22px;
  margin: 0 0 8px;
  line-height: 1.2;
}

.card p {
  font-size: 14px;
  color: var(--ink-soft);
  margin: 0;
  line-height: 1.5;
}

.intro-lead {
  font-family: var(--serif);
  font-size: 22px;
  font-style: italic;
  line-height: 1.5;
  color: var(--ink-soft);
  margin: 0 0 32px;
  max-width: 680px;
}

/* Mobile */
.nav-toggle {
  display: none;
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 100;
  background: var(--sidebar-bg);
  color: var(--sidebar-ink);
  border: none;
  width: 44px;
  height: 44px;
  font-size: 20px;
  border-radius: 4px;
  cursor: pointer;
}

@media (max-width: 880px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar {
    position: fixed;
    top: 0;
    left: -300px;
    width: 280px;
    z-index: 50;
    transition: left 0.25s;
    height: 100vh;
  }
  .sidebar.open { left: 0; }
  .nav-toggle { display: block; }
  main { padding: 80px 24px 64px; }
  h1.page-title { font-size: 36px; }
  .prose h1 { font-size: 28px; }
  .prose h2 { font-size: 22px; }
}

/* Print */
@media print {
  .sidebar, .nav-toggle { display: none; }
  .layout { grid-template-columns: 1fr; }
  main { padding: 0; max-width: 100%; }
  body { background: white; }
  .prose pre { background: #f5f5f5; }
}
"""

NAV_JS = """
document.addEventListener('DOMContentLoaded', function() {
  var toggle = document.querySelector('.nav-toggle');
  var sidebar = document.querySelector('.sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', function() {
      sidebar.classList.toggle('open');
    });
  }
});
"""

INDEX_INTRO = """
<p class="intro-lead">A self-contained reference for everyone writing, editing, or designing for Zia Tile. The style guide governs product pages. The voice research governs blogs and editorial collection pages. The website research is the verbatim source for current site copy.</p>
"""

def build_nav(active_slug: str) -> str:
    """Render sidebar navigation HTML, marking the active page."""
    sections: dict[str | None, list[dict]] = {}
    order: list[str | None] = []
    for page in PAGES:
        sec = page["section"]
        if sec not in sections:
            sections[sec] = []
            order.append(sec)
        sections[sec].append(page)

    parts = ['<ul>']
    for sec in order:
        if sec is not None:
            parts.append(f'<li class="nav-section">{html.escape(sec)}</li>')
        for page in sections[sec]:
            cls = ' class="active"' if page["slug"] == active_slug else ""
            parts.append(
                f'<li><a href="{page["slug"]}.html"{cls}>{html.escape(page["nav_label"])}</a></li>'
            )
    parts.append("</ul>")
    return "\n".join(parts)


def build_index_body() -> str:
    cards = []
    for page in PAGES:
        if page["slug"] == "index":
            continue
        eyebrow = page["section"] or ""
        cards.append(
            f'<a class="card" href="{page["slug"]}.html">'
            f'<div class="card-eyebrow">{html.escape(eyebrow)}</div>'
            f'<h3>{html.escape(page["nav_label"])}</h3>'
            f'<p>{html.escape(page.get("subtitle", ""))}</p>'
            f"</a>"
        )
    grid = '<div class="card-grid">' + "".join(cards) + "</div>"

    body = INDEX_INTRO + grid + """
<h2>How to use this site</h2>
<p>Each section comes from a single source-of-truth markdown file in <code>knowledge/products/zia-tile/</code>. When facts change in the source, the file is regenerated; this static export should be rebuilt from the build script in the site folder.</p>

<h2>Voice precedence</h2>
<ul>
  <li><strong>Blogs and editorial collection pages</strong> follow the Editorial Voice Research — closer to <em>Architectural Digest</em> than to generic SaaS SEO.</li>
  <li><strong>Product pages</strong> follow the Style Guide v2.0 — required terminology, freeze/thaw rules, structured sections.</li>
  <li>When the two conflict on a collection page, the editorial voice wins; product-page sections defer to the style guide.</li>
</ul>

<h2>Final sign-off</h2>
<p>All Zia content: Aleksandra Velickovic.</p>
"""
    return body


def fix_internal_links(html_body: str, source_path: Path | None) -> str:
    """Rewrite local .md links to site pages; neutralize repo-only links."""
    mapping = {
        "../knowledge/products/zia-tile/style-guide-v2.md": "style-guide.html",
        "../knowledge/products/zia-tile/editorial-voice-research-2026-05-04.md": "editorial-voice.html",
        "../knowledge/products/zia-tile/editorial-voice-research-2026-05-04.html": "editorial-voice.html",
        "../knowledge/products/zia-tile/website-research-2026-05-04.md": "website-research-2026-05-04.html",
        "../knowledge/products/zia-tile/website-research-2026-05-04.html": "website-research-2026-05-04.html",
        "../knowledge/products/zia-tile/website-research.md": "website-research-original.html",
        "../knowledge/products/zia-tile/installation-guides-research.md": "installation-guides.html",
        "../knowledge/products/zia-tile/": "index.html",
        "style-guide-v2.md": "style-guide.html",
        "editorial-voice-research-2026-05-04.md": "editorial-voice.html",
        "website-research-2026-05-04.md": "website-research-2026-05-04.html",
        "website-research.md": "website-research-original.html",
        "installation-guides-research.md": "installation-guides.html",
    }
    for src, dst in mapping.items():
        html_body = html_body.replace(f'href="{src}"', f'href="{dst}"')

    # Neutralize remaining repo-only links (paths starting with ../ that point
    # at files outside the site). Replace the <a href="...">label</a> with a
    # span carrying a "(repo only)" marker so the export stays self-contained.
    def neutralize(match: re.Match) -> str:
        href = match.group(1)
        label = match.group(2)
        return f'<span class="repo-link" title="Repo path: {html.escape(href)}">{label} <em class="repo-tag">(repo only)</em></span>'

    html_body = re.sub(
        r'<a href="(\.\./[^"]+)">([^<]+)</a>',
        neutralize,
        html_body,
    )
    return html_body


def render_markdown(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
        output_format="html5",
    )
    html_body = md.convert(text)
    return html_body


def page_template(page: dict, body_html: str) -> str:
    nav_html = build_nav(page["slug"])
    eyebrow = page["section"] or "Knowledge Base"
    subtitle_html = (
        f'<p class="subtitle">{html.escape(page.get("subtitle", ""))}</p>'
        if page.get("subtitle")
        else ""
    )
    title = page["title"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} — Zia Tile Knowledge</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<button class="nav-toggle" aria-label="Toggle navigation">☰</button>
<div class="layout">
<aside class="sidebar">
<div class="brand">
<div class="brand-mark">Zia Tile</div>
<div class="brand-sub">Knowledge Base</div>
</div>
<nav>
{nav_html}
</nav>
<div class="meta">Last updated 2026-05-07</div>
</aside>
<main>
<div class="page-header">
<div class="eyebrow">{html.escape(eyebrow)}</div>
<h1 class="page-title">{html.escape(title)}</h1>
{subtitle_html}
</div>
<article class="prose">
{body_html}
</article>
</main>
</div>
<script src="nav.js"></script>
</body>
</html>
"""


def main() -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / "styles.css").write_text(CSS, encoding="utf-8")
    (SITE_DIR / "nav.js").write_text(NAV_JS, encoding="utf-8")

    for page in PAGES:
        if page["slug"] == "index":
            body = build_index_body()
        else:
            source = page["source"]
            body = render_markdown(source)
            body = fix_internal_links(body, source)
            # Strip the leading H1 from the source if it duplicates the page title,
            # since we already render the title in the page header.
            body = re.sub(
                r'^\s*<h1[^>]*>.*?</h1>\s*',
                '',
                body,
                count=1,
                flags=re.DOTALL,
            )
        out = page_template(page, body)
        (SITE_DIR / f"{page['slug']}.html").write_text(out, encoding="utf-8")
        print(f"wrote {page['slug']}.html")


if __name__ == "__main__":
    main()
