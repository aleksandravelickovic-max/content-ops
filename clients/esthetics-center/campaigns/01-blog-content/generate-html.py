#!/usr/bin/env python3
"""
Generate HTML preview replicas of Esthetics Center blog posts.
Reads markdown drafts + briefs, outputs Webflow-styled HTML files for client preview.
"""
import os
import re

BASE = "/home/thema/work/content-ops/clients/esthetics-center/campaigns/01-blog-content"
DRAFTS_DIR = os.path.join(BASE, "drafts")
BRIEFS_DIR = os.path.join(BASE, "briefs")
OUTPUT_DIR = os.path.join(BASE, "html")

HERO_IMAGE = "https://cdn.prod.website-files.com/61ce73519eba121f1f149ad0/6a16b7fd97a42b0a20060815_esthetics-center-under-eye-filler.avif"

NAV_HTML = (
    '<div data-animation="default" data-collapse="medium" data-duration="400" '
    'data-easing="ease" data-easing2="ease" role="banner" class="navbar-5 w-nav">'
    '<div class="navbar-container blog">'
    '<a href="/blog" class="brand-wrapper blog w-inline-block">'
    '<img width="300" height="33" src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/62bce0bf30fd51571af2d5e3_confidenceweekly2.svg" loading="lazy" alt="" class="image-123"/>'
    '</a>'
    '<nav role="navigation" class="nav-menu-2 blog w-nav-menu">'
    '<a href="/" class="nav-link-dark home">HOME</a>'
    '<div data-hover="false" data-delay="0" class="nav-dropdown blog w-dropdown">'
    '<div class="nav-dropdown-toggle w-dropdown-toggle">'
    '<div class="nav-link-dark w-icon-dropdown-toggle"></div>'
    '<div class="nav-link-dark">Treatments</div>'
    '</div>'
    '<nav class="nav-dropdown-list w-dropdown-list">'
    '<div class="nav-dropdown-wrapper-2 _2">'
    '<a href="/plastic-surgery" class="nav-link-dark dropdown">Cosmetic Surgery</a>'
    '<a href="/injectables" class="nav-link-dark dropdown">Injectables</a>'
    '<a href="/lasers-and-skin" class="nav-link-dark dropdown">Laser &amp; Skin</a>'
    '<a href="/body-contouring" class="nav-link-dark dropdown">Body Contouring</a>'
    '<a href="#" class="nav-link-dark dropdown">Permanent Makeup</a>'
    '<a href="/facials" class="nav-link-dark dropdown">Facials</a>'
    '</div></nav></div>'
    '<div data-hover="false" data-delay="0" class="nav-dropdown blog w-dropdown">'
    '<div class="nav-dropdown-toggle w-dropdown-toggle">'
    '<div class="nav-link-dark arrow w-icon-dropdown-toggle"></div>'
    '<div class="nav-link-dark arrow">About</div>'
    '</div>'
    '<nav class="nav-dropdown-list _2 w-dropdown-list">'
    '<div class="nav-dropdown-wrapper-2 _2">'
    '<a href="/about" class="nav-link-dark dropdown">About Us</a>'
    '<a href="/locations" class="nav-link-dark dropdown">Locations</a>'
    '<a href="/reginald-rice-md" class="nav-link-dark dropdown">Dr. Rice</a>'
    '</div></nav></div>'
    '<a href="/before-afters" class="nav-link-dark">Before &amp; Afters</a>'
    '<a href="/blog" class="nav-link-dark">Blog</a>'
    '<a href="/contact" class="nav-link-dark">Contact</a>'
    '</nav>'
    '<div class="menu-button-2 w-nav-button"></div>'
    '</div></div>'
)

EMAIL_OPTIN_HTML = (
    '<div class="div-block-196"><div class="downloadsectionwrapper">'
    '<div class="text-block-20">'
    '<span class="text-span-14">(FREE EBOOK)</span> '
    '5 THINGS YOU SHOULDN\'T COMPROMISE WHEN CHOOSING A COSMETIC SURGEON AND MEDICAL SPA'
    '</div>'
    '<div id="email-opt-in" class="form-block-3 w-form">'
    '<form id="wf-form-Email-Opt-In" name="wf-form-Email-Opt-In" data-name="Email Opt In" method="get" class="form-3">'
    '<input class="text-field-3 name w-input" maxlength="256" name="name" placeholder="name" type="text" id="name-4" required=""/>'
    '<input class="text-field-3 w-input" maxlength="256" name="Email-7" placeholder="email" type="email" id="Email-7" required=""/>'
    '<input type="submit" data-wait="Please wait..." class="submit-button w-button" value="Download"/>'
    '</form>'
    '<div class="error-message w-form-done"><div>Thank you! Your submission has been received!</div></div>'
    '<div class="error-message w-form-fail"><div>Oops! Something went wrong while submitting the form.</div></div>'
    '</div></div></div>'
)

FOOTER_HTML = (
    '<div class="footer"><div class="w-layout-grid grid">'
    '<div class="div-block-2">'
    '<a href="#" class="link-block w-inline-block">'
    '<img src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/61ce73519eba124498149ca4_TEC_type_white.svg" width="300" height="30" alt="Footer Logo" class="image"/>'
    '</a>'
    '<div class="w-layout-grid grid-2">'
    '<a href="https://www.facebook.com/estheticscenter" target="_blank" class="social-link w-inline-block">'
    '<img src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/61ce73519eba1279c8149b16_1Asset%204esthetics-05.svg" width="35" height="35" alt="Facebook"/>'
    '</a>'
    '<a href="https://www.instagram.com/estheticscenter/" target="_blank" class="social-link w-inline-block">'
    '<img src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/61ce73519eba1239ce149b12_1Asset%204esthetics-01.svg" width="35" height="35" alt="Instagram"/>'
    '</a>'
    '<a href="https://twitter.com/estheticsedh" target="_blank" class="social-link w-inline-block">'
    '<img src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/61ce73519eba12df4e149af5_1Asset%204esthetics-04.svg" width="35" height="35" alt="Twitter"/>'
    '</a>'
    '<a href="https://www.youtube.com/channel/UCaZHnGo1ZGQZyjr7Y-kf9Lg" target="_blank" class="social-link w-inline-block">'
    '<img src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/61ce73519eba125362149b00_1Asset%204esthetics-03.svg" width="35" height="35" alt="Youtube"/>'
    '</a>'
    '<a href="https://www.tiktok.com/@estheticscenter" target="_blank" class="social-link w-inline-block">'
    '<img src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/61ce73519eba120405149af9_1Asset%204esthetics-02.svg" width="35" height="35" alt="Tiktok"/>'
    '</a>'
    '</div></div>'
    '<div class="footer-div services">'
    '<div class="footer-heading">Services</div>'
    '<a href="/plastic-surgery" class="footer-links">Cosmetic Surgery</a>'
    '<a href="/med-spa-treatments" class="footer-links">MEDICAL SPA</a>'
    '<a href="/facials" class="footer-links">FACIALS</a>'
    '</div>'
    '<div class="footer-div about">'
    '<div class="footer-heading">About</div>'
    '<a href="/about" class="footer-links">overview</a>'
    '<a href="/reginald-rice-md" class="footer-links">Dr. rice</a>'
    '<a href="/testimonials" class="footer-links">REvieWS</a>'
    '</div>'
    '<div class="footer-div learn-more">'
    '<div class="footer-heading">Learn More</div>'
    '<a href="/before-afters" class="footer-links">RESULTS</a>'
    '<a href="/blog" class="footer-links">blog</a>'
    '<a href="/contact" class="footer-links">contact</a>'
    '<a href="/accessibility-statement" class="footer-links">accessibility statement</a>'
    '</div>'
    '</div>'
    '<div><div class="text-block-126 foot">ALPHA AESTHETICS PARTNERS</div></div>'
    '</div>'
)


def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def convert_inline(text):
    """Convert inline markdown (bold, italic, links) to HTML. Escapes special chars first."""
    # Escape HTML special characters
    result = escape_html(text)
    # Bold: **text**
    result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
    # Italic: *text* (not preceded/followed by *)
    result = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', result)
    # Links: [text](url) — unescape &amp; in URLs only
    def fix_link(m):
        link_text = m.group(1)
        url = m.group(2).replace('&amp;', '&')
        return f'<a href="{escape_html(url)}">{link_text}</a>'
    result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', fix_link, result)
    return result


def parse_table(lines):
    """Convert markdown table lines to an HTML table."""
    html = ['<table>']
    in_head = True
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        # Separator row (e.g. |---|---|)
        if re.match(r'^\|[\s\-:|]+\|$', line):
            if in_head:
                html.append('</thead><tbody>')
                in_head = False
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if in_head:
            html.append('<thead><tr>' + ''.join(f'<th>{convert_inline(c)}</th>' for c in cells) + '</tr>')
        else:
            html.append('<tr>' + ''.join(f'<td>{convert_inline(c)}</td>' for c in cells) + '</tr>')
    if in_head:
        html.append('</thead><tbody>')
    html.append('</tbody></table>')
    return '\n'.join(html)


def convert_body(markdown):
    """Convert a markdown body string to HTML, block by block."""
    # Normalize line endings
    markdown = markdown.replace('\r\n', '\n')

    # Split into blocks by one or more blank lines
    blocks = re.split(r'\n{2,}', markdown.strip())
    html_parts = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Horizontal rule — skip
        if re.match(r'^-{3,}$', block):
            continue

        # H1 — skip (used as page title separately)
        if re.match(r'^# (?!#)', block):
            continue

        # H2
        if re.match(r'^## (?!#)', block):
            text = block[3:].strip()
            html_parts.append(f'<h2>{convert_inline(text)}</h2>')
            continue

        # H3
        if re.match(r'^### (?!#)', block):
            text = block[4:].strip()
            html_parts.append(f'<h3>{convert_inline(text)}</h3>')
            continue

        lines = block.split('\n')

        # Table block (all lines start with |)
        if all(l.strip().startswith('|') or not l.strip() for l in lines) and any(l.strip().startswith('|') for l in lines):
            html_parts.append(parse_table(lines))
            continue

        # Detect if block is purely a list
        non_empty = [l for l in lines if l.strip()]
        is_ul = all(re.match(r'^[-*]\s', l) for l in non_empty)
        is_ol = all(re.match(r'^\d+\.\s', l) for l in non_empty)

        if is_ul and non_empty:
            items = []
            for line in non_empty:
                m = re.match(r'^[-*]\s(.+)', line)
                if m:
                    items.append(f'<li>{convert_inline(m.group(1))}</li>')
            html_parts.append('<ul role="list">' + ''.join(items) + '</ul>')
            continue

        if is_ol and non_empty:
            items = []
            for line in non_empty:
                m = re.match(r'^\d+\.\s(.+)', line)
                if m:
                    items.append(f'<li>{convert_inline(m.group(1))}</li>')
            html_parts.append('<ol role="list" start="">' + ''.join(items) + '</ol>')
            continue

        # Mixed block: may contain paragraph text + list items interspersed
        # (e.g., a label line followed by list items in the same block)
        has_list = any(re.match(r'^[-*]\s', l) or re.match(r'^\d+\.\s', l) for l in non_empty)

        if has_list:
            current_para = []
            current_list = []
            current_list_type = None

            def flush_para():
                if current_para:
                    text = ' '.join(current_para)
                    html_parts.append(f'<p>{convert_inline(text)}</p>')
                    current_para.clear()

            def flush_list():
                if current_list:
                    tag = current_list_type or 'ul'
                    attr = ' start=""' if tag == 'ol' else ' role="list"'
                    html_parts.append(f'<{tag}{attr}>' + ''.join(current_list) + f'</{tag}>')
                    current_list.clear()

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                ul_m = re.match(r'^[-*]\s(.+)', stripped)
                ol_m = re.match(r'^\d+\.\s(.+)', stripped)
                if ul_m:
                    if current_list_type == 'ol':
                        flush_list()
                    flush_para()
                    current_list_type = 'ul'
                    current_list.append(f'<li>{convert_inline(ul_m.group(1))}</li>')
                elif ol_m:
                    if current_list_type == 'ul':
                        flush_list()
                    flush_para()
                    current_list_type = 'ol'
                    current_list.append(f'<li>{convert_inline(ol_m.group(1))}</li>')
                else:
                    flush_list()
                    current_list_type = None
                    current_para.append(stripped)

            flush_para()
            flush_list()
            continue

        # Regular paragraph — join lines with a space
        text = ' '.join(l.strip() for l in lines if l.strip())
        if text:
            html_parts.append(f'<p>{convert_inline(text)}</p>')

    return '\n'.join(html_parts)


def parse_brief(filepath):
    """Extract meta title tag and description from a brief file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Title tag: first numbered option under ### Title Tags
    title_match = re.search(r'### Title Tags.*?\n1\.\s+(.+?)(?:\s+\(\d+\))?(?:\n|$)', content, re.DOTALL)
    meta_title = title_match.group(1).strip() if title_match else ''

    # Meta description: prefer *Final option 1:* or first numbered option
    final_match = re.search(r'\*Final option 1:\*\s+(.+?)(?:\s+\(\d+[^)]*\))?(?:\n|$)', content)
    if not final_match:
        final_match = re.search(r'### Meta Descriptions.*?\n1\.\s+(.+?)(?:\s+\(\d+\))?(?:\n|$)', content, re.DOTALL)
    meta_desc = final_match.group(1).strip() if final_match else ''

    return meta_title, meta_desc


def parse_draft(filepath):
    """Extract H1 title and body from a draft markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    title = ''
    body_start = 0

    for i, line in enumerate(lines):
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            body_start = i + 1
            break

    body = '\n'.join(lines[body_start:])
    return title, body


def build_html(meta_title, meta_desc, h1_title, body_html, hero_image):
    """Assemble the full Webflow-styled HTML page."""
    safe_meta_title = escape_html(meta_title)
    safe_meta_desc = escape_html(meta_desc)
    safe_h1 = escape_html(h1_title)
    safe_hero = escape_html(hero_image)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{safe_meta_title}</title>
<meta content="{safe_meta_desc}" name="description"/>
<meta content="{safe_meta_title}" property="og:title"/>
<meta content="{safe_meta_desc}" property="og:description"/>
<meta content="{safe_meta_title}" name="twitter:title"/>
<meta content="{safe_meta_desc}" name="twitter:description"/>
<meta property="og:type" content="website"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<link href="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/css/esthetics-center-ee8d2c50-27a53de946547.shared.3ac4fdb24.min.css" rel="stylesheet" type="text/css" crossorigin="anonymous"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link href="https://fonts.gstatic.com" rel="preconnect" crossorigin="anonymous"/>
<script src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js" type="text/javascript"></script>
<script type="text/javascript">WebFont.load({{google:{{families:["Noto Sans:300,400,500,600,700"]}}}});</script>
<script src="https://use.typekit.net/djd6twt.js" type="text/javascript"></script>
<script type="text/javascript">try{{Typekit.load();}}catch(e){{}}</script>
<link href="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/61ce73519eba1246a1149d4f_TEC_icon_white_FAVICO2.jpg" rel="shortcut icon" type="image/x-icon"/>
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" crossorigin="anonymous">
<style>
body {{ overflow-x: hidden; }}
.header-circular-image {{ display: none; }}
</style>
</head>
<body>
{NAV_HTML}
<div>
  <div style="background-image:url(&quot;{safe_hero}&quot;)" class="blog-header">
    <div class="div-block-207">
      <h1 class="heading-102">{safe_h1}</h1>
    </div>
    <div class="title-image-gradient blog"></div>
  </div>
  <div class="div-block-345">
    <div class="div-block-346">
      <div class="div-block-347">
        <div class="div-block-208">
          <div class="rich-text-block-11 w-richtext">
{body_html}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
{EMAIL_OPTIN_HTML}
{FOOTER_HTML}
<script src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=61ce73519eba1266c3149acc" type="text/javascript" crossorigin="anonymous"></script>
<script src="https://cdn.prod.website-files.com/61ce73519eba1266c3149acc/js/esthetics-center-ee8d2c50-27a53de946547.schunk.f2efb3c5440a81cf.js" type="text/javascript" crossorigin="anonymous"></script>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    draft_files = sorted(f for f in os.listdir(DRAFTS_DIR) if f.endswith('.md'))

    for draft_file in draft_files:
        slug = os.path.splitext(draft_file)[0]
        draft_path = os.path.join(DRAFTS_DIR, draft_file)
        brief_path = os.path.join(BRIEFS_DIR, draft_file)

        if not os.path.exists(brief_path):
            print(f"  [WARN] No brief found for {draft_file}, skipping meta")
            meta_title, meta_desc = '', ''
        else:
            meta_title, meta_desc = parse_brief(brief_path)

        h1_title, body_md = parse_draft(draft_path)
        if not meta_title:
            meta_title = h1_title

        body_html = convert_body(body_md)
        full_html = build_html(meta_title, meta_desc, h1_title, body_html, HERO_IMAGE)

        out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"  [OK] {slug}.html — title: {h1_title[:60]}")

    print(f"\nDone. {len(draft_files)} files written to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
