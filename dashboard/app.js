/* global localStorage, fetch */
let CFG=null, DATA=null, LIVE=null;
let nextAt=null;
const INTERVAL=5*60*1000;
const VKEY='ai_dash_versions_v2';
const CKEY='ai_dash_context_v2';

const fmtNum=n=>n==null?'—':Number(n).toLocaleString('en-US');
const fmtPts=n=>n==null?'—':Number(n).toLocaleString('en-US',{maximumFractionDigits:1});
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const abs=n=>Math.abs(n||0);
const parseD=s=>{ if(!s) return new Date(); const [y,m,d]=s.split('-').map(Number); return new Date(y,(m||1)-1,d||1); };
const longDate=ds=>parseD(ds).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});
const isoDate=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
const dirOf=n=>n==null?'flat':n>0?'up':n<0?'down':'flat';
const pctStr=n=>n==null?'':(n>0?'+':'')+n.toFixed(1)+'%';

function statusLabel(s){
  return ({completed:'Completed', in_progress:'In Progress', not_started:'Not Started', blocked:'Blocked'})[s] || s || '';
}
function statusTone(s){
  return ({completed:'good', in_progress:'warn', not_started:'neutral', blocked:'bad'})[s] || 'neutral';
}

/* ============================================================
   MAP fetched CFG/DATA -> LIVE render-shape (mirrors template's
   static CONFIG/METRICS/LEADING/ROCKS/AGENDA, but computed live)
   ============================================================ */
function buildLive(){
  const Q = (CFG[CFG.active_quarter] || CFG.q2 || {});
  const CP = Q.content_production || {};
  const gsc = DATA.gsc || {};
  const llmv = DATA.llm_visibility || {};
  const decay = DATA.content_decay || [];
  const wins = DATA.quick_wins || [];

  const bs = gsc.branded_split || {};
  const nbPct  = bs.current?.nonbranded_pct ?? null;
  const nbDelta = bs.nonbranded_ppt_change ?? null;
  const nbDeltaStr = nbDelta !== null ? (nbDelta >= 0 ? '+' : '') + nbDelta.toFixed(1) + ' pp' : null;

  const metrics = [
    { label:'Organic Clicks',    value: fmtNum(gsc.current?.clicks), delta: pctStr(gsc.change?.clicks_pct), dir: dirOf(gsc.change?.clicks_pct), ctx:'GSC · 28-day rolling · sc-domain:searchatlas.com' },
    { label:'Non-branded Share', value: nbPct !== null ? nbPct + '%' : '—', delta: nbDeltaStr, dir: dirOf(nbDelta), ctx:'GSC · branded = searchatlas|search atlas|linkgraph|otto seo|atlas agent|manick bhan' },
    { label:'LLM Visibility',    value: (llmv.overall_visibility??'—')+'%', delta: pctStr(llmv.visibility_change), dir: dirOf(llmv.visibility_change), ctx:'SearchAtlas LLMV · searchatlas.com' },
    { label:'Decaying Pages',    value: String(decay.length), delta:null, dir:'flat', ctx:'3-period click decline · GSC' },
  ];

  const rocks = (Q.rocks||[]).map(r=>({
    title:r.title, owner:r.owner||CFG.name, pct:(r.pct??0), tone:r.tone||statusTone(r.status),
    status:statusLabel(r.status), doc:r.link||'', notes:r.notes||'', due:r.due
  }));

  const agenda = (Q.agenda||[]).map(a=>({ t:a.topic, d:a.notes||'', type:a.type||'update' }));

  let leadingActual5 = null;
  const liGroups = (Q.leading_indicators||[]).map(g=>({
    group:g.group,
    items:(g.items||[]).map(it=>{
      let actual = it.actual;
      if((it.source||'').toLowerCase().includes('clickup') && (it.label||'').toLowerCase().includes('articles published')){
        const live = DATA?.clickup_stats?.articles_published_7d;
        if(live!=null) actual = live;
      }
      return { label:it.label, target:it.target, actual, unit:it.unit||'', note:it.note||'' };
    })
  }));

  return {
    asOf: (DATA.meta?.generated_at || new Date().toISOString()).slice(0,10),
    northStar: CFG.north_star || '',
    owner: CFG.name || '',
    quarterLabel: Q.label || '',
    quarterStart: Q.start, quarterEnd: Q.end,
    goal: CP.goal || 0,
    goalUnit: 'weighted pts',
    actual: (CP.final!=null ? CP.final : (CP.current!=null ? CP.current : 0)),
    thresholds: { exceeding:1.05, onTrack:0.92 },
    metrics, rocks, agenda, leadingGroups: liGroups,
    resp: CFG.ongoing_responsibilities || [],
    coaching: CFG.coaching || {read:'',work:[],risk:[],moves:[],close:''},
  };
}

/* ============================================================
   1 · NORTH STAR + dash title
   ============================================================ */
function renderNorthStar(s){
  document.getElementById('dashTitle').textContent = (s.owner||'') + ' — Content Pillar';
  document.getElementById('northStar').textContent = s.northStar;
  document.getElementById('ownerName').textContent = s.owner;
  document.getElementById('quarterLabel').textContent = s.quarterLabel;
  document.getElementById('asOfLabel').textContent = parseD(s.asOf).toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric'});
}

/* ============================================================
   2 · GOAL PACING
   ============================================================ */
function renderPacing(s){
  const goal=s.goal, actual=s.actual;
  const start=parseD(s.quarterStart), end=parseD(s.quarterEnd), now=parseD(s.asOf);
  const th=s.thresholds||{exceeding:1.05,onTrack:0.92};

  const totalDays=Math.max(1,(end-start)/86400000);
  const elapsedDays=Math.min(totalDays,Math.max(0,(now-start)/86400000));
  const elapsedFrac=elapsedDays/totalDays;
  const expected=goal*elapsedFrac;
  const ratio = expected>0 ? actual/expected : (actual>0?Infinity:1);

  let tone,label;
  if(ratio>=th.exceeding){tone='good';label='Exceeding';}
  else if(ratio>=th.onTrack){tone='good';label='On Track';}
  else if(ratio>=0.75){tone='warn';label='Slightly Behind';}
  else {tone='bad';label='Off Track';}

  document.getElementById('goalLbl').textContent = s.quarterLabel + ' Content Goal';
  document.getElementById('goalBig').textContent = fmtPts(goal)+' '+s.goalUnit;
  document.getElementById('actualInline').textContent = fmtPts(actual)+' '+s.goalUnit;

  const badge=document.getElementById('statusBadge');
  badge.className='status-badge '+tone;
  document.getElementById('statusText').textContent=label;

  const fill=document.getElementById('fill');
  fill.className='fill '+tone;
  fill.style.width=Math.min(100,(actual/goal)*100)+'%';

  const marker=document.getElementById('paceMarker');
  marker.style.left=Math.min(100,elapsedFrac*100)+'%';
  marker.setAttribute('data-label','Pace today '+Math.round(elapsedFrac*100)+'%');

  document.getElementById('scaleMid').textContent=fmtPts(goal/2);
  document.getElementById('scaleEnd').textContent=fmtPts(goal);

  const pct=elapsedFrac*100;
  let whereInQ;
  if(pct<12) whereInQ="We're just getting into the quarter";
  else if(pct<38) whereInQ="We're a few weeks into the quarter";
  else if(pct<46) whereInQ="We're about a third of the way through the quarter";
  else if(pct<58) whereInQ="We're halfway through the quarter";
  else if(pct<80) whereInQ="We're about three-quarters through the quarter";
  else whereInQ="We're in the final stretch of the quarter";

  const goalFmt=fmtPts(goal)+' '+s.goalUnit;
  let pacing;
  if(ratio>=1.20) pacing=`pacing well ahead of the ${goalFmt} goal`;
  else if(ratio>=th.exceeding) pacing='pacing comfortably ahead of schedule';
  else if(ratio>=th.onTrack) pacing='pacing just ahead of schedule';
  else if(ratio>=0.75) pacing='tracking a little behind pace';
  else pacing=`falling behind the ${goalFmt} goal`;

  document.getElementById('paceSummary').innerHTML =
    `${whereInQ} and we're <b>${pacing}</b> — ${fmtPts(actual)} produced of the ${goalFmt} target.`;
}

/* ============================================================
   3 · TOP METRICS
   ============================================================ */
function renderMetrics(s){
  document.getElementById('metrics').innerHTML = s.metrics.map(m=>`
    <div class="metric">
      <div class="label">${esc(m.label)}</div>
      <div class="value num">${esc(m.value)}</div>
      ${m.delta?`<div class="delta ${m.dir||'flat'}">${m.dir==='up'?'▲':m.dir==='down'?'▼':'–'} ${esc(m.delta)}</div>`:''}
      <div class="ctx">${esc(m.ctx||'')}</div>
    </div>`).join('');
}

/* ============================================================
   4 · ROCKS
   ============================================================ */
function dueLabel(ds){
  if(!ds) return '';
  const d=Math.floor((parseD(ds)-new Date())/86400000);
  if(d<0) return '<span style="color:var(--bad);font-weight:600">Overdue</span>';
  if(d===0) return '<span style="color:var(--warn);font-weight:600">Due today</span>';
  if(d<=7) return `<span style="color:var(--warn)">Due in ${d}d</span>`;
  return 'Due '+parseD(ds).toLocaleDateString('en-US',{month:'short',day:'numeric'});
}
function renderRocks(s){
  document.getElementById('rocksNote').textContent = s.rocks.length + ' priorities this quarter';
  document.getElementById('rocks').innerHTML = s.rocks.map((r,i)=>{
    const barColor = r.tone==='good'?'var(--good)':r.tone==='warn'?'var(--warn)':r.tone==='bad'?'var(--bad)':'var(--subtle)';
    return `<div class="rock">
      <div class="rk-head"><span class="rk-num">R${i+1}</span><h3 class="rk-title">${esc(r.title)}</h3></div>
      <div class="rk-owner">Owner · ${esc(r.owner)}${r.due?' · '+dueLabel(r.due):''}</div>
      ${r.notes?`<div class="rk-notes">${esc(r.notes)}</div>`:''}
      <div class="rk-bar"><i style="width:${r.pct}%;background:${barColor}"></i></div>
      <div class="rk-foot"><span class="pill ${r.tone}">${esc(r.status)}</span><span class="rk-pct num">${r.pct}%</span></div>
      ${r.doc?`<a class="rk-doc" href="${esc(r.doc)}" target="_blank" rel="noopener">View in ClickUp →</a>`:`<span class="rk-doc muted">No doc linked</span>`}
    </div>`;
  }).join('');
}

/* ============================================================
   5 · AGENDA
   ============================================================ */
function renderAgenda(s){
  const typeLabel={action_item:'Action',decision:'Decision',discussion:'Discussion',update:'Update'};
  document.getElementById('agenda').innerHTML = s.agenda.map(a=>`
    <li>
      <div class="ag-t">${esc(a.t)} <span class="ag-type t-${esc(a.type)}">${esc(typeLabel[a.type]||a.type)}</span></div>
      <div class="ag-d">${esc(a.d)}</div>
    </li>`).join('');
}

/* ============================================================
   6 · CLICKUP — 4-category native lists (no iframes; X-Frame-Options blocks them)
   ============================================================ */
function cuRow(t, metaFn){
  return `<div class="cu-row"><a class="ct-title" href="${esc(t.url)}" target="_blank" title="${esc(t.title)}">${esc(t.title)}</a><span class="ct-meta">${metaFn(t)}</span></div>`;
}
function renderClickUp(){
  const links = CFG?.clickup_links || {};
  document.getElementById('cuOwnerNote').textContent = 'Assigned to ' + (CFG.name||'');
  const CT = DATA?.clickup_tasks || {};
  const cats = [
    { key:'overdue', h:'Overdue', sw:'var(--bad)', metaFn:t=>(t.days_overdue>0?t.days_overdue+'d overdue':'due today'), empty:'No overdue tasks.' },
    { key:'no_due_date', h:'No Due Date', sw:'var(--warn)', metaFn:t=>esc(t.status), empty:'Everything has a due date.' },
    { key:'recently_completed', h:'Recently Completed', sw:'var(--good)', metaFn:t=>esc(t.closed), empty:'Nothing completed recently.' },
    { key:'assigned', h:'Assigned', sw:'var(--accent)', metaFn:t=>esc(t.due||''), empty:'Nothing currently assigned.' },
  ];
  document.getElementById('cuGrid').innerHTML = cats.map(c=>{
    const items = CT[c.key]||[];
    const show = items.slice(0,6);
    const rest = items.length-show.length;
    const inner = items.length
      ? `<div class="cu-list">${show.map(t=>cuRow(t,c.metaFn)).join('')}</div>${rest>0?`<div class="cu-more"><a href="${esc(links.seo_content_open||'#')}" target="_blank">+${rest} more in ClickUp</a></div>`:''}`
      : `<div class="cu-empty"><div class="ic">✓</div><div>${esc(c.empty)}</div></div>`;
    return `<div class="cu-card">
      <div class="cu-head"><span class="h"><span class="sw" style="background:${c.sw}"></span>${esc(c.h)}</span><span class="ct">${items.length}</span></div>
      ${inner}
    </div>`;
  }).join('');
}

/* ============================================================
   7 · RESPONSIBILITIES
   ============================================================ */
function renderResp(s){
  document.getElementById('resp').innerHTML = s.resp.map(r=>`
    <div class="resp"><span class="rb"></span><div><div class="rt">${esc(r.t)}</div><div class="rd">${esc(r.d||'')}</div></div></div>`).join('');
}

/* ============================================================
   3b · LEADING INDICATORS
   ============================================================ */
function renderLeading(s){
  document.getElementById('leading').innerHTML = s.leadingGroups.map(g=>`
    <div class="lead-card">
      <div class="lead-head"><h3>${esc(g.group)}</h3><span class="lead-sub">This week vs. weekly target</span></div>
      ${g.items.map(it=>{
        const r = it.target ? (it.actual||0)/it.target : 0;
        const col = r>=1 ? 'var(--good)' : r>=0.7 ? 'var(--warn)' : 'var(--bad)';
        const actualDisp = it.actual!=null ? it.actual : '—';
        return `<div class="lead-row">
          <div class="lr-top"><span class="lr-label">${esc(it.label)}</span><span class="lr-val"><b class="num">${esc(String(actualDisp))}</b> <span class="lr-tgt num">/ ${esc(String(it.target))}${esc(it.unit)}</span></span></div>
          <div class="lr-bar"><i style="width:${Math.min(100,r*100)}%;background:${col}"></i></div>
          ${it.note?`<div style="font-size:11px;color:var(--subtle);margin-top:6px">${esc(it.note)}</div>`:''}
        </div>`;
      }).join('')}
    </div>`).join('');
}

/* ============================================================
   EXTRA — LLM / AI VISIBILITY (not in template)
   ============================================================ */
function renderLLMV(){
  const L = DATA?.llm_visibility;
  const el = document.getElementById('llmvCard');
  if(!L){ el.innerHTML = '<div class="lead-card">No LLM visibility data.</div>'; return; }
  const v=L.overall_visibility||0, R=35, C=2*Math.PI*R, dash=(v/100)*C, gap=C-dash;
  const color = v>=40?'var(--good)':v>=20?'var(--warn)':'var(--bad)';
  const zero=(L.platforms||[]).filter(p=>p.visibility_score===0).map(p=>p.platform).join(', ');
  const rows=(L.platforms||[]).map(p=>{
    const col = p.visibility_score>=40?'var(--good)':p.visibility_score>=20?'var(--warn)':p.visibility_score>0?'var(--accent)':'var(--bad)';
    return `<div class="lead-row">
      <div class="lr-top"><span class="lr-label">${esc(p.platform)}</span><span class="lr-val"><b class="num">${p.visibility_score}%</b><span class="lr-tgt"> · 😊 ${p.sentiment_score}%</span></span></div>
      <div class="lr-bar"><i style="width:${p.visibility_score}%;background:${col}"></i></div>
    </div>`;
  }).join('');
  el.innerHTML = `<div class="lead-card">
    <div class="llmv-wrap">
      <div class="llmv-ring"><svg width="84" height="84" viewBox="0 0 84 84"><circle cx="42" cy="42" r="${R}" fill="none" stroke="#ecedf1" stroke-width="7"/><circle cx="42" cy="42" r="${R}" fill="none" stroke="${color}" stroke-width="7" stroke-dasharray="${dash.toFixed(1)} ${gap.toFixed(1)}" stroke-linecap="round"/></svg><div class="llmv-ring-num"><span class="v" style="color:${color}">${v}%</span><span class="l">visibility</span></div></div>
      <div class="llmv-stats">
        <div class="llmv-stat"><div class="v">${L.sentiment_score?.toFixed(0)}%</div><div class="l">Sentiment</div></div>
        <div class="llmv-stat"><div class="v">${fmtNum(L.total_mentions)}</div><div class="l">Mentions (was ${fmtNum(L.previous_mentions)})</div></div>
        <div class="llmv-stat"><div class="v">${(L.platforms||[]).filter(p=>p.visibility_score>0).length}/${(L.platforms||[]).length}</div><div class="l">Platforms active</div></div>
      </div>
      ${zero?`<div class="llmv-zero-flag"><b>0% visibility:</b> ${esc(zero)}</div>`:''}
    </div>
    ${rows}
  </div>`;
}

/* ============================================================
   EXTRA — CONTENT PERFORMANCE: top performers + climbing pages
   ============================================================ */
function renderPerformance(){
  const P = DATA?.content_performance;
  const el = document.getElementById('perfGrid');
  if(!P){ el.innerHTML=''; return; }
  const top=P.top_pages||[], climb=P.climbing||[];
  const topRows = top.map((r,i)=>`<tr><td>${i+1}</td><td><a href="${esc(r.page)}" target="_blank">${esc(r.slug)}</a></td><td class="tr" style="font-weight:600">${fmtNum(r.clicks)}</td><td class="tr">${r.ctr.toFixed(2)}%</td><td class="tr tm">${r.position.toFixed(1)}</td></tr>`).join('');
  const climbRows = climb.map((r,i)=>{
    const growthTxt = r.is_new ? 'New' : `+${r.growth_pct.toFixed(0)}%`;
    return `<tr><td>${i+1}</td><td><a href="${esc(r.page)}" target="_blank">${esc(r.slug)}</a></td><td class="tr tm" style="color:var(--subtle)">${r.clicks_prior} → <strong style="color:var(--text)">${r.clicks_now}</strong></td><td class="tr"><span class="pill good">▲ ${esc(growthTxt)}</span></td></tr>`;
  }).join('');
  el.innerHTML = `
    <div class="lead-card">
      <div class="lead-head"><h3>🏆 Top Performing Pages — 28d</h3><span class="lead-sub">${top.length} pages</span></div>
      <div class="table-wrap"><table class="dtable"><thead><tr><th>#</th><th>Page</th><th class="tr">Clicks</th><th class="tr">CTR</th><th class="tr">Pos</th></tr></thead><tbody>${topRows}</tbody></table></div>
    </div>
    <div class="lead-card">
      <div class="lead-head"><h3>📈 Climbing Pages — vs prior 28d</h3><span class="lead-sub">${climb.length} growing</span></div>
      <div class="table-wrap"><table class="dtable"><thead><tr><th>#</th><th>Page</th><th class="tr">Prior → Now</th><th class="tr">Growth</th></tr></thead><tbody>${climbRows||'<tr><td colspan="4" style="text-align:center;color:var(--subtle);padding:14px">No significant climbers.</td></tr>'}</tbody></table></div>
    </div>`;
}

/* ============================================================
   EXTRA — GSC DETAIL
   ============================================================ */
function renderGSC(){
  const G = DATA?.gsc;
  const el = document.getElementById('gscCard');
  if(!G){ el.innerHTML='<div class="lead-card">No GSC data.</div>'; return; }
  const c=G.current||{}, ch=G.change||{};
  const stats=[
    {lbl:'Clicks (28d)', val:fmtNum(c.clicks), delta:ch.clicks_pct, inv:false},
    {lbl:'Impressions', val:fmtNum(c.impressions), delta:ch.impressions_pct, inv:false},
    {lbl:'Avg CTR', val:(c.ctr||0)+'%', delta:null, sub:'was '+G.prior?.ctr+'%'},
    {lbl:'Avg Position', val:(c.position||0).toFixed(1), delta:ch.position_change, inv:true, sub:'was '+G.prior?.position?.toFixed(1)},
  ];
  const cards = stats.map(s=>{
    const dir = s.delta==null ? 'flat' : (s.inv ? (s.delta<0?'up':'down') : (s.delta>0?'up':'down'));
    return `<div class="metric sm"><div class="value num">${esc(String(s.val))}</div><div class="label" style="text-transform:none;letter-spacing:0;font-size:11px">${esc(s.lbl)}</div>${s.delta!=null?`<div class="delta ${dir}">${dir==='up'?'▲':'▼'} ${abs(s.delta).toFixed(1)}%</div>`:`<div class="ctx">${esc(s.sub||'')}</div>`}</div>`;
  }).join('');
  el.innerHTML = `<div class="grid-4">${cards}</div>
    <div class="lead-card" style="margin-top:14px;background:var(--accent-soft);border-color:#c7d6ff">
      <b>Insight:</b> Position improved ${abs(ch.position_change||0).toFixed(1)} pts (${G.prior?.position?.toFixed(1)} → ${c.position?.toFixed(1)}) but clicks dropped ${abs(ch.clicks_pct||0).toFixed(1)}%. CTR fell ${G.prior?.ctr}% → ${c.ctr}% — AI Mode likely displacing organic clicks.
    </div>`;
}

/* ============================================================
   EXTRA — CONTENT DECAY (with recommended action)
   ============================================================ */
function actionForTrend(t){
  if(!t) return '';
  if(t.includes('declining')) return 'Refresh content — rankings dropping';
  if(t.includes('stable')) return 'Rewrite title/meta — CTR is the gap';
  if(t.includes('improved')) return 'Target adjacent queries — demand shifted';
  return '';
}
function trendPill(t){
  if(!t) return '';
  if(t.includes('declining')) return '<span class="pill bad">Declining</span>';
  if(t.includes('stable')) return '<span class="pill warn">Demand ↓</span>';
  if(t.includes('improved')) return '<span class="pill neutral" style="color:var(--accent);background:var(--accent-soft)">Rank ↑</span>';
  return `<span class="pill neutral">${esc(t)}</span>`;
}
let decayRows=[], decayMax=1;
function renderDecay(){
  decayRows = DATA?.content_decay || [];
  decayMax = decayRows[0]?.loss || 1;
  document.getElementById('decayNote').textContent = decayRows.length+' pages · '+decayRows.reduce((s,r)=>s+(r.loss||0),0)+' clicks lost';
  const mk=(r,i)=>`<tr><td>${i+1}</td><td><a href="${esc(r.page)}" target="_blank">${esc(r.slug||r.page)}</a></td><td class="tr" style="color:var(--bad);font-weight:600">−${r.loss}</td><td>${trendPill(r.trend)}</td><td style="font-size:11.5px;color:var(--muted)">${esc(actionForTrend(r.trend))}</td><td class="tr tm">${r.position_now?.toFixed(1)}</td></tr>`;
  const show=decayRows.slice(0,6), rest=decayRows.slice(6);
  document.getElementById('decayTable').innerHTML = `<table class="dtable"><thead><tr><th>#</th><th>Page</th><th class="tr">Clicks Lost</th><th>Trend</th><th>Action</th><th class="tr">Pos</th></tr></thead><tbody id="decay-tb">${show.map(mk).join('')}${rest.length?`<tr class="more-row" onclick="expandDecay()"><td colspan="6">▾ Show ${rest.length} more</td></tr>`:''}</tbody></table>`;
}
function expandDecay(){
  const rest=decayRows.slice(6); const tb=document.getElementById('decay-tb'); const mr=tb.querySelector('.more-row');
  rest.forEach((r,i)=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${i+7}</td><td><a href="${esc(r.page)}" target="_blank">${esc(r.slug||r.page)}</a></td><td class="tr" style="color:var(--bad);font-weight:600">−${r.loss}</td><td>${trendPill(r.trend)}</td><td style="font-size:11.5px;color:var(--muted)">${esc(actionForTrend(r.trend))}</td><td class="tr tm">${r.position_now?.toFixed(1)}</td>`; tb.insertBefore(tr,mr); });
  mr.remove();
}

/* ============================================================
   EXTRA — QUICK WIN KEYWORDS
   ============================================================ */
let winsRows=[], winsMax=1;
function renderWins(){
  winsRows = DATA?.quick_wins || [];
  winsMax = winsRows[0]?.opportunity || 1;
  document.getElementById('winsNote').textContent = winsRows.length+' keywords · top opportunity: '+fmtNum(winsRows[0]?.opportunity||0)+' clicks';
  const mk=(r,i)=>`<tr><td>${i+1}</td><td style="font-weight:500">${esc(r.query)}</td><td class="tr tm">${r.position?.toFixed(1)}</td><td class="tr">${fmtNum(r.impressions)}</td><td class="tr">${r.clicks}</td><td class="tr" style="color:var(--subtle)">${(r.ctr*100).toFixed(2)}%</td><td><span class="mini-bar"><i style="width:${Math.min(100,r.opportunity/winsMax*100)}%;background:var(--good)"></i></span> <span style="font-size:11px;color:var(--subtle)">${fmtNum(r.opportunity)}</span></td></tr>`;
  const show=winsRows.slice(0,10), rest=winsRows.slice(10);
  document.getElementById('winsTable').innerHTML = `<table class="dtable"><thead><tr><th>#</th><th>Keyword</th><th class="tr">Position</th><th class="tr">Impressions</th><th class="tr">Clicks</th><th class="tr">CTR</th><th>Opportunity</th></tr></thead><tbody id="wins-tb">${show.map(mk).join('')}${rest.length?`<tr class="more-row" onclick="expandWins()"><td colspan="7">▾ Show ${rest.length} more</td></tr>`:''}</tbody></table>`;
}
function expandWins(){
  const rest=winsRows.slice(10); const tb=document.getElementById('wins-tb'); const mr=tb.querySelector('.more-row');
  rest.forEach((r,i)=>{ const tr=document.createElement('tr'); tr.innerHTML=`<td>${i+11}</td><td style="font-weight:500">${esc(r.query)}</td><td class="tr tm">${r.position?.toFixed(1)}</td><td class="tr">${fmtNum(r.impressions)}</td><td class="tr">${r.clicks}</td><td class="tr" style="color:var(--subtle)">${(r.ctr*100).toFixed(2)}%</td><td><span class="mini-bar"><i style="width:${Math.min(100,r.opportunity/winsMax*100)}%;background:var(--good)"></i></span> <span style="font-size:11px;color:var(--subtle)">${fmtNum(r.opportunity)}</span></td>`; tb.insertBefore(tr,mr); });
  mr.remove();
}

/* ============================================================
   WEEKLY METRICS SCORECARD
   ============================================================ */
function renderWeeklyMetrics(){
  const wm = CFG?.[CFG.active_quarter]?.weekly_metrics;
  const el = document.getElementById('weeklyTable');
  const noteEl = document.getElementById('weeklyNote');
  if(!el) return;
  if(!wm || !wm.weeks || !wm.rows || !wm.rows.length){
    el.innerHTML = '<p style="color:var(--subtle);font-size:13px;padding:8px 0">Add <code>weekly_metrics</code> to config-pillar.json to enable this table.</p>';
    return;
  }

  const weeks = wm.weeks;
  const rows = wm.rows;

  // Update note
  const filled = rows.reduce((s,r)=>{
    const v=r.values||[]; return s+v.filter(x=>x!==null&&x!==undefined&&x!=='').length;
  },0);
  const total = rows.length * weeks.length;
  if(noteEl) noteEl.textContent = `${weeks.length} weeks · ${filled}/${total} cells filled`;

  // Group separator labels
  const GROUP_LABELS = { traffic:'Traffic', pipeline:'Pipeline', llm:'LLM', branded:'Branded Split' };
  let lastGroup = null;
  let bodyHtml = '';
  for(const r of rows){
    if(r.group && r.group !== lastGroup){
      lastGroup = r.group;
      const lbl = GROUP_LABELS[r.group] || r.group;
      bodyHtml += `<tr class="wm-group-label"><td class="wm-metric" style="font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--subtle);font-weight:700;background:var(--surface-alt)" colspan="${1+weeks.length}">${lbl}</td></tr>`;
    }
    const cells = (r.values || []).map((v,i)=>{
      if(v === null || v === undefined || v === '') return `<td class="wm-null">—</td>`;
      const fmt = typeof v === 'number' && v >= 1000 ? fmtNum(v) : (typeof v === 'number' ? String(v) : esc(String(v)));
      return `<td>${fmt}</td>`;
    });
    // pad if fewer values than weeks
    while(cells.length < weeks.length) cells.push('<td class="wm-null">—</td>');
    bodyHtml += `<tr class="wm-group-${r.group||''}"><td class="wm-metric">${esc(r.metric)}</td>${cells.join('')}</tr>`;
  }

  el.innerHTML = `<div class="wm-wrap"><table class="wm-table">
    <thead><tr>
      <th style="text-align:left;min-width:160px">Metric</th>
      ${weeks.map(w=>`<th class="wm-week-head">${esc(w)}</th>`).join('')}
    </tr></thead>
    <tbody>${bodyHtml}</tbody>
  </table></div>`;
}

/* ============================================================
   8 · AI CAREER COACHING
   ============================================================ */
function renderCoaching(s){
  const C = s.coaching || {};
  const has = C.read || (C.work&&C.work.length) || (C.risk&&C.risk.length) || (C.moves&&C.moves.length) || C.close;
  const el = document.getElementById('coachSection');
  if(!has){
    el.innerHTML = `<p class="c-eyebrow">✧ AI Career Coaching</p>
      <h2>${esc(s.owner)} — Content Pillar</h2>
      <p class="c-sub">Acting-CMO read. Blunt on purpose.</p>
      <div class="coach-empty">Sophia fills this in before each 1:1. Add under <code style="color:#cdd6e6">coaching</code> in config-pillar.json.</div>`;
    return;
  }
  el.innerHTML = `
    <p class="c-eyebrow">✧ AI Career Coaching</p>
    <h2>${esc(s.owner)} — Content Pillar</h2>
    <p class="c-sub">Acting-CMO read. Blunt on purpose.</p>
    ${C.read?`<p class="c-read">${esc(C.read)}</p>`:''}
    <div class="c-grid">
      <div class="c-block work"><h3>What's working</h3><ul>${(C.work||[]).map(x=>`<li>${esc(x)}</li>`).join('')||'<li>—</li>'}</ul></div>
      <div class="c-block risk"><h3>The problems</h3><ul>${(C.risk||[]).map(x=>`<li>${esc(x)}</li>`).join('')||'<li>—</li>'}</ul></div>
    </div>
    ${(C.moves&&C.moves.length)?`<div class="c-block moves"><h3>Do this week</h3><ul>${C.moves.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>`:''}
    ${C.close?`<p class="c-close">${esc(C.close)}</p>`:''}`;
}

/* ============================================================
   RENDER ORCHESTRATION
   ============================================================ */
function renderReport(s){
  renderNorthStar(s);
  renderPacing(s);
  renderMetrics(s);
  renderRocks(s);
  renderAgenda(s);
  renderClickUp();
  renderResp(s);
  renderLeading(s);
  renderLLMV();
  renderPerformance();
  renderGSC();
  renderDecay();
  renderWins();
  renderWeeklyMetrics();
  renderCoaching(s);
  document.getElementById('footLeft').textContent = 'Search Atlas · Content Pillar · 1:1 with ' + (CFG?.one_on_one_with||'Sophia Deluz-Bhan');
  document.getElementById('freshness').textContent = 'Data as of ' + parseD(s.asOf).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});
}

/* ============================================================
   VERSION ARCHIVE (date drop-down)
   ============================================================ */
const clone=o=>JSON.parse(JSON.stringify(o));
function versionsLoad(){ try{ const v=JSON.parse(localStorage.getItem(VKEY)); return v&&typeof v==='object'?v:{}; }catch(e){ return {}; } }
function versionsSave(m){ try{ localStorage.setItem(VKEY, JSON.stringify(m)); }catch(e){} }

function initVersions(){
  let versions = versionsLoad();
  versions[LIVE.asOf] = clone(LIVE);
  versionsSave(versions);

  const sel=document.getElementById('verSelect');
  const badge=document.getElementById('verBadge');
  const banner=document.getElementById('verBanner');

  function refreshOptions(){
    versions = versionsLoad();
    const dates = Object.keys(versions).sort((a,b)=>b.localeCompare(a));
    sel.innerHTML = dates.map(d=>`<option value="${d}">${longDate(d)}${d===LIVE.asOf?' — current':''}</option>`).join('');
  }
  function show(dateStr){
    const v = versionsLoad();
    const s = v[dateStr];
    if(!s) return;
    renderReport(s);
    const isCurrent = dateStr===LIVE.asOf;
    badge.textContent = isCurrent?'Live':'Archived';
    badge.className = 'ver-badge '+(isCurrent?'live':'arch');
    if(isCurrent){ banner.hidden=true; }
    else{
      banner.hidden=false;
      banner.innerHTML = `Viewing the archived version from <b>${longDate(dateStr)}</b> — read-only snapshot. <a href="#" id="verBack">Back to current →</a>`;
      document.getElementById('verBack').addEventListener('click', e=>{ e.preventDefault(); sel.value=LIVE.asOf; show(LIVE.asOf); });
    }
    sel.value = dateStr;
  }
  refreshOptions();
  show(LIVE.asOf);
  sel.addEventListener('change', ()=>show(sel.value));

  document.getElementById('verSave').addEventListener('click', e=>{
    const v=versionsLoad(); v[LIVE.asOf]=clone(LIVE); versionsSave(v);
    refreshOptions(); show(LIVE.asOf);
    const b=e.target, o=b.textContent; b.textContent='Saved ✓'; setTimeout(()=>b.textContent=o,1400);
  });
  document.getElementById('verReset').addEventListener('click', ()=>{
    if(confirm("Clear all saved report versions from this browser?")){ localStorage.removeItem(VKEY); location.reload(); }
  });
}

/* ============================================================
   LOAD + AUTO-REFRESH
   ============================================================ */
async function loadData(){
  const [cr,dr] = await Promise.all([fetch('config-pillar.json?t='+Date.now()), fetch('data.json?t='+Date.now())]);
  CFG = await cr.json();
  DATA = await dr.json();
  LIVE = buildLive();
}
function scheduleNext(){
  nextAt = Date.now()+INTERVAL;
  clearInterval(window._ri); clearInterval(window._ci);
  window._ri = setInterval(doRefresh, INTERVAL);
  window._ci = setInterval(()=>{
    const r=Math.max(0,nextAt-Date.now()); const m=Math.floor(r/60000), sec=Math.floor((r%60000)/1000);
    document.getElementById('countdown').textContent = `Refreshes in ${m}:${String(sec).padStart(2,'0')}`;
  },1000);
}
async function doRefresh(){
  const btn=document.getElementById('btnRefresh'); const orig=btn.textContent; btn.textContent='⟳ Refreshing…';
  try{
    await loadData();
    const versions=versionsLoad(); versions[LIVE.asOf]=clone(LIVE); versionsSave(versions);
    renderReport(LIVE);
    document.getElementById('verBadge').textContent='Live'; document.getElementById('verBadge').className='ver-badge live';
    document.getElementById('verBanner').hidden=true;
    const sel=document.getElementById('verSelect');
    const dates=Object.keys(versions).sort((a,b)=>b.localeCompare(a));
    sel.innerHTML = dates.map(d=>`<option value="${d}">${longDate(d)}${d===LIVE.asOf?' — current':''}</option>`).join('');
    sel.value=LIVE.asOf;
  } finally { btn.textContent=orig; scheduleNext(); }
}

async function init(){
  try{
    await loadData();
    initVersions();
    scheduleNext();
    window.dispatchEvent(new Event('ctx-cfg-ready'));
  }catch(e){
    document.getElementById('tab-dashboard').innerHTML = `<div class="lead-card" style="max-width:420px;margin:60px auto;text-align:center"><div style="color:var(--bad);font-weight:700;margin-bottom:6px">Failed to load</div><div style="font-size:12px;color:var(--muted)">${esc(e.message)}</div><div style="font-size:11px;color:var(--subtle);margin-top:8px">Serve with: <code>python3 -m http.server 8080</code></div></div>`;
  }
}
document.getElementById('btnRefresh').addEventListener('click', doRefresh);

/* ============================================================
   TABS
   ============================================================ */
document.querySelectorAll('.tabbar button').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.tabbar button').forEach(b=>b.setAttribute('aria-selected', String(b===btn)));
    document.querySelectorAll('.tab-panel').forEach(p=>p.classList.toggle('active', p.id==='tab-'+btn.dataset.tab));
    window.scrollTo(0,0);
  });
});

/* ============================================================
   CONTEXT FOR AI (editable, saved in browser)
   ============================================================ */
(function contextStore(){
  const load=()=>{ try{ const v=JSON.parse(localStorage.getItem(CKEY)); return Array.isArray(v)?v:null; }catch(e){ return null; } };
  const save=a=>{ try{ localStorage.setItem(CKEY, JSON.stringify(a)); }catch(e){} };
  let truths=null;

  const listEl=document.getElementById('ctxList');
  const inputEl=document.getElementById('ctxInput');

  function ensureLoaded(){ if(truths===null){ const stored=load(); truths = stored!==null ? stored : (CFG?.context_truths ? CFG.context_truths.slice() : []); } }
  function render(){
    ensureLoaded();
    if(!truths.length){ listEl.innerHTML = `<div class="ctx-empty">No statements yet. Add the first truth below.</div>`; return; }
    listEl.innerHTML = truths.map((t,i)=>`<div class="ctx-item"><span class="ci-dot">✓</span><div class="ci-text">${esc(t)}</div><button class="ci-del" data-i="${i}" title="Remove">×</button></div>`).join('');
    listEl.querySelectorAll('.ci-del').forEach(b=>b.addEventListener('click', ()=>{ truths.splice(+b.dataset.i,1); save(truths); render(); }));
  }
  function add(){ const v=inputEl.value.trim(); if(!v) return; ensureLoaded(); truths.push(v); save(truths); inputEl.value=''; render(); inputEl.focus(); }
  document.getElementById('ctxAdd').addEventListener('click', add);
  inputEl.addEventListener('keydown', e=>{ if(e.key==='Enter') add(); });
  document.getElementById('ctxCopy').addEventListener('click', e=>{
    ensureLoaded();
    navigator.clipboard?.writeText(truths.map(t=>'- '+t).join('\n'));
    const b=e.target, orig=b.textContent; b.textContent='Copied ✓'; setTimeout(()=>b.textContent=orig,1400);
  });
  window.addEventListener('ctx-cfg-ready', ()=>{ truths=null; render(); });
  render();
})();

init();
