#!/usr/bin/env python3
"""
Patch 4 for revised/ product pages:
  Replace the faq-toggle class approach (broken) with inline onclick handlers
  that are completely independent of the Shopify theme JS.

  Changes:
  1. FAQ toggle button: remove faq-toggle class, add onclick that toggles .open
  2. FAQ modal overlay: remove faq-toggle class, add onclick that removes .open
  3. FAQ modal close btn: remove faq-toggle class, add onclick that removes .open
  4. CSS: add !important to .product-content-modal--faq.open rule
  5. JS: strip the unused event listener from zt-ac-js
"""
import re
from pathlib import Path

REVISED_DIR = Path(__file__).parent / 'revised'

# SVG shared across all toggle buttons
_SVG = (
    '<svg height="4.699" viewbox="0 0 7.984 4.699" width="7.984">\n'
    '<path d="m-1724.792-21856 3.639 3.639 3.639-3.639" fill="none" '
    'stroke="currentColor" transform="translate(1725.145 21856.354)"></path>\n'
    '</svg>'
)

# ── 1 & 2 & 3: Replace FAQ toggle button + modal ─────────────────────────────

OLD_FAQ_BTN = (
    '<button class="product-details__toggle faq-toggle body body--small-desktop body--bold">\n'
    '          Frequently Asked Questions\n'
    '          ' + _SVG + '\n'
    '</button></div>'
)
NEW_FAQ_BTN = (
    '<button class="product-details__toggle body body--small-desktop body--bold"'
    ' onclick="document.querySelector(\'.product-content-modal--faq\').classList.toggle(\'open\')">\n'
    '          Frequently Asked Questions\n'
    '          ' + _SVG + '\n'
    '</button></div>'
)

OLD_FAQ_MODAL = (
    '<div class="product-content-modal product-content-modal--faq">\n'
    '<div class="product-content-modal__overlay faq-toggle"></div>\n'
    '<div class="product-content-modal__inner">'
    '<button class="product-content-modal__close faq-toggle body body--small body--regular">Close</button>\n'
    '<h2 class="product-content-modal__title label label--bold">Frequently Asked Questions</h2>\n'
    '<div class="product-content-modal__content text-wrapper body body--regular"'
    ' contenteditable="true"><p>[KEEP]</p></div></div>\n'
    '</div>'
)
NEW_FAQ_MODAL = (
    '<div class="product-content-modal product-content-modal--faq">\n'
    '<div class="product-content-modal__overlay"'
    ' onclick="this.closest(\'.product-content-modal--faq\').classList.remove(\'open\')"></div>\n'
    '<div class="product-content-modal__inner">'
    '<button class="product-content-modal__close body body--small body--regular"'
    ' onclick="this.closest(\'.product-content-modal--faq\').classList.remove(\'open\')">Close</button>\n'
    '<h2 class="product-content-modal__title label label--bold">Frequently Asked Questions</h2>\n'
    '<div class="product-content-modal__content text-wrapper body body--regular"'
    ' contenteditable="true"><p>[KEEP]</p></div></div>\n'
    '</div>'
)

# ── 4: Upgrade CSS rule with !important ───────────────────────────────────────
OLD_FAQ_CSS = '.product-content-modal--faq.open { display: block; }'
NEW_FAQ_CSS = '.product-content-modal--faq.open { display: block !important; }'

# ── 5: Strip event listener from zt-ac-js ────────────────────────────────────
OLD_AC_JS = (
    '<script id="zt-ac-js">\n'
    'function ztAc(btn) { btn.parentElement.classList.toggle(\'open\'); }\n'
    'document.addEventListener(\'click\', function(e) {\n'
    '  var modal = document.querySelector(\'.product-content-modal--faq\');\n'
    '  if (!modal) return;\n'
    '  var t = e.target;\n'
    '  if (t.closest && t.closest(\'.product-details__toggle.faq-toggle\')) {\n'
    '    modal.classList.add(\'open\');\n'
    '  } else if (t.closest && t.closest(\'.product-content-modal--faq\') && t.classList.contains(\'faq-toggle\')) {\n'
    '    modal.classList.remove(\'open\');\n'
    '  }\n'
    '});\n'
    '</script>'
)
NEW_AC_JS = (
    '<script id="zt-ac-js">\n'
    'function ztAc(btn) { btn.parentElement.classList.toggle(\'open\'); }\n'
    '</script>'
)


def patch_product(content):
    content = content.replace(OLD_FAQ_BTN,   NEW_FAQ_BTN,   1)
    content = content.replace(OLD_FAQ_MODAL,  NEW_FAQ_MODAL,  1)
    content = content.replace(OLD_FAQ_CSS,    NEW_FAQ_CSS,    1)
    content = content.replace(OLD_AC_JS,      NEW_AC_JS,      1)
    return content


def main():
    files = sorted(REVISED_DIR.glob('products--*.html'))
    done = 0
    skipped = 0

    for f in files:
        text = f.read_text(encoding='utf-8')

        # Skip if already on the new onclick approach
        if 'onclick="document.querySelector' in text:
            skipped += 1
            print(f'  ~  {f.name}  (already patched)')
            continue

        original = text
        text = patch_product(text)

        if text == original:
            print(f'  !  {f.name}  (no match — check manually)')
            skipped += 1
        else:
            f.write_text(text, encoding='utf-8')
            done += 1
            print(f'  ✓  {f.name}')

    print(f'\nDone: {done} patched, {skipped} unchanged.')


if __name__ == '__main__':
    main()
