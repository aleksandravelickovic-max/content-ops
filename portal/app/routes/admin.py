"""Admin routes for managing share links and reviewing comments."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import ShareLink, Comment
from .. import content as content_svc
from ..config import BASE_URL

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    links_q = await db.execute(
        select(ShareLink).order_by(desc(ShareLink.created_at))
    )
    links = links_q.scalars().all()

    # Comment counts per link
    counts_q = await db.execute(
        select(Comment.share_link_token, func.count(Comment.id))
        .group_by(Comment.share_link_token)
    )
    comment_counts = dict(counts_q.all())

    unresolved_q = await db.execute(
        select(Comment.share_link_token, func.count(Comment.id))
        .where(~Comment.resolved, Comment.parent_id.is_(None))
        .group_by(Comment.share_link_token)
    )
    unresolved_counts = dict(unresolved_q.all())

    clients = content_svc.list_clients()
    campaigns_by_client = {}
    for c in clients:
        campaigns_by_client[c] = content_svc.list_campaigns(c)

    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "links": links,
        "comment_counts": comment_counts,
        "unresolved_counts": unresolved_counts,
        "clients": clients,
        "campaigns_by_client": campaigns_by_client,
        "base_url": BASE_URL,
    })


@router.post("/share-links")
async def create_share_link(
    request: Request,
    client_slug: str = Form(...),
    campaign_slug: str = Form(...),
    label: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    # Verify campaign exists
    registry = content_svc.load_registry(client_slug, campaign_slug)
    if not registry:
        raise HTTPException(status_code=404, detail=f"Campaign {client_slug}/{campaign_slug} not found.")

    link = ShareLink(
        client_slug=client_slug,
        campaign_slug=campaign_slug,
        label=label.strip() or f"{client_slug} / {campaign_slug}",
    )
    db.add(link)
    await db.commit()
    await db.refresh(link)

    return RedirectResponse(url="/admin/", status_code=303)


@router.post("/share-links/{token}/toggle")
async def toggle_share_link(
    token: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Share link not found.")

    link.is_active = not link.is_active
    await db.commit()

    return RedirectResponse(url="/admin/", status_code=303)


@router.get("/comments", response_class=HTMLResponse)
async def admin_comments(
    request: Request,
    token: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Comment).where(Comment.parent_id.is_(None)).order_by(desc(Comment.created_at))
    if token:
        query = query.where(Comment.share_link_token == uuid.UUID(token))

    result = await db.execute(query)
    comments = result.scalars().all()

    # Load share link info for each comment
    link_tokens = {c.share_link_token for c in comments}
    links_q = await db.execute(select(ShareLink).where(ShareLink.token.in_(link_tokens)))
    links_map = {lnk.token: lnk for lnk in links_q.scalars().all()}

    # Load reply counts
    reply_counts_q = await db.execute(
        select(Comment.parent_id, func.count(Comment.id))
        .where(Comment.parent_id.isnot(None))
        .group_by(Comment.parent_id)
    )
    reply_counts = dict(reply_counts_q.all())

    all_links_q = await db.execute(select(ShareLink).order_by(desc(ShareLink.created_at)))
    all_links = all_links_q.scalars().all()

    return templates.TemplateResponse("admin/comments.html", {
        "request": request,
        "comments": comments,
        "links_map": links_map,
        "reply_counts": reply_counts,
        "all_links": all_links,
        "selected_token": token,
    })


@router.post("/comments/{comment_id}/resolve")
async def admin_resolve_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime, timezone

    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")

    comment.resolved = not comment.resolved
    comment.resolved_at = datetime.now(timezone.utc) if comment.resolved else None
    await db.commit()

    return RedirectResponse(url=f"/admin/comments?token={comment.share_link_token}", status_code=303)
