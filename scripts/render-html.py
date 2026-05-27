#!/usr/bin/env python3
"""
Render a final content draft from Markdown into clean semantic HTML.

The pipeline's final delivery artifact is HTML (decision: 2026-05-27 sync).
Generating HTML directly out of an MD source is deterministic and free of
LLM cost — the previous path (upload .md to Google Drive, let Drive convert)
burned tokens on every re-upload and produced inconsistent heading mapping.
This script does the conversion locally, preserving H1/H2/H3, lists,
tables, emphasis, and image tags inline so the downstream Google Doc
import keeps the structure.

Usage:
    python3 scripts/render-html.py <path-to-draft.md> [--out <path>] [--title <title>]

    <path-to-draft.md>   Required. The final MD draft (post-pipeline).
    --out <path>         Optional. Output path. Defaults to same path with .html.
    --title <title>      Optional. Used in <title> and the leading <h1>. Defaults to
                         the first H1 in the document, or the file stem.

Exit codes:
    0  success
    1  input error (missing file, unreadable)
    2  dependency missing
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import markdown
except ImportError:
    print("Missing dependency: markdown. Install with: pip install markdown", file=sys.stderr)
    sys.exit(2)

MD_EXTENSIONS = [
    "extra",          # tables, fenced code, footnotes, attr_list, def_list, abbr
    "sane_lists",     # consistent list parsing
    "smarty",         # smart quotes (but we already strip em-dashes upstream)
    "toc",            # heading IDs for anchor linking
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="generator" content="content-ops/render-html">
<meta name="source-md" content="{source}">
<meta name="rendered-at" content="{rendered_at}">
</head>
<body>
{body}
</body>
</html>
"""


def first_h1(md_text: str) -> str | None:
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            return stripped[2:].strip()
    return None


def strip_frontmatter(md_text: str) -> str:
    """Remove a leading `---` ... `---` YAML frontmatter block.

    Pipeline drafts carry frontmatter (url, meta_title, meta_description, source, etc.)
    that is operational metadata, not publishable copy. The HTML delivery artifact
    must not surface it as visible body text.
    """
    if not md_text.startswith("---"):
        return md_text
    lines = md_text.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != "---":
        return md_text
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return "".join(lines[i + 1:]).lstrip("\n")
    return md_text


def render(md_path: Path, out_path: Path, title: str | None) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    md_text = strip_frontmatter(md_text)

    page_title = title or first_h1(md_text) or md_path.stem.replace("-", " ").title()

    html_body = markdown.markdown(md_text, extensions=MD_EXTENSIONS, output_format="html")

    rendered_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    source_rel = md_path.as_posix()

    full_html = HTML_TEMPLATE.format(
        title=page_title,
        source=source_rel,
        rendered_at=rendered_at,
        body=html_body,
    )

    out_path.write_text(full_html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Markdown draft into clean semantic HTML.")
    parser.add_argument("md_path", type=Path, help="Path to the final MD draft.")
    parser.add_argument("--out", type=Path, default=None, help="Output HTML path. Defaults to the same path with .html extension.")
    parser.add_argument("--title", type=str, default=None, help="Override the <title> and leading H1. Defaults to the document's first H1.")
    args = parser.parse_args()

    if not args.md_path.exists():
        print(f"error: input file does not exist: {args.md_path}", file=sys.stderr)
        return 1

    if not args.md_path.is_file():
        print(f"error: input path is not a file: {args.md_path}", file=sys.stderr)
        return 1

    out_path = args.out or args.md_path.with_suffix(".html")

    render(args.md_path, out_path, args.title)
    print(out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
