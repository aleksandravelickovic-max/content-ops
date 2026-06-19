#!/usr/bin/env python3
"""
Make all revised/ HTML pages editable:
  - Injects edit-mode CSS + badge
  - Adds contenteditable to new copy sections
  - Injects FAQ accordion (after install guide in products, after FAQ accordion in collections)
"""
import re
from pathlib import Path

REVISED_DIR = Path(__file__).parent / 'revised'

# ── Injected CSS ────────────────────────────────────────────────────────────
EDIT_CSS = """
<style id="zt-edit-mode">
.zt-edit-badge {
  position: fixed;
  top: 48px;
  right: 16px;
  background: #8a3324;
  color: #fff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: 3px;
  z-index: 99999;
  pointer-events: none;
  user-select: none;
}
[contenteditable="true"] { cursor: text; transition: outline 0.1s; }
[contenteditable="true"]:hover  { outline: 2px dashed #c47a52 !important; outline-offset: 3px !important; }
[contenteditable="true"]:focus  { outline: 2px solid #8a3324 !important; outline-offset: 3px !important; }

/* FAQ accordion */
.zt-faq { max-width: 1200px; margin: 48px auto 64px; padding: 0 24px; }
.zt-faq__title {
  font-family: Georgia, serif;
  font-size: 26px;
  font-weight: 600;
  color: #1c1a17;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #d9cfb9;
}
.zt-ac-item {
  background: #fbf7ee;
  border: 1px solid #d9cfb9;
  margin-bottom: 8px;
  border-radius: 4px;
  overflow: hidden;
}
.zt-ac-trigger {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  user-select: none;
}
.zt-ac-trigger:hover { background: #f0ebe0; }
.zt-ac-q {
  flex: 1;
  font-family: Georgia, serif;
  font-size: 17px;
  font-weight: 600;
  color: #1c1a17;
  cursor: text;
  border-radius: 2px;
}
.zt-ac-q:hover { outline: 1px dashed #c47a52; outline-offset: 2px; }
.zt-ac-q:focus { outline: 2px solid #8a3324; outline-offset: 2px; }
.zt-ac-icon {
  font-size: 22px;
  font-weight: 300;
  color: #8a3324;
  flex-shrink: 0;
  line-height: 1;
  transition: transform 0.2s;
  pointer-events: none;
  user-select: none;
}
.zt-ac-item.open .zt-ac-icon { transform: rotate(45deg); }
.zt-ac-body {
  display: none;
  padding: 4px 20px 20px;
  border-top: 1px solid #d9cfb9;
}
.zt-ac-item.open .zt-ac-body { display: block; }
.zt-ac-body p {
  margin: 12px 0 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 15px;
  color: #444;
  line-height: 1.7;
}
</style>
"""

EDIT_BADGE = '<div class="zt-edit-badge">Edit mode</div>'

FAQ_BLOCK = """
<section class="zt-faq">
  <h2 class="zt-faq__title">FAQ</h2>

  <div class="zt-ac-item">
    <button class="zt-ac-trigger" onclick="ztAc(this)">
      <span class="zt-ac-q" contenteditable="true" onclick="event.stopPropagation()">Question</span>
      <span class="zt-ac-icon">+</span>
    </button>
    <div class="zt-ac-body"><p contenteditable="true">Answer</p></div>
  </div>

  <div class="zt-ac-item">
    <button class="zt-ac-trigger" onclick="ztAc(this)">
      <span class="zt-ac-q" contenteditable="true" onclick="event.stopPropagation()">Question</span>
      <span class="zt-ac-icon">+</span>
    </button>
    <div class="zt-ac-body"><p contenteditable="true">Answer</p></div>
  </div>

  <div class="zt-ac-item">
    <button class="zt-ac-trigger" onclick="ztAc(this)">
      <span class="zt-ac-q" contenteditable="true" onclick="event.stopPropagation()">Question</span>
      <span class="zt-ac-icon">+</span>
    </button>
    <div class="zt-ac-body"><p contenteditable="true">Answer</p></div>
  </div>

  <div class="zt-ac-item">
    <button class="zt-ac-trigger" onclick="ztAc(this)">
      <span class="zt-ac-q" contenteditable="true" onclick="event.stopPropagation()">Question</span>
      <span class="zt-ac-icon">+</span>
    </button>
    <div class="zt-ac-body"><p contenteditable="true">Answer</p></div>
  </div>

  <div class="zt-ac-item">
    <button class="zt-ac-trigger" onclick="ztAc(this)">
      <span class="zt-ac-q" contenteditable="true" onclick="event.stopPropagation()">Question</span>
      <span class="zt-ac-icon">+</span>
    </button>
    <div class="zt-ac-body"><p contenteditable="true">Answer</p></div>
  </div>

</section>
"""

ACCORDION_JS = """
<script id="zt-ac-js">
function ztAc(btn) { btn.parentElement.classList.toggle('open'); }
</script>
"""


def add_contenteditable(html, selector_class, attr_class):
    """Add contenteditable="true" to divs whose class contains attr_class,
    but only within a parent that contains selector_class."""
    # Simple string replacement — add contenteditable to matching divs
    return html.replace(
        f'<div class="{attr_class}">',
        f'<div class="{attr_class}" contenteditable="true">'
    )


def process_product(content):
    # 1. Edit CSS before </head>
    content = content.replace('</head>', EDIT_CSS + '</head>', 1)

    # 2. Edit badge inside <body>
    content = content.replace('<body>', f'<body>\n{EDIT_BADGE}', 1)

    # 3. Make product modal content areas editable
    #    Targets all product-content-modal__content divs (About, Order, Install)
    content = content.replace(
        'class="product-content-modal__content text-wrapper body body--regular"',
        'class="product-content-modal__content text-wrapper body body--regular" contenteditable="true"'
    )

    # 4. Make the product description (romance paragraph) in product-details editable
    #    Target the metafield-rich_text_field div inside product-details__content__cell
    content = re.sub(
        r'(class="product-details__content__cell">\s*<div[^>]*>)\s*(<div class="metafield-rich_text_field">)',
        lambda m: m.group(1) + '\n' + m.group(2).replace(
            '<div class="metafield-rich_text_field">',
            '<div class="metafield-rich_text_field" contenteditable="true">'
        ),
        content
    )

    # 5. Inject FAQ before the carousel CTA wrapper (after all modals end)
    content = content.replace(
        '<div class="product__carousel__cta-wrapper">',
        FAQ_BLOCK + '<div class="product__carousel__cta-wrapper">',
        1
    )

    # 6. Accordion JS before </body>
    content = content.replace('</body>', ACCORDION_JS + '</body>', 1)

    return content


def process_collection(content):
    # 1. Edit CSS before </head>
    content = content.replace('</head>', EDIT_CSS + '</head>', 1)

    # 2. Edit badge inside <body>
    content = content.replace('<body>', f'<body>\n{EDIT_BADGE}', 1)

    # 3. Make existing FAQ accordion answer divs editable (ac-text)
    content = re.sub(
        r'(<div )(aria-hidden="true" class="ac-text\b[^"]*"[^>]*>)',
        r'\1\2'.replace(r'\2', r'contenteditable="true" \2') if False else
        lambda m: m.group(1) + 'contenteditable="true" ' + m.group(2),
        content
    )

    # 4. Inject FAQ after the accordion_container </section>
    #    Pattern: find the section with id containing "accordion_container", then its </section>
    pattern = r'(<section[^>]+id="[^"]*accordion_container[^"]*"[^>]*>)(.*?)(</section>)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        insert_pos = match.end(3)
        content = content[:insert_pos] + FAQ_BLOCK + content[insert_pos:]
    else:
        # Fallback: inject before </main>
        content = content.replace('</main>', FAQ_BLOCK + '</main>', 1)

    # 5. Accordion JS before </body>
    content = content.replace('</body>', ACCORDION_JS + '</body>', 1)

    return content


def main():
    files = sorted(REVISED_DIR.glob('*.html'))
    done = 0
    skipped = 0

    for f in files:
        text = f.read_text(encoding='utf-8')

        if 'zt-edit-badge' in text:
            skipped += 1
            continue

        if f.name.startswith('products--'):
            text = process_product(text)
        elif f.name.startswith('collections--'):
            text = process_collection(text)
        else:
            continue

        f.write_text(text, encoding='utf-8')
        done += 1
        print(f'  ✓  {f.name}')

    print(f'\nDone: {done} files processed, {skipped} already done.')


if __name__ == '__main__':
    main()
