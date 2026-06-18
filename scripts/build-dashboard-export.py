#!/usr/bin/env python3
"""
build-dashboard-export.py

Builds a self-contained single-file HTML export of pillar-dashboard.html
with app.js, config-pillar.json, and data.json all inlined.

The export opens directly in any browser — no server needed.

Usage:
    python3 scripts/build-dashboard-export.py
    python3 scripts/build-dashboard-export.py --out dashboard/my-snapshot.html
"""

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DASHBOARD = REPO_ROOT / "dashboard"


def build(out_path: Path) -> None:
    html      = (DASHBOARD / "pillar-dashboard.html").read_text(encoding="utf-8")
    app_js    = (DASHBOARD / "app.js").read_text(encoding="utf-8")
    cfg_json  = json.dumps(json.loads((DASHBOARD / "config-pillar.json").read_text()), separators=(",", ":"))
    data_json = json.dumps(json.loads((DASHBOARD / "data.json").read_text()),          separators=(",", ":"))

    # Data vars at the TOP so they exist before any hoisted function runs.
    # Function overrides at the BOTTOM to win over app.js fetch-based versions.
    combined = f"""<script>
// ── Inlined data (standalone export) ────────────────────────────────
var __CFG__  = {cfg_json};
var __DATA__ = {data_json};

// ── app.js ───────────────────────────────────────────────────────────
{app_js}

// ── Standalone overrides ─────────────────────────────────────────────
async function loadData(){{
  CFG  = __CFG__;
  DATA = __DATA__;
  LIVE = buildLive();
}}
function scheduleNext(){{ /* disabled in standalone export */ }}
async function doRefresh(){{
  renderReport(LIVE);
  document.getElementById('countdown').textContent = 'Standalone export — data frozen at generation time';
}}
</script>"""

    banner = (
        '<div style="background:#f59e0b;color:#1c1c1e;font-size:11px;font-weight:700;'
        'text-align:center;padding:4px 0;letter-spacing:.06em">'
        "SNAPSHOT EXPORT — data frozen at generation time</div>"
    )

    result = html.replace('<script src="app.js"></script>', combined)
    container_div = '<div class="container">'
    result = result.replace(container_div, banner + "\n" + container_div, 1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result, encoding="utf-8")
    print(f"Export written → {out_path}  ({len(result):,} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build standalone dashboard export")
    parser.add_argument("--out", default=str(DASHBOARD / "pillar-dashboard-export.html"))
    args = parser.parse_args()
    build(Path(args.out))
