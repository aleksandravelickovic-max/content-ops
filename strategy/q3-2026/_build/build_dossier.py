#!/usr/bin/env python3
"""Build strategy-full.html (single-file navigable dossier) from the 16 Q3-2026 deliverables.

Reads the .md / .csv files in the parent directory verbatim, converts markdown and CSV to
HTML, and assembles one self-contained file with a sidebar + hash routing. Re-run after
editing any source file, then re-publish the artifact.

Usage:  python3 _build/build_dossier.py   (run from strategy/q3-2026/ or anywhere)
"""
import csv, html, re, os

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(SRC, "strategy-full.html")

ENTRIES = [
    ("home","README.md","Overview","Start","md"),
    ("s01","01-executive-summary.md","01 · Executive Summary","Start","md"),
    ("s02","02-data-sources-and-methodology.md","02 · Data &amp; Methodology","Start","md"),
    ("s03","03-content-inventory.csv","03 · Content Inventory","Evidence","csv"),
    ("s04","04-gsc-performance-analysis.md","04 · GSC Performance","Evidence","md"),
    ("s05","05-content-decay-and-quick-wins.csv","05 · Decay &amp; Quick Wins","Evidence","csv"),
    ("s06","06-cannibalization-map.csv","06 · Cannibalization Map","Evidence","csv"),
    ("s07","07-topic-cluster-and-gap-analysis.md","07 · Clusters &amp; Gaps","Evidence","md"),
    ("s08","08-2026-trends-research.md","08 · 2026 Trends","Evidence","md"),
    ("s09","09-competitor-serp-analysis.csv","09 · Competitor SERP","Evidence","csv"),
    ("s10","10-opportunity-scorecard.csv","10 · Opportunity Scorecard","Decisions","csv"),
    ("s11","11-q3-content-portfolio.md","11 · Content Portfolio","Decisions","md"),
    ("s12","12-q3-editorial-calendar.csv","12 · Editorial Calendar","Decisions","csv"),
    ("s13","13-top-10-content-briefs.md","13 · Top-10 Briefs","Decisions","md"),
    ("s14","14-internal-linking-plan.csv","14 · Internal Linking","Decisions","csv"),
    ("s15","15-measurement-framework.md","15 · Measurement","Decisions","md"),
]

def inline(t):
    t = html.escape(t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t

def is_table_sep(line):
    s = line.strip()
    return bool(re.match(r'^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?$', s))

def split_row(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    return [c.strip() for c in s.split('|')]

def md_to_html(md):
    lines = md.split('\n'); out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]; s = line.strip()
        if '|' in line and i+1 < n and is_table_sep(lines[i+1]):
            head = split_row(line); i += 2; body = []
            while i < n and '|' in lines[i] and lines[i].strip():
                body.append(split_row(lines[i])); i += 1
            t = ['<div class="scroll"><table><thead><tr>'] + [f'<th>{inline(c)}</th>' for c in head] + ['</tr></thead><tbody>']
            for row in body:
                t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in row) + '</tr>')
            t.append('</tbody></table></div>'); out.append(''.join(t)); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            lvl = len(m.group(1)); out.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>'); i += 1; continue
        if s == '---': out.append('<hr>'); i += 1; continue
        if s.startswith('>'):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append('<blockquote>' + ''.join(f'<p>{inline(x)}</p>' for x in buf if x) + '</blockquote>'); continue
        if re.match(r'^[-*]\s+', s):
            items = []
            while i < n and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append(re.sub(r'^\s*[-*]\s+', '', lines[i])); i += 1
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'); continue
        if re.match(r'^\d+\.\s+', s):
            items = []
            while i < n and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append(re.sub(r'^\s*\d+\.\s+', '', lines[i])); i += 1
            out.append('<ol>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ol>'); continue
        if not s: i += 1; continue
        buf = []
        while i < n and lines[i].strip() and not re.match(r'^(#{1,6}\s|[-*]\s|\d+\.\s|>)', lines[i].strip()) \
              and not ('|' in lines[i] and i+1 < n and is_table_sep(lines[i+1])) and lines[i].strip() != '---':
            buf.append(lines[i].strip()); i += 1
        out.append('<p>' + inline(' '.join(buf)) + '</p>')
    return '\n'.join(out)

def csv_to_html(path):
    with open(path, newline='') as fh: rows = list(csv.reader(fh))
    head, body = rows[0], rows[1:]
    t = ['<div class="scroll"><table class="data"><thead><tr>'] + [f'<th>{html.escape(c)}</th>' for c in head] + ['</tr></thead><tbody>']
    for r in body:
        t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>')
    t.append('</tbody></table></div>')
    return f'<p class="meta-line">{len(body)} rows · {len(head)} columns · source <code>{os.path.basename(path)}</code></p>' + ''.join(t)

HERO = '''<div class="hero">
  <div class="eyebrow">Search Atlas · Content Strategy · searchatlas.com</div>
  <h1 class="herotitle">Q3 2026 Content Strategy <span>— the full dossier</span></h1>
  <p class="herothesis"><b>Consolidate &amp; route, don't scale wider.</b> The site is past its peak; the Q3 win is to fix snippets, consolidate duplicates, and build one real AI-Search cluster on content Search Atlas already ranks for.</p>
  <div class="herometa">
    <span><b>Window</b> Jul 1 – Sep 30 2026</span><span><b>Data</b> live Google Search Console</span>
    <span><b>Prepared</b> 2026-06-25</span><span><b>Capacity</b> Aggressive (confirmed)</span>
  </div>
  <div class="herokpis">
    <div class="hk"><div class="hkl">Clicks 90d</div><div class="hkv">45,767</div><div class="hkd warn">+1.6% flat</div></div>
    <div class="hk"><div class="hkl">Impressions 90d</div><div class="hkv">17.2M</div><div class="hkd neg">−38%</div></div>
    <div class="hk"><div class="hkl">Avg position</div><div class="hkv">30.9</div><div class="hkd pos">↑ from 39.3</div></div>
    <div class="hk"><div class="hkl">Branded share</div><div class="hkv">~50%</div><div class="hkd warn">of all clicks</div></div>
    <div class="hk"><div class="hkl">H1-26 vs H2-25</div><div class="hkv">−33%</div><div class="hkd neg">decelerating</div></div>
  </div>
</div>'''

panes = []
for eid, fname, title, group, kind in ENTRIES:
    path = os.path.join(SRC, fname)
    content = csv_to_html(path) if kind == "csv" else md_to_html(open(path).read())
    hero = HERO if eid == "home" else ""
    panes.append(f'<section id="{eid}" class="pane" data-pane="{eid}">{hero}<div class="prose">{content}</div></section>')

groups_order, seen = [], set()
for e in ENTRIES:
    if e[3] not in seen: seen.add(e[3]); groups_order.append(e[3])
nav = []
for g in groups_order:
    nav.append(f'<div class="navgroup"><div class="navlabel">{g}</div>')
    for eid, fname, title, group, kind in ENTRIES:
        if group != g: continue
        tag = '<span class="kindtag">CSV</span>' if kind == 'csv' else ''
        nav.append(f'<a class="navlink" href="#{eid}" data-target="{eid}">{title}{tag}</a>')
    nav.append('</div>')
NAV = '\n'.join(nav)

CSS = r'''
:root{--paper:#F3F4F7;--surface:#FFFFFF;--band:#13151D;--band-soft:#1E212C;--ink:#14161D;--ink-soft:#3B4250;
--muted:#6A7280;--faint:#9AA1AD;--hairline:#E4E7EC;--hairline-band:#2C303C;--accent:#2A47D6;--accent-soft:#E9ECFB;
--pos:#14855E;--pos-soft:#E2F1EB;--neg:#C2382A;--neg-soft:#F8E7E4;--warn:#A9710F;--warn-soft:#F6EDDC;
--mono:ui-monospace,"SF Mono",SFMono-Regular,"Cascadia Mono","JetBrains Mono",Menlo,Consolas,monospace;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--side:288px}
*{box-sizing:border-box}body{margin:0}
.app{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.58;-webkit-font-smoothing:antialiased}
.tnum{font-variant-numeric:tabular-nums}
.side{position:fixed;top:0;left:0;width:var(--side);height:100vh;background:var(--band);color:#D7DAE3;overflow-y:auto;border-right:1px solid #000;padding:0 0 40px}
.brand{padding:22px 22px 18px;border-bottom:1px solid var(--hairline-band);position:sticky;top:0;background:var(--band);z-index:2}
.brand .eyebrow{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#7E86A0}
.brand .bt{font-size:16px;font-weight:680;color:#fff;margin-top:6px;letter-spacing:-.01em}
.brand .bs{font-family:var(--mono);font-size:11px;color:#8C93A4;margin-top:3px}
.navgroup{padding:14px 14px 4px}
.navlabel{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#717892;padding:0 8px 6px}
.navlink{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 10px;border-radius:7px;color:#C3C8D4;text-decoration:none;font-size:13.5px;line-height:1.3;margin:1px 0}
.navlink:hover{background:var(--band-soft);color:#fff}
.navlink.active{background:var(--accent);color:#fff;font-weight:550}
.navlink.active .kindtag{background:rgba(255,255,255,.22);color:#fff}
.kindtag{font-family:var(--mono);font-size:9px;letter-spacing:.06em;background:#2A2E3A;color:#8C93A4;padding:2px 5px;border-radius:4px;flex:none}
.main{margin-left:var(--side);min-height:100vh}
.topbar{position:sticky;top:0;z-index:3;background:rgba(243,244,247,.86);backdrop-filter:blur(8px);border-bottom:1px solid var(--hairline);padding:11px 32px;display:flex;align-items:center;gap:14px}
.topbar .crumb{font-family:var(--mono);font-size:12px;color:var(--muted)}
.topbar .crumb b{color:var(--ink)}.topbar .sp{flex:1}
.btn{font-family:var(--mono);font-size:11.5px;color:var(--ink-soft);background:var(--surface);border:1px solid var(--hairline);padding:6px 11px;border-radius:7px;cursor:pointer;text-decoration:none}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.menu-btn{display:none}
.content{max-width:1000px;margin:0 auto;padding:34px 32px 90px}
.pane{display:none;animation:rise .4s cubic-bezier(.2,.7,.3,1)}
.pane.active{display:block}
@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.hero{background:var(--band);color:#EEF0F5;border-radius:14px;padding:30px 30px 26px;margin-bottom:30px;border:1px solid var(--hairline-band)}
.hero .eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8C93A4}
.herotitle{font-size:clamp(24px,3vw,32px);font-weight:680;letter-spacing:-.02em;margin:10px 0 0;color:#fff}
.herotitle span{color:#8C93A4;font-weight:400}
.herothesis{max-width:70ch;color:#D7DAE3;margin:14px 0 0;font-size:16px}.herothesis b{color:#fff}
.herometa{display:flex;flex-wrap:wrap;gap:8px 24px;margin-top:16px;font-family:var(--mono);font-size:11.5px;color:#9AA1B2}
.herometa b{color:#D6DAE4;font-weight:500}
.herokpis{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:22px}
.hk{background:var(--band-soft);border:1px solid var(--hairline-band);border-radius:9px;padding:12px}
.hkl{font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;color:#8C93A4}
.hkv{font-family:var(--mono);font-size:22px;font-weight:600;color:#fff;margin:6px 0 4px}
.hkd{font-family:var(--mono);font-size:11px;font-weight:600}
.hkd.pos{color:#5FC79B}.hkd.neg{color:#E8897C}.hkd.warn{color:#E0B765}
.prose h1{font-size:26px;font-weight:700;letter-spacing:-.02em;margin:6px 0 14px;text-wrap:balance}
.prose h2{font-size:20px;font-weight:660;letter-spacing:-.01em;margin:30px 0 12px;padding-top:18px;border-top:1px solid var(--hairline);text-wrap:balance}
.prose h2:first-of-type{border-top:0;padding-top:0}
.prose h3{font-size:16px;font-weight:650;margin:22px 0 8px}
.prose h4{font-size:13px;font-weight:650;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:18px 0 6px}
.prose p{margin:11px 0;max-width:74ch}
.prose ul,.prose ol{margin:11px 0;padding-left:24px;max-width:74ch}.prose li{margin:5px 0}
.prose a{color:var(--accent);text-decoration:none;border-bottom:1px solid var(--accent-soft)}
.prose a:hover{border-bottom-color:var(--accent)}
.prose strong{font-weight:650;color:var(--ink)}
.prose code{font-family:var(--mono);font-size:.86em;background:var(--accent-soft);color:var(--accent);padding:1px 6px;border-radius:5px}
.prose hr{border:0;border-top:1px solid var(--hairline);margin:26px 0}
.prose blockquote{margin:16px 0;padding:12px 18px;background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:0 8px 8px 0}
.prose blockquote p{margin:4px 0;color:#6b5418;font-size:14px}
.meta-line{font-family:var(--mono);font-size:12px;color:var(--muted);margin:4px 0 14px}
.meta-line code{font-family:var(--mono);background:var(--accent-soft);color:var(--accent);padding:1px 5px;border-radius:4px}
.scroll{overflow-x:auto;border:1px solid var(--hairline);border-radius:10px;background:var(--surface);margin:14px 0}
table{border-collapse:collapse;width:100%;font-size:13px}
.prose table{min-width:520px}.prose table.data,table.data{min-width:720px}
thead th{font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-align:left;font-weight:600;padding:11px 13px;border-bottom:1px solid var(--hairline);white-space:nowrap;background:#FAFBFC;position:sticky;top:0}
tbody td{padding:10px 13px;border-bottom:1px solid var(--hairline);vertical-align:top;color:var(--ink-soft)}
tbody tr:last-child td{border-bottom:0}tbody tr:hover{background:#FAFBFC}
td code,th code{font-size:11.5px}
.data tbody td:first-child{color:var(--ink);font-weight:500}
.foot{margin-top:40px;padding-top:18px;border-top:1px solid var(--hairline);font-family:var(--mono);font-size:11.5px;color:var(--faint)}
@media print{.side{display:none}.main{margin:0}.topbar{display:none}.pane{display:block!important;page-break-after:always}.hero{break-inside:avoid}}
@media (prefers-reduced-motion:reduce){.pane{animation:none}}
@media (max-width:920px){:root{--side:0px}.side{transform:translateX(-100%);transition:transform .25s;width:280px;z-index:50}
.app.nav-open .side{transform:none}.app.nav-open::after{content:"";position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:40}
.menu-btn{display:inline-flex}.content{padding:24px 18px 80px}.herokpis{grid-template-columns:repeat(2,1fr)}}
'''

JS = r'''
const app=document.querySelector('.app');
const panes=[...document.querySelectorAll('.pane')];
const links=[...document.querySelectorAll('.navlink')];
const crumb=document.getElementById('crumb');
function show(id){
  if(!document.getElementById(id))id='home';
  panes.forEach(p=>p.classList.toggle('active',p.id===id));
  links.forEach(a=>a.classList.toggle('active',a.dataset.target===id));
  const active=links.find(a=>a.dataset.target===id);
  if(active)crumb.innerHTML='<b>'+active.textContent.replace('CSV','').trim()+'</b>';
  app.classList.remove('nav-open');window.scrollTo(0,0);
}
links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault();const id=a.dataset.target;history.pushState(null,'','#'+id);show(id);}));
window.addEventListener('hashchange',()=>show(location.hash.slice(1)||'home'));
document.getElementById('menuBtn').addEventListener('click',()=>app.classList.toggle('nav-open'));
show(location.hash.slice(1)||'home');
'''

DOC = f'''<title>Search Atlas — Q3 2026 Content Strategy (Full Dossier)</title>
<style>{CSS}</style>
<div class="app">
  <aside class="side">
    <div class="brand"><div class="eyebrow">Search Atlas</div><div class="bt">Q3 2026 Content Strategy</div><div class="bs">Full dossier · 16 deliverables</div></div>
    <nav>{NAV}</nav>
  </aside>
  <div class="main">
    <div class="topbar">
      <button class="btn menu-btn" id="menuBtn">☰ Menu</button>
      <div class="crumb" id="crumb"><b>Overview</b></div><div class="sp"></div>
      <button class="btn" onclick="window.print()">Print / PDF</button>
    </div>
    <div class="content">
      {''.join(panes)}
      <div class="foot">Search Atlas · Q3 2026 Content Strategy · prepared 2026-06-25 · every figure traces to a live GSC pull · facts, estimates, and inferences labeled throughout.</div>
    </div>
  </div>
</div>
<script>{JS}</script>'''

if __name__ == "__main__":
    with open(OUT, "w") as f:
        f.write(DOC)
    print("wrote", OUT, "·", len(DOC), "bytes ·", len(panes), "panes")
