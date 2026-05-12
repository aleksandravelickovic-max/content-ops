"""Client-facing review routes. No auth required — the UUID token IS the auth."""

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

    # Count comments per content path
    comment_counts_q = await db.execute(
        select(Comment.content_path, func.count(Comment.id))
        .where(Comment.share_link_token == token, Comment.parent_id.is_(None))
        .group_by(Comment.content_path)
    )
    comment_counts = dict(comment_counts_q.all())

    type_labels = {
        "product-page": "Product Pages",
        "collection-page": "Collection Pages",
        "draft": "Drafts",
        "draft-v3": "V3 Revisions",
        "brief": "Briefs",
        "audit": "Audit Reports",
        "campaign-urls": "URL Maps",
        "blog": "Blog Posts",
        "other": "Other",
    }

    return templates.TemplateResponse("review/campaign.html", {
        "request": request,
        "link": link,
        "registry": registry,
        "groups": groups,
        "type_labels": type_labels,
        "comment_counts": comment_counts,
        "token": str(token),
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

    return templates.TemplateResponse("review/content.html", {
        "request": request,
        "link": link,
        "entry": entry,
        "content_html": rendered_html,
        "comments": comments,
        "replies_map": replies_map,
        "token": str(token),
        "content_path": content_path,
        "prev_entry": prev_entry,
        "next_entry": next_entry,
        "nav_position": f"{current_idx + 1} of {len(same_type)}",
    })
