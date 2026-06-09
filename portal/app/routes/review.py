"""Client-facing review routes. No auth required — the UUID token IS the auth."""

import html as _html
import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import ShareLink, Comment
from .. import content as content_svc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/review/{token}", response_class=HTMLResponse)
async def campaign_review(
    request: Request,
    token: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="This review link is not active or does not exist.")

    link.last_accessed_at = datetime.now(timezone.utc)
    link.access_count += 1
    await db.commit()

    registry = content_svc.load_registry(link.client_slug, link.campaign_slug)
    if not registry:
        raise HTTPException(status_code=404, detail="Campaign content not found.")

    # Group entries by type
    groups: dict[str, list] = {}
    for entry in registry.get("entries", []):
        t = entry.get("type", "other")
        groups.setdefault(t, []).append(entry)

    # Count comments per content path (total and unresolved)
    comment_counts_q = await db.execute(
        select(Comment.content_path, func.count(Comment.id))
        .where(Comment.share_link_token == token, Comment.parent_id.is_(None))
        .group_by(Comment.content_path)
    )
    comment_counts = dict(comment_counts_q.all())

    unresolved_counts_q = await db.execute(
        select(Comment.content_path, func.count(Comment.id))
        .where(
            Comment.share_link_token == token,
            Comment.parent_id.is_(None),
            Comment.resolved.is_(False),
        )
        .group_by(Comment.content_path)
    )
    unresolved_counts = dict(unresolved_counts_q.all())

    type_labels = {
        "product-page": "Product Pages",
        "collection-page": "Collection Pages",
        "draft": "Drafts",
        "draft-v3": "V3 Revisions",
        "brief": "Briefs",
        "audit": "Audit Reports",
        "campaign-urls": "URL Maps",
        "blog": "Blog Posts",
        "html-revised": "Revised HTML",
        "html-original": "Original HTML",
        "html-index": "HTML Index",
        "other": "Other",
    }

    tab_order = [
        "product-page", "collection-page", "draft", "draft-v3",
        "html-revised", "html-original",
        "brief", "audit", "campaign-urls", "blog", "html-index", "other",
    ]
    ordered_tabs = []
    for t in tab_order:
        if t in groups:
            ordered_tabs.append({
                "key": t,
                "label": type_labels.get(t, t.replace("-", " ").title()),
                "count": len(groups[t]),
            })
    for t in groups:
        if t not in tab_order:
            ordered_tabs.append({
                "key": t,
                "label": type_labels.get(t, t.replace("-", " ").title()),
                "count": len(groups[t]),
            })

    compare_pairs = content_svc.get_compare_pairs(registry)

    return templates.TemplateResponse(request, "review/campaign.html", {
        "link": link,
        "registry": registry,
        "groups": groups,
        "tabs": ordered_tabs,
        "type_labels": type_labels,
        "comment_counts": comment_counts,
        "unresolved_counts": unresolved_counts,
        "compare_pairs": compare_pairs,
        "token": str(token),
    })


@router.get("/review/{token}/raw/{content_path:path}", response_class=HTMLResponse)
async def raw_html(
    request: Request,
    token: uuid.UUID,
    content_path: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404)

    html = content_svc.get_content_html(link.client_slug, link.campaign_slug, content_path)
    if html is None:
        raise HTTPException(status_code=404)
    return HTMLResponse(content=html)


@router.get("/review/{token}/compare/{filename:path}", response_class=HTMLResponse)
async def compare_view(
    request: Request,
    token: uuid.UUID,
    filename: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404)

    registry = content_svc.load_registry(link.client_slug, link.campaign_slug)
    if not registry:
        raise HTTPException(status_code=404)

    original_path = f"html/original/{filename}"
    revised_path = f"html/revised/{filename}"

    original_entry = next((e for e in registry.get("entries", []) if e["path"] == original_path), None)
    if not original_entry:
        raise HTTPException(status_code=404, detail="Original HTML not found.")

    has_revised = any(e["path"] == revised_path for e in registry.get("entries", []))

    pairs = content_svc.get_compare_pairs(registry)
    current_idx = next((i for i, p in enumerate(pairs) if p["filename"] == filename), 0)
    prev_pair = pairs[current_idx - 1] if current_idx > 0 else None
    next_pair = pairs[current_idx + 1] if current_idx < len(pairs) - 1 else None

    draft_info = content_svc.find_draft_for_html(
        link.client_slug, link.campaign_slug, filename
    )
    draft_html = draft_info["html"] if draft_info else None
    draft_path = draft_info["path"] if draft_info else None

    content_path = f"compare:{filename}"
    pin_count_q = await db.execute(
        select(func.count(Comment.id))
        .where(
            Comment.share_link_token == token,
            Comment.content_path == content_path,
            Comment.parent_id.is_(None),
        )
    )
    pin_comment_count = pin_count_q.scalar() or 0

    return templates.TemplateResponse(request, "review/compare.html", {
        "link": link,
        "token": str(token),
        "filename": filename,
        "display_name": filename.replace("--", " / ").replace(".html", "").replace("-", " ").title(),
        "original_path": original_path,
        "revised_path": revised_path if has_revised else None,
        "draft_html": draft_html,
        "draft_path": draft_path,
        "prev_pair": prev_pair,
        "next_pair": next_pair,
        "nav_position": f"{current_idx + 1} of {len(pairs)}",
        "pin_comment_count": pin_comment_count,
    })


@router.get("/review/{token}/{content_path:path}", response_class=HTMLResponse)
async def content_review(
    request: Request,
    token: uuid.UUID,
    content_path: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="This review link is not active or does not exist.")

    registry = content_svc.load_registry(link.client_slug, link.campaign_slug)
    if not registry:
        raise HTTPException(status_code=404, detail="Campaign content not found.")

    entry = next((e for e in registry.get("entries", []) if e["path"] == content_path), None)
    if not entry:
        raise HTTPException(status_code=404, detail="Content piece not found.")

    rendered_html = content_svc.get_content_html(link.client_slug, link.campaign_slug, content_path)
    if rendered_html is None:
        raise HTTPException(status_code=404, detail="Unable to read content file.")

    comments_q = await db.execute(
        select(Comment)
        .where(
            Comment.share_link_token == token,
            Comment.content_path == content_path,
            Comment.parent_id.is_(None),
        )
        .order_by(Comment.created_at.desc())
    )
    comments = comments_q.scalars().all()

    # Load replies for each comment
    comment_ids = [c.id for c in comments]
    replies_map: dict[int, list] = {cid: [] for cid in comment_ids}
    if comment_ids:
        replies_q = await db.execute(
            select(Comment)
            .where(Comment.parent_id.in_(comment_ids))
            .order_by(Comment.created_at.asc())
        )
        for reply in replies_q.scalars().all():
            replies_map.setdefault(reply.parent_id, []).append(reply)

    # Build navigation (prev/next content in same type)
    all_entries = registry.get("entries", [])
    same_type = [e for e in all_entries if e["type"] == entry["type"]]
    current_idx = next((i for i, e in enumerate(same_type) if e["path"] == content_path), 0)
    prev_entry = same_type[current_idx - 1] if current_idx > 0 else None
    next_entry = same_type[current_idx + 1] if current_idx < len(same_type) - 1 else None

    comments_json = json.dumps([
        {
            "id": c.id,
            "author_name": c.author_name,
            "body": c.body,
            "highlight_text": c.highlight_text,
            "anchor_prefix": c.anchor_prefix,
            "anchor_suffix": c.anchor_suffix,
            "anchor_start_offset": c.anchor_start_offset,
            "anchor_end_offset": c.anchor_end_offset,
            "anchor_heading": c.anchor_heading,
            "anchor_paragraph_index": c.anchor_paragraph_index,
            "resolved": c.resolved,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in comments
    ])

    return templates.TemplateResponse(request, "review/content.html", {
        "link": link,
        "entry": entry,
        "content_html": rendered_html,
        "comments": comments,
        "replies_map": replies_map,
        "comments_json": comments_json,
        "token": str(token),
        "content_path": content_path,
        "prev_entry": prev_entry,
        "next_entry": next_entry,
        "nav_position": f"{current_idx + 1} of {len(same_type)}",
        "reviewer_name": link.recipient_name or "",
    })


# ── Blog review: full-page HTML with annotation overlay injected ──────────────

def _build_blog_overlay(
    token: str,
    content_path: str,
    comments: list,
    replies_map: dict,
    comments_json_str: str,
    reviewer_name: str,
) -> str:
    """Build the annotation sidebar + JS to inject into the blog HTML page."""
    e = _html.escape
    back_url = f"/review/{token}"
    count = len(comments)

    def fmt_comment(c, is_reply: bool = False) -> str:
        hl = ""
        if c.highlight_text:
            text = c.highlight_text[:120] + ("…" if len(c.highlight_text) > 120 else "")
            hl = f'<blockquote class="portal-hl">&ldquo;{e(text)}&rdquo;</blockquote>'
        badge = '<span class="portal-resolved-badge">Resolved</span>' if c.resolved else ""
        cls = "portal-comment comment resolved" if c.resolved else "portal-comment comment"
        if is_reply:
            cls += " portal-reply"
        return (
            f'<div class="{cls}" data-id="{c.id}">'
            f'<div class="comment-header portal-ch">'
            f'<strong>{e(c.author_name)}</strong>'
            f'<time>{c.created_at.strftime("%b %d, %Y")}</time>'
            f"</div>{hl}"
            f'<div class="portal-body">{e(c.body)}</div>'
            f"{badge}</div>"
        )

    comments_html = ""
    for c in comments:
        comments_html += fmt_comment(c)
        for reply in replies_map.get(c.id, []):
            comments_html += fmt_comment(reply, is_reply=True)
        if not c.resolved:
            if reviewer_name:
                name_f = f'<input type="hidden" name="author_name" value="{e(reviewer_name)}">'
            else:
                name_f = '<input type="text" name="author_name" placeholder="Your name" required class="portal-input">'
            comments_html += (
                f'<button class="portal-reply-btn" onclick="togglePortalReply({c.id})">Reply</button>'
                f'<form class="portal-reply-form" id="prf-{c.id}" style="display:none">'
                f'<input type="hidden" name="parent_id" value="{c.id}">{name_f}'
                f'<textarea name="body" placeholder="Reply…" required class="portal-textarea" rows="2"></textarea>'
                f'<button type="submit" class="portal-btn portal-btn-sm">Reply</button>'
                f"</form>"
            )

    if not comments_html:
        comments_html = '<p class="portal-empty">No feedback yet.<br>Highlight any text to leave a comment.</p>'

    if reviewer_name:
        name_field = f'<input type="hidden" name="author_name" value="{e(reviewer_name)}">'
    else:
        name_field = '<input type="text" name="author_name" placeholder="Your name" required class="portal-input">'

    token_js = json.dumps(token)
    path_js = json.dumps(content_path)
    name_js = json.dumps(reviewer_name)

    return f"""
<!-- ── Content Review Portal overlay ── -->
<link rel="stylesheet" href="/static/annotation.css">
<style>
body {{ margin-right: 320px !important; box-sizing: border-box; }}
#portal-sidebar {{
  position: fixed; top: 0; right: 0;
  width: 320px; height: 100vh;
  background: #fff; border-left: 1px solid #e2e8f0;
  box-shadow: -4px 0 20px rgba(0,0,0,.07);
  z-index: 99999; display: flex; flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 14px; line-height: 1.5; overflow: hidden;
  transition: transform .25s ease;
}}
#portal-sidebar.collapsed {{ transform: translateX(296px); }}
#portal-sidebar.collapsed ~ * {{ margin-right: 24px !important; }}
#portal-top {{
  padding: 14px 16px 10px; border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0; background: #f8fafc;
}}
#portal-top a.back {{
  display: block; font-size: 12px; color: #64748b;
  text-decoration: none; margin-bottom: 8px;
}}
#portal-top a.back:hover {{ color: #1e293b; }}
#portal-title {{
  font-size: 14px; font-weight: 600; color: #1e293b;
  display: flex; align-items: center; justify-content: space-between;
}}
.portal-count {{
  background: #2563eb; color: #fff; border-radius: 9999px;
  font-size: 11px; font-weight: 600; padding: 1px 7px; margin-left: 6px;
}}
#portal-toggle {{
  background: none; border: 1px solid #e2e8f0; border-radius: 4px;
  cursor: pointer; padding: 2px 8px; font-size: 13px; color: #64748b;
}}
.portal-pill {{
  margin: 10px 16px 0; padding: 6px 12px;
  background: #fef9c3; color: #854d0e;
  border: 1px solid #fde68a; border-radius: 999px;
  font-size: 12px; font-weight: 500; flex-shrink: 0;
}}
#portal-scroll {{
  flex: 1; overflow-y: auto; padding: 12px 14px;
}}
.portal-comment {{
  padding: 10px 12px; border: 1px solid #e2e8f0;
  border-radius: 8px; margin-bottom: 8px; background: #fff;
}}
.portal-comment.resolved {{ opacity: .6; background: #f8fafc; }}
.portal-ch {{
  display: flex; justify-content: space-between;
  align-items: baseline; gap: 8px; margin-bottom: 5px;
}}
.portal-ch strong {{ font-size: 13px; color: #1e293b; }}
.portal-ch time {{ font-size: 11px; color: #94a3b8; white-space: nowrap; }}
.portal-hl {{
  margin: 5px 0; padding: 5px 8px;
  background: rgba(251,191,36,.15); border-left: 3px solid #f59e0b;
  border-radius: 0 4px 4px 0; font-size: 12px;
  color: #78350f; font-style: italic;
}}
.portal-body {{ font-size: 13px; color: #374151; }}
.portal-resolved-badge {{
  display: inline-block; margin-top: 3px; font-size: 11px;
  background: #d1fae5; color: #065f46;
  border-radius: 4px; padding: 1px 6px;
}}
.portal-reply {{
  margin-top: 6px; margin-left: 10px;
  background: #f8fafc; border-style: dashed;
}}
.portal-reply-btn {{
  margin-top: 6px; font-size: 12px; background: none;
  border: 1px solid #e2e8f0; border-radius: 4px;
  padding: 2px 9px; cursor: pointer; color: #64748b; display: block;
}}
.portal-reply-form {{ margin-top: 6px; }}
.portal-input, .portal-textarea {{
  display: block; width: 100%; padding: 5px 8px;
  border: 1px solid #e2e8f0; border-radius: 6px;
  font-size: 13px; margin-bottom: 5px;
  box-sizing: border-box; font-family: inherit;
}}
.portal-textarea {{ resize: vertical; }}
.portal-btn {{
  padding: 5px 14px; background: #2563eb; color: #fff;
  border: none; border-radius: 6px; font-size: 13px;
  cursor: pointer; font-weight: 500;
}}
.portal-btn:hover {{ background: #1d4ed8; }}
.portal-btn-sm {{ padding: 3px 10px; font-size: 12px; }}
.portal-empty {{
  color: #94a3b8; text-align: center;
  padding: 20px 0; font-size: 13px;
}}
</style>

<div id="portal-sidebar">
  <div id="portal-top">
    <a href="{back_url}" class="back">&larr; Back to campaign</a>
    <div id="portal-title">
      Feedback<span class="portal-count">{count}</span>
      <button id="portal-toggle" title="Collapse">&#x2715;</button>
    </div>
  </div>
  <div class="portal-pill">&#9998;&nbsp; Highlight any text to leave feedback</div>
  <div id="portal-scroll">
    {comments_html}
  </div>
</div>

<script>
var TOKEN = {token_js};
var CONTENT_PATH = {path_js};
var COMMENTS_DATA = {comments_json_str};
var REVIEWER_NAME = {name_js};

// Mark content area so annotation.js can find it
(function() {{
  var rc = document.querySelector('.rich-text-block-11.w-richtext');
  if (rc) rc.classList.add('rendered-content');
}})();

// Sidebar collapse toggle
document.getElementById('portal-toggle').addEventListener('click', function() {{
  var sb = document.getElementById('portal-sidebar');
  var collapsed = sb.classList.toggle('collapsed');
  this.textContent = collapsed ? '\\u2261' : '\\u2715';
  document.body.style.marginRight = collapsed ? '24px' : '320px';
}});

// Reply form handling
function togglePortalReply(id) {{
  var f = document.getElementById('prf-' + id);
  if (f) f.style.display = f.style.display === 'none' ? 'block' : 'none';
}}
document.querySelectorAll('.portal-reply-form').forEach(function(form) {{
  form.addEventListener('submit', function(e) {{
    e.preventDefault();
    var btn = form.querySelector('[type=submit]');
    if (btn) {{ btn.disabled = true; btn.textContent = 'Saving…'; }}
    fetch('/api/review/' + TOKEN + '/comments/' + CONTENT_PATH, {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{
        author_name: form.author_name.value,
        body: form.body.value,
        parent_id: parseInt(form.parent_id.value),
      }}),
    }}).then(function(r) {{
      if (r.ok) location.reload();
      else r.json().then(function(err) {{ alert(err.detail || 'Failed'); }});
    }});
  }});
}});
</script>
<script src="/static/annotation.js"></script>"""


@router.get("/review/{token}/blog/{content_path:path}", response_class=HTMLResponse)
async def blog_review(
    request: Request,
    token: uuid.UUID,
    content_path: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Review link not active.")

    link.last_accessed_at = datetime.now(timezone.utc)
    link.access_count += 1
    await db.commit()

    raw_html = content_svc.get_content_html(link.client_slug, link.campaign_slug, content_path)
    if raw_html is None:
        raise HTTPException(status_code=404, detail="Content file not found.")

    comments_q = await db.execute(
        select(Comment)
        .where(
            Comment.share_link_token == token,
            Comment.content_path == content_path,
            Comment.parent_id.is_(None),
        )
        .order_by(Comment.created_at.desc())
    )
    comments = comments_q.scalars().all()

    comment_ids = [c.id for c in comments]
    replies_map: dict[int, list] = {cid: [] for cid in comment_ids}
    if comment_ids:
        replies_q = await db.execute(
            select(Comment)
            .where(Comment.parent_id.in_(comment_ids))
            .order_by(Comment.created_at.asc())
        )
        for reply in replies_q.scalars().all():
            replies_map.setdefault(reply.parent_id, []).append(reply)

    comments_json_str = json.dumps([
        {
            "id": c.id,
            "author_name": c.author_name,
            "body": c.body,
            "highlight_text": c.highlight_text,
            "anchor_prefix": c.anchor_prefix,
            "anchor_suffix": c.anchor_suffix,
            "anchor_start_offset": c.anchor_start_offset,
            "anchor_end_offset": c.anchor_end_offset,
            "anchor_heading": c.anchor_heading,
            "anchor_paragraph_index": c.anchor_paragraph_index,
            "resolved": c.resolved,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in comments
    ])

    reviewer_name = link.recipient_name or ""
    overlay = _build_blog_overlay(
        str(token), content_path, comments, replies_map, comments_json_str, reviewer_name
    )

    if "</body>" in raw_html:
        final_html = raw_html.replace("</body>", overlay + "\n</body>", 1)
    else:
        final_html = raw_html + overlay

    return HTMLResponse(content=final_html)
