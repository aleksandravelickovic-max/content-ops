#!/usr/bin/env python3
"""
Add a Status dropdown column to index-editable.html.
  - Inserts <th>Status</th> in both table headers
  - Inserts a <select> with In Progress / Updated / Approved in every data row
  - Adds CSS (color-coded states) and JS (localStorage persistence)
"""
import re
from pathlib import Path

FILE = Path(__file__).parent / 'index-editable.html'

# ── CSS ────────────────────────────────────────────────────────────────────────
STATUS_CSS = """
  /* ── Status dropdown ── */
  .status-select {
    appearance: none;
    -webkit-appearance: none;
    border: 1px solid var(--rule);
    border-radius: 4px;
    padding: 4px 26px 4px 10px;
    font-size: 12px;
    font-family: inherit;
    background-color: var(--paper);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%23aaa'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 8px center;
    cursor: pointer;
    min-width: 116px;
    color: #777;
  }
  .status-select:focus { outline: 2px solid var(--accent); border-color: var(--accent); }
  .status-select[data-status="in-progress"] { background-color: #fff8e1; border-color: #e6ac00; color: #7a5c00; }
  .status-select[data-status="updated"]     { background-color: #e8f4fd; border-color: #4a9edd; color: #1a5a8a; }
  .status-select[data-status="approved"]    { background-color: #e9f7ee; border-color: #4caf6e; color: #1f6b3a; }

"""

# ── JS ────────────────────────────────────────────────────────────────────────
STATUS_JS = """<script>
(function () {
  function applyStatus(sel) {
    sel.setAttribute('data-status', sel.value);
    if (sel.dataset.key) {
      localStorage.setItem('zt-status-' + sel.dataset.key, sel.value);
    }
  }
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.status-select').forEach(function (sel) {
      var saved = sel.dataset.key
        ? localStorage.getItem('zt-status-' + sel.dataset.key)
        : null;
      if (saved) sel.value = saved;
      applyStatus(sel);
      sel.addEventListener('change', function () { applyStatus(this); });
    });
  });
})();
</script>
"""

# ── Select HTML ───────────────────────────────────────────────────────────────
def status_td(key):
    return (
        '  <td><select class="status-select" data-key="' + key + '">'
        '<option value="">—</option>'
        '<option value="in-progress">In Progress</option>'
        '<option value="updated">Updated</option>'
        '<option value="approved">Approved</option>'
        '</select></td>\n'
    )


def add_status_to_row(m):
    row = m.group(0)
    # Only touch data rows (they contain <strong>)
    key_match = re.search(r'<strong>([^<]+)</strong>', row)
    if not key_match:
        return row
    raw_key = key_match.group(1)
    key = re.sub(r'[^a-z0-9]+', '-', raw_key.lower()).strip('-')
    # Insert status td before the closing </tr>
    return row[:-5] + status_td(key) + '</tr>'   # row[:-5] strips '</tr>'


def main():
    html = FILE.read_text(encoding='utf-8')

    if 'status-select' in html:
        print('Already patched — nothing to do.')
        return

    # 1. Inject CSS before closing </style>
    html = html.replace(
        '\n</style>\n</head>',
        STATUS_CSS + '</style>\n</head>',
        1
    )

    # 2. Inject JS before </body>
    html = html.replace('</body>', STATUS_JS + '</body>', 1)

    # 3. Add <th>Status</th> to both table headers
    html = html.replace(
        '<th>Original</th><th>Revised</th></tr></thead>',
        '<th>Original</th><th>Revised</th><th>Status</th></tr></thead>'
    )

    # 4. Add status <td> to every data row
    html = re.sub(r'<tr>.*?</tr>', add_status_to_row, html, flags=re.DOTALL)

    FILE.write_text(html, encoding='utf-8')
    print('Done — Status column added to index-editable.html')


if __name__ == '__main__':
    main()
