#!/usr/bin/env python3
"""
Patch 5 for revised/ product pages:
  The Shopify theme toggles the "active" class on modals — not "open".
  All previous patches used "open", so the FAQ modal never became visible.
  This patch replaces every "open" reference in the FAQ elements with "active".
"""
from pathlib import Path

REVISED_DIR = Path(__file__).parent / 'revised'

REPLACEMENTS = [
    # onclick on the toggle button
    (
        "onclick=\"document.querySelector('.product-content-modal--faq').classList.toggle('open')\"",
        "onclick=\"document.querySelector('.product-content-modal--faq').classList.toggle('active')\""
    ),
    # onclick on the overlay
    (
        "onclick=\"this.closest('.product-content-modal--faq').classList.remove('open')\"",
        "onclick=\"this.closest('.product-content-modal--faq').classList.remove('active')\""
    ),
    # CSS rule
    (
        '.product-content-modal--faq.open { display: block !important; }',
        '.product-content-modal--faq.active { display: block !important; }'
    ),
]


def patch_product(content):
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    return content


def main():
    files = sorted(REVISED_DIR.glob('products--*.html'))
    done = 0
    skipped = 0

    for f in files:
        text = f.read_text(encoding='utf-8')

        if ".classList.toggle('active')" in text and 'product-content-modal--faq' in text:
            skipped += 1
            continue

        original = text
        text = patch_product(text)

        if text == original:
            print(f'  !  {f.name}  (no match)')
            skipped += 1
        else:
            f.write_text(text, encoding='utf-8')
            done += 1
            print(f'  ✓  {f.name}')

    print(f'\nDone: {done} patched, {skipped} unchanged.')


if __name__ == '__main__':
    main()
