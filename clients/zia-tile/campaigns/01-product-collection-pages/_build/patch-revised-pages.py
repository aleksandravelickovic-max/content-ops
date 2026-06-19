#!/usr/bin/env python3
"""
Patch 2 for revised/ product pages:
  1. Remove the .zt-faq section injected in the previous pass
  2. Make the product-details__details description text editable
  3. Add FAQ modal right after the Installation Guide modal
  4. Add FAQ toggle button right after the Installation Guide button
"""
import re
from pathlib import Path

REVISED_DIR = Path(__file__).parent / 'revised'

# ── 1. Remove .zt-faq section ───────────────────────────────────────────────
FAQ_SECTION_RE = re.compile(
    r'\n<section class="zt-faq">.*?</section>\n',
    re.DOTALL
)

# ── 2. Install Guide modal → inject FAQ modal right after it ────────────────
# The install modal ends with this exact sequence
INSTALL_MODAL_END = (
    '<div class="product-content-modal__content text-wrapper body body--regular"'
    ' contenteditable="true"><p>[KEEP]</p></div></div>\n</div>\n</div>'
)
FAQ_MODAL = (
    '<div class="product-content-modal__content text-wrapper body body--regular"'
    ' contenteditable="true"><p>[KEEP]</p></div></div>\n</div>\n'
    '<div class="product-content-modal product-content-modal--faq">\n'
    '<div class="product-content-modal__overlay faq-toggle"></div>\n'
    '<div class="product-content-modal__inner">'
    '<button class="product-content-modal__close faq-toggle body body--small body--regular">Close</button>\n'
    '<h2 class="product-content-modal__title label label--bold">Frequently Asked Questions</h2>\n'
    '<div class="product-content-modal__content text-wrapper body body--regular"'
    ' contenteditable="true"><p>[KEEP]</p></div></div>\n</div>\n</div>'
)

# ── 3. Installation Guide toggle → inject FAQ toggle right after ─────────────
INSTALL_BTN_SVG = (
    '<svg height="4.699" viewbox="0 0 7.984 4.699" width="7.984">\n'
    '<path d="m-1724.792-21856 3.639 3.639 3.639-3.639" fill="none" '
    'stroke="currentColor" transform="translate(1725.145 21856.354)"></path>\n'
    '</svg>'
)
INSTALL_BTN_END = (
    '<button class="product-details__toggle install-toggle body body--small-desktop body--bold">\n'
    '          Installation Guide\n'
    '          ' + INSTALL_BTN_SVG + '\n'
    '</button></div>'
)
WITH_FAQ_BTN = (
    '<button class="product-details__toggle install-toggle body body--small-desktop body--bold">\n'
    '          Installation Guide\n'
    '          ' + INSTALL_BTN_SVG + '\n'
    '</button>'
    '<button class="product-details__toggle faq-toggle body body--small-desktop body--bold">\n'
    '          Frequently Asked Questions\n'
    '          ' + INSTALL_BTN_SVG + '\n'
    '</button></div>'
)

# ── 4. Make product-details__details description editable ───────────────────
# Target the metafield-rich_text_field inside product-details__details
DETAILS_CE_RE = re.compile(
    r'(<div class="product-details__details">.*?'
    r'<div class="metafield-rich_text_field">)',
    re.DOTALL
)


def patch_product(content):
    # 1. Remove zt-faq section
    content = FAQ_SECTION_RE.sub('\n', content)

    # 2. Add FAQ modal after install modal
    if INSTALL_MODAL_END in content:
        content = content.replace(INSTALL_MODAL_END, FAQ_MODAL, 1)

    # 3. Add FAQ toggle button
    if INSTALL_BTN_END in content:
        content = content.replace(INSTALL_BTN_END, WITH_FAQ_BTN, 1)

    # 4. Make product-details__details text editable
    content = DETAILS_CE_RE.sub(
        lambda m: m.group(0).replace(
            '<div class="metafield-rich_text_field">',
            '<div class="metafield-rich_text_field" contenteditable="true">',
            1
        ),
        content,
        count=1
    )

    return content


def main():
    files = sorted(REVISED_DIR.glob('products--*.html'))
    done = 0
    skipped = 0

    for f in files:
        text = f.read_text(encoding='utf-8')

        # Skip if FAQ modal already added
        if 'product-content-modal--faq' in text:
            skipped += 1
            continue

        original = text
        text = patch_product(text)

        if text == original:
            print(f'  ~  {f.name}  (no changes matched)')
            skipped += 1
        else:
            f.write_text(text, encoding='utf-8')
            done += 1
            print(f'  ✓  {f.name}')

    print(f'\nDone: {done} patched, {skipped} unchanged.')


if __name__ == '__main__':
    main()
