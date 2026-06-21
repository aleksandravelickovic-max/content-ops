#!/usr/bin/env python3
"""
Patch v5: Update 5 revised product HTML files with content from finalized
markdown drafts. Replaces: Details intro text, About modal, How It's Made
modal, Order & Shipping modal, and FAQ modal.
"""
import re
from pathlib import Path

HTML_DIR = Path(__file__).parent / 'revised'
MD_DIR   = Path(__file__).parent.parent / 'drafts' / 'product-pages'

SKU_MAP = [
    ('products--2x6-rectangle-oscura.html',            '2x6-rectangle-oscura.md'),
    ('products--8x9-hex-red-clay-cotto-tile.html',     '8x9-hex-red-clay.md'),
    ('products--absinthe-2x6-zellige-tile.html',        'absinthe-2x6-bejmat-zellige.md'),
    ('products--absinthe-trapezoid-zellige-tile.html',  'absinthe-trapezoid.md'),
    ('products--aegean-zellige-tile.html',              'aegean-4x4.md'),
]

PROP65_HTML = (
    '<p><em>⚠ WARNING: Cancer and Reproductive Harm.</em> '
    '<a href="https://www.ziatile.com/proposition-65-warnings">'
    '<em>Learn more about Proposition 65 Warnings.</em></a></p>'
)

MODAL_CONTENT_DIV = (
    '<div class="product-content-modal__content text-wrapper '
    'body body--regular" contenteditable="true">'
)

DETAILS_DIV = (
    '<div class="body body--small-desktop body--regular text-wrapper" '
    'contenteditable="true">'
)
# Zellige pages put the editable layer one div deeper
ZELLIGE_DETAILS_DIV = '<div class="metafield-rich_text_field" contenteditable="true">'


# ── Inline markdown → HTML ─────────────────────────────────────────────────────

def convert_inline(text):
    # Unescape markdown backslash sequences first
    text = re.sub(r'\\(.)', r'\1', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic (must follow bold)
    text = re.sub(r'\*([^*\n]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_\n]+)_', r'<em>\1</em>', text)
    return text


def md_block_to_html(text):
    """Convert a markdown block to HTML paragraphs and headings."""
    lines = text.split('\n')
    html_parts = []
    para_lines = []

    def flush():
        joined = ' '.join(l.strip() for l in para_lines if l.strip())
        if joined:
            html_parts.append(f'<p>{convert_inline(joined)}</p>')
        para_lines.clear()

    for line in lines:
        s = line.strip()
        if s.startswith('### '):
            flush()
            html_parts.append(f'<h3>{convert_inline(s[4:])}</h3>')
        elif s.startswith('#### '):
            flush()
            # Sub-headings inside sections — render as h4
            html_parts.append(f'<h4>{convert_inline(s[5:])}</h4>')
        elif s.startswith('## ') or s.startswith('# '):
            flush()
        elif s == '---' or s == '' or s == '[KEEP]' or '\\[KEEP\\]' in s:
            flush()
        elif s.startswith('[INSERT') or '\\[INSERT' in s:
            flush()
        elif s.startswith('[IMAGE') or '\\[IMAGE' in s:
            flush()
        elif s.startswith('|'):
            flush()  # Skip table rows
        elif re.match(r'^[:\-]+$', s) or re.match(r'^\|[-: |]+\|$', s):
            flush()  # Skip table separators
        else:
            para_lines.append(s)

    flush()
    return '\n'.join(html_parts)


# ── Markdown section extraction ────────────────────────────────────────────────

def extract_intro(md_text):
    """Lines between [INSERT CART MODULE HERE] and [IMAGE:..."""
    lines = md_text.split('\n')
    collecting = False
    intro_lines = []
    for line in lines:
        # Match both escaped (\[...\]) and plain ([...]) variants
        if 'INSERT CART MODULE HERE' in line:
            collecting = True
            continue
        if collecting and 'IMAGE:' in line and ('[IMAGE:' in line or r'\[IMAGE:' in line):
            break
        if collecting:
            s = line.strip()
            if s == '---':
                continue
            intro_lines.append(line)
    return '\n'.join(intro_lines)


def extract_sections(md_text):
    """Return dict of section_name → section_body for every ## heading."""
    # Strip YAML frontmatter
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        if len(parts) >= 3:
            md_text = parts[2]

    sections = {}
    blocks = re.split(r'\n---\n', md_text)
    for block in blocks:
        lines = block.strip().split('\n')
        for i, line in enumerate(lines):
            s = line.strip()
            if s.startswith('## '):
                raw_name = s[3:].strip()
                # Remove trailing *\[Locked\]* and variants
                name = re.sub(r'\s*\*?\\\[Locked\\\]\*?', '', raw_name).strip()
                name = re.sub(r'\s*\*?\[Locked\]\*?', '', name).strip()
                sections[name] = '\n'.join(lines[i + 1:]).strip()
                break
    return sections


# ── HTML replacement helpers ───────────────────────────────────────────────────

def replace_modal_content(html, modal_class, new_html, append_prop65=False):
    """Replace the contenteditable body of a specific product modal."""
    tag = f'<div class="product-content-modal product-content-modal--{modal_class}">'
    modal_idx = html.find(tag)
    if modal_idx < 0:
        return html, False

    cd_idx = html.find(MODAL_CONTENT_DIV, modal_idx + len(tag))
    if cd_idx < 0:
        return html, False

    content_start = cd_idx + len(MODAL_CONTENT_DIV)
    end_idx = html.find('</div></div>', content_start)
    if end_idx < 0:
        return html, False

    body = new_html
    if append_prop65:
        body = new_html + '\n' + PROP65_HTML

    return html[:content_start] + body + html[end_idx:], True


def replace_details_content(html, new_html):
    """Replace product intro — handles Cotto and Zellige HTML structures."""
    # Cotto: contenteditable on the wrapper div itself
    idx = html.find(DETAILS_DIV)
    if idx >= 0:
        content_start = idx + len(DETAILS_DIV)
        end_idx = html.find('\n</div>', content_start)
        if end_idx >= 0:
            return html[:content_start] + '\n' + new_html + '\n' + html[end_idx:], True

    # Zellige: contenteditable on inner metafield div inside product-details__info
    info_idx = html.find('product-details__info')
    if info_idx < 0:
        return html, False

    # Stay within the __info section (stop before __details)
    details_boundary = html.find('product-details__details', info_idx)
    search_end = details_boundary if details_boundary > 0 else info_idx + 20000

    meta_idx = html.find(ZELLIGE_DETAILS_DIV, info_idx, search_end)
    if meta_idx < 0:
        return html, False

    content_start = meta_idx + len(ZELLIGE_DETAILS_DIV)
    end_idx = html.find('</div>', content_start)
    if end_idx < 0:
        return html, False

    return html[:content_start] + new_html + html[end_idx:], True


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    for html_name, md_name in SKU_MAP:
        html_path = HTML_DIR / html_name
        md_path   = MD_DIR / md_name

        if not html_path.exists():
            print(f'SKIP  {html_name}  (HTML not found)')
            continue
        if not md_path.exists():
            print(f'SKIP  {md_name}  (markdown not found)')
            continue

        print(f'\n── {html_name}')

        md_text  = md_path.read_text(encoding='utf-8')
        html     = html_path.read_text(encoding='utf-8')
        sections = extract_sections(md_text)
        intro    = extract_intro(md_text)
        saved    = 0

        # 1. Details / intro text
        if intro.strip():
            ih = md_block_to_html(intro)
            if ih:
                html, ok = replace_details_content(html, ih)
                print(f'  {"✓" if ok else "✗"}  Details/intro')
                saved += ok

        # 2. About
        about = sections.get('About', '')
        if about:
            html, ok = replace_modal_content(
                html, 'about', md_block_to_html(about), append_prop65=True
            )
            print(f'  {"✓" if ok else "✗"}  About')
            saved += ok

        # 3. How It's Made  (handle both straight and curly apostrophe)
        made = sections.get("How It’s Made", sections.get("How It's Made", ''))
        if made:
            html, ok = replace_modal_content(html, 'info', md_block_to_html(made))
            print(f'  {"✓" if ok else "✗"}  How It\'s Made')
            saved += ok

        # 4. Order & Shipping
        orders = sections.get('Order & Shipping', '')
        if orders:
            html, ok = replace_modal_content(html, 'orders', md_block_to_html(orders))
            print(f'  {"✓" if ok else "✗"}  Order & Shipping')
            saved += ok

        # 5. FAQ
        faq = sections.get('Frequently Asked Questions', '')
        if faq:
            html, ok = replace_modal_content(html, 'faq', md_block_to_html(faq))
            print(f'  {"✓" if ok else "✗"}  FAQ')
            saved += ok

        if saved:
            html_path.write_text(html, encoding='utf-8')
            print(f'  → Saved  ({saved}/5 sections replaced)')
        else:
            print(f'  !  No sections matched — file unchanged')


if __name__ == '__main__':
    main()
