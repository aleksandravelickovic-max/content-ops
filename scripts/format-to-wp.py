#!/usr/bin/env python3
"""
format-to-wp.py — ClickUp "ready to format" → WordPress draft automation

Polls the SEO Content list in ClickUp for tasks with status "ready to format",
exports the linked Google Doc as HTML, creates a WordPress draft on the staging
site, then moves the task to "ready to publish".

Setup:
    cp scripts/.env.format-to-wp.example scripts/.env.format-to-wp
    # Fill in CLICKUP_API_KEY (from https://app.clickup.com/settings/apps)

Run manually:
    python3 scripts/format-to-wp.py
    python3 scripts/format-to-wp.py --dry-run   # preview only, no writes

Cron (every 30 min, logs to /tmp/format-to-wp.log):
    crontab -e
    */30 * * * * /usr/bin/python3 /Users/aleksandravelickovic/content-ops/scripts/format-to-wp.py >> /tmp/format-to-wp.log 2>&1

Exit codes:
    0  success (or nothing to do)
    1  config error
    2  one or more tasks failed (others may have succeeded — check output)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

# ── Config ─────────────────────────────────────────────────────────────────────

def _load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

_load_env(Path(__file__).parent / '.env.format-to-wp')

CLICKUP_API_KEY  = os.environ.get('CLICKUP_API_KEY', '')
WP_USERNAME      = os.environ.get('WP_USERNAME', 'aleksandra.velickovic@linkgraph.io')
WP_APP_PASSWORD  = os.environ.get('WP_APP_PASSWORD', '')

CLICKUP_LIST_ID  = '901111125948'       # Marketing → Content Writing Team → SEO Content
STATUS_TRIGGER   = 'ready to format'
STATUS_DONE      = 'ready to publish'
DRAFT_FIELD_NAME = '🪩 Draft URL'

WP_API_BASE      = 'https://stg.searchatlas.com/wp-json/wp/v2'

# ── HTML cleaning ──────────────────────────────────────────────────────────────

_KEEP_TAGS = {
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'ul', 'ol', 'li',
    'a', 'strong', 'em', 'b', 'i',
    'blockquote', 'table', 'thead', 'tbody', 'tr', 'td', 'th',
    'br', 'hr', 'code', 'pre',
}

def _gdoc_formatting_classes(soup: BeautifulSoup) -> tuple[set, set]:
    """Parse the Google Docs <style> block and return (bold_classes, italic_classes)."""
    bold, italic = set(), set()
    style_tag = soup.find('style')
    if not style_tag:
        return bold, italic
    for m in re.finditer(r'\.(c\d+)\s*\{([^}]+)\}', style_tag.get_text()):
        cls, rules = m.group(1), m.group(2)
        if 'font-weight:700' in rules:
            bold.add(cls)
        if 'font-style:italic' in rules:
            italic.add(cls)
    return bold, italic


def clean_gdoc_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, 'html.parser')
    bold_classes, italic_classes = _gdoc_formatting_classes(soup)
    body = soup.find('body') or soup

    for tag in body.find_all(['style', 'script']):
        tag.decompose()

    # Convert bold/italic spans to semantic tags before unwrapping
    for tag in body.find_all('span', class_=True):
        classes = set(tag.get('class', []))
        is_bold   = bool(classes & bold_classes)
        is_italic = bool(classes & italic_classes)
        if is_bold and is_italic:
            tag.name = 'strong'
            wrapper = soup.new_tag('em')
            tag.wrap(wrapper)
        elif is_bold:
            tag.name = 'strong'
        elif is_italic:
            tag.name = 'em'

    # Unwrap non-semantic wrappers (span, div, font…)
    for tag in reversed(body.find_all(True)):
        if tag.name not in _KEEP_TAGS:
            tag.unwrap()

    # Strip all attributes except href on <a>; unwrap Google redirect URLs
    for tag in body.find_all(True):
        if tag.name == 'a':
            href = tag.get('href', '')
            # Google Docs wraps all links in google.com/url?q=REAL_URL
            if 'google.com/url' in href:
                qs = parse_qs(urlparse(href).query)
                href = qs.get('q', [href])[0]
            tag.attrs = {'href': href} if href else {}
        else:
            tag.attrs = {}

    content = body.decode_contents()
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    return content.strip()

# ── ClickUp ────────────────────────────────────────────────────────────────────

def _cu_headers() -> dict:
    return {'Authorization': CLICKUP_API_KEY, 'Content-Type': 'application/json'}

def get_ready_tasks() -> list[dict]:
    r = requests.get(
        f'https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task',
        headers=_cu_headers(),
        params={'statuses[]': STATUS_TRIGGER, 'include_closed': 'false', 'page': 0},
        timeout=15,
    )
    r.raise_for_status()
    return r.json().get('tasks', [])

def get_draft_url(task: dict) -> str | None:
    for field in task.get('custom_fields', []):
        if field['name'] == DRAFT_FIELD_NAME:
            return field.get('value') or None
    return None

def set_task_status(task_id: str, status: str, dry_run: bool) -> None:
    if dry_run:
        print(f'    [dry-run] ClickUp status → {status}')
        return
    r = requests.put(
        f'https://api.clickup.com/api/v2/task/{task_id}',
        headers=_cu_headers(),
        json={'status': status},
        timeout=15,
    )
    r.raise_for_status()

# ── Google Docs ────────────────────────────────────────────────────────────────

def _doc_id(gdoc_url: str) -> str | None:
    m = re.search(r'/document/d/([a-zA-Z0-9_-]+)', gdoc_url)
    return m.group(1) if m else None

def fetch_gdoc_html(doc_id: str) -> str:
    r = requests.get(
        f'https://docs.google.com/document/d/{doc_id}/export?format=html',
        timeout=30,
        allow_redirects=True,
    )
    r.raise_for_status()
    if 'accounts.google.com' in r.url:
        raise ValueError('Google Doc requires login — check sharing is set to "anyone with link"')
    return r.text

# ── WordPress ──────────────────────────────────────────────────────────────────

def create_wp_draft(title: str, content: str, dry_run: bool) -> str:
    if dry_run:
        print(f'    [dry-run] would POST draft to {WP_API_BASE}/posts')
        return '(dry-run)'
    r = requests.post(
        f'{WP_API_BASE}/posts',
        json={'title': title, 'content': content, 'status': 'draft'},
        auth=(WP_USERNAME, WP_APP_PASSWORD),
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    return data.get('link') or data.get('guid', {}).get('rendered', str(data.get('id')))

# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true', help='Preview without making any changes.')
    args = parser.parse_args()

    missing = [k for k, v in [('CLICKUP_API_KEY', CLICKUP_API_KEY), ('WP_APP_PASSWORD', WP_APP_PASSWORD)] if not v]
    if missing:
        print(f'ERROR: {", ".join(missing)} not set. See scripts/.env.format-to-wp.example', file=sys.stderr)
        sys.exit(1)

    tasks = get_ready_tasks()
    if not tasks:
        print('Nothing to do.')
        return

    print(f'Found {len(tasks)} task(s){" (dry-run)" if args.dry_run else ""}.\n')
    errors = 0

    for task in tasks:
        task_id   = task['id']
        task_name = task['name']
        print(f'→ {task_name}')

        draft_url = get_draft_url(task)
        if not draft_url:
            print('  ⚠  No Draft URL — skipping\n')
            errors += 1
            continue

        doc_id = _doc_id(draft_url)
        if not doc_id:
            print(f'  ⚠  Cannot parse Google Doc ID from: {draft_url} — skipping\n')
            errors += 1
            continue

        try:
            raw_html = fetch_gdoc_html(doc_id)
            content  = clean_gdoc_html(raw_html)
            wp_url   = create_wp_draft(task_name, content, dry_run=args.dry_run)
            set_task_status(task_id, STATUS_DONE, dry_run=args.dry_run)
            print(f'  ✓  WP draft → {wp_url}')
            print(f'  ✓  ClickUp  → {STATUS_DONE}\n')
        except Exception as exc:
            print(f'  ✗  {exc}\n')
            errors += 1

    if errors:
        sys.exit(2)


if __name__ == '__main__':
    main()
