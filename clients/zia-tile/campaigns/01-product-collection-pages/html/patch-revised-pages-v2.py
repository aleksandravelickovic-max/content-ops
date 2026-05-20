#!/usr/bin/env python3
"""
Patch 3 for revised/ product pages:
  1. Fix Type B pages (21 files) — make description text in product-details__details editable
     (these pages use <div class="body...text-wrapper"> instead of metafield-rich_text_field)
  2. Fix FAQ toggle JS — inject event listener that opens/closes product-content-modal--faq
     when .faq-toggle elements are clicked
"""
import re
from pathlib import Path

REVISED_DIR = Path(__file__).parent / 'revised'

# ── 1. Type B description fix ─────────────────────────────────────────────────
# Targets the text-wrapper div inside product-details__details (Type B only)
TYPE_B_TEXT_WRAPPER = '<div class="body body--small-desktop body--regular text-wrapper">'
TYPE_B_TEXT_WRAPPER_CE = '<div class="body body--small-desktop body--regular text-wrapper" contenteditable="true">'

# Regex to confirm we're inside product-details__details before replacing
TYPE_B_RE = re.compile(
    r'(<div class="product-details__details">.*?)'
    r'(<div class="body body--small-desktop body--regular text-wrapper">)',
    re.DOTALL
)

# ── 2. FAQ toggle JS ──────────────────────────────────────────────────────────
OLD_AC_JS = (
    '<script id="zt-ac-js">\n'
    'function ztAc(btn) { btn.parentElement.classList.toggle(\'open\'); }\n'
    '</script>'
)

NEW_AC_JS = (
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

# ── 3. CSS for FAQ modal open state (appended to zt-edit-mode style) ──────────
# Ensures the modal is visible when .open is toggled, even if Shopify CSS doesn't cover --faq
OLD_EDIT_STYLE_CLOSE = '</style>'   # matches the first closing </style> after our zt-edit-mode block
# We inject within the zt-edit-mode style block
FAQ_MODAL_CSS = (
    '\n/* FAQ modal open state */\n'
    '.product-content-modal--faq.open { display: block; }\n'
)

EDIT_MODE_STYLE_END_RE = re.compile(
    r'(</style>\n)',  # just the first </style> after zt-edit-mode
)


def fix_type_b_editable(content):
    """Add contenteditable to the text-wrapper div inside product-details__details."""
    if 'product-details__content__cell' in content:
        return content  # Type A — skip

    if TYPE_B_TEXT_WRAPPER_CE in content:
        return content  # already patched

    def replacer(m):
        return m.group(1) + TYPE_B_TEXT_WRAPPER_CE

    result, count = TYPE_B_RE.subn(replacer, content, count=1)
    return result


def fix_faq_js(content):
    """Replace the zt-ac-js script with the extended version that handles faq-toggle."""
    if OLD_AC_JS in content:
        return content.replace(OLD_AC_JS, NEW_AC_JS, 1)
    return content


def fix_faq_modal_css(content):
    """Append FAQ modal open CSS to the zt-edit-mode style block."""
    if '.product-content-modal--faq.open' in content:
        return content  # already present

    # Insert before the closing </style> of the zt-edit-mode block
    target = '<style id="zt-edit-mode">'
    if target not in content:
        return content

    # Find the </style> that closes the zt-edit-mode block
    start = content.index(target)
    close_idx = content.index('</style>', start)
    return content[:close_idx] + FAQ_MODAL_CSS + content[close_idx:]


def patch_product(content):
    content = fix_type_b_editable(content)
    content = fix_faq_js(content)
    content = fix_faq_modal_css(content)
    return content


def main():
    files = sorted(REVISED_DIR.glob('products--*.html'))
    done = 0
    skipped = 0

    for f in files:
        text = f.read_text(encoding='utf-8')

        original = text
        text = patch_product(text)

        if text == original:
            print(f'  ~  {f.name}  (no changes)')
            skipped += 1
        else:
            f.write_text(text, encoding='utf-8')
            done += 1
            print(f'  ✓  {f.name}')

    print(f'\nDone: {done} patched, {skipped} unchanged.')


if __name__ == '__main__':
    main()
