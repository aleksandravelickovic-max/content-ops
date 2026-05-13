"""Admin routes for managing share links, reviewing comments, and browsing campaigns."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import ShareLink, Comment
from .. import content as content_svc
from ..config import ALLOWED_DOMAINS, BASE_URL
from .auth import is_oauth_configured

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")


def _get_user_or_none(request: Request) -> dict | None:
    """Return session user dict if present and domain-valid, else None."""
    user = request.session.get("user")
    if not user:
        return None
    email = user.get("email", "")
    if "@" not in email:
        return None
    domain = email.rsplit("@", 1)[1].lower()
    if domain not in ALLOWED_DOMAINS:
        return None
    return user


async def require_admin(request: Request) -> dict | None:
    """Dependency that enforces Google OAuth on admin routes.

    When OAuth is not configured (dev mode), access is unrestricted and
    returns None. When configured, redirects unauthenticated users to login.
    """
    if not is_oauth_configured():
        return None

    user = _get_user_or_none(request)
    if user is None:
        raise HTTPException(
            status_code=307,
            headers={"Location": "/auth/login"},
        )
    return user


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
):
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
        "user": user,
    })


@router.post("/share-links")
async def create_share_link(
    request: Request,
    client_slug: str = Form(...),
    campaign_slug: str = Form(...),
    label: str = Form(""),
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
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
    request: Request,
    redirect: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Share link not found.")

    link.is_active = not link.is_active
    await db.commit()

    return RedirectResponse(url=redirect or "/admin/", status_code=303)


@router.get("/comments", response_class=HTMLResponse)
async def admin_comments(
    request: Request,
    token: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
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
        "user": user,
    })


@router.post("/comments/{comment_id}/resolve")
async def admin_resolve_comment(
    comment_id: int,
    request: Request,
    redirect: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
):
    from datetime import datetime, timezone

    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")

    comment.resolved = not comment.resolved
    comment.resolved_at = datetime.now(timezone.utc) if comment.resolved else None
    await db.commit()

    if redirect:
        return RedirectResponse(url=redirect, status_code=303)
    return RedirectResponse(url=f"/admin/comments?token={comment.share_link_token}", status_code=303)


# ── Campaign Browser Routes ──────────────────────────────────────────


# Shared constants for tab ordering / labels (same as review routes)
_TYPE_LABELS = {
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

_TAB_ORDER = [
    "product-page", "collection-page", "draft", "draft-v3",
    "html-revised", "html-original",
    "brief", "audit", "campaign-urls", "blog", "html-index", "other",
]


def _build_tabs(groups: dict[str, list]) -> list[dict]:
    """Build ordered tab list from content groups dict."""
    tabs = []
    for t in _TAB_ORDER:
        if t in groups:
            tabs.append({
                "key": t,
                "label": _TYPE_LABELS.get(t, t.replace("-", " ").title()),
                "count": len(groups[t]),
            })
    for t in groups:
        if t not in _TAB_ORDER:
            tabs.append({
                "key": t,
                "label": _TYPE_LABELS.get(t, t.replace("-", " ").title()),
                "count": len(groups[t]),
            })
    return tabs


@router.get("/campaigns", response_class=HTMLResponse)
async def admin_campaigns(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
):
    """Campaign overview — list all clients and their campaigns with stats."""
    clients = content_svc.list_clients()

    # Gather campaign info for each client
    client_campaigns: list[dict] = []
    for client_slug in clients:
        campaigns = content_svc.list_campaigns(client_slug)
        for campaign_slug in campaigns:
            registry = content_svc.load_registry(client_slug, campaign_slug)
            file_count = registry.get("totalFiles", 0) if registry else 0
            client_campaigns.append({
                "client_slug": client_slug,
                "campaign_slug": campaign_slug,
                "file_count": file_count,
            })

    # Batch query: share link counts per client/campaign
    link_counts_q = await db.execute(
        select(
            ShareLink.client_slug,
            ShareLink.campaign_slug,
            func.count(ShareLink.token),
        )
        .where(ShareLink.is_active.is_(True))
        .group_by(ShareLink.client_slug, ShareLink.campaign_slug)
    )
    link_counts = {
        (row[0], row[1]): row[2] for row in link_counts_q.all()
    }

    # Batch query: total comments per client/campaign (via share links)
    comment_totals_q = await db.execute(
        select(
            ShareLink.client_slug,
            ShareLink.campaign_slug,
            func.count(Comment.id),
        )
        .join(Comment, Comment.share_link_token == ShareLink.token)
        .where(Comment.parent_id.is_(None))
        .group_by(ShareLink.client_slug, ShareLink.campaign_slug)
    )
    comment_totals = {
        (row[0], row[1]): row[2] for row in comment_totals_q.all()
    }

    # Batch query: unresolved comments per client/campaign
    unresolved_totals_q = await db.execute(
        select(
            ShareLink.client_slug,
            ShareLink.campaign_slug,
            func.count(Comment.id),
        )
        .join(Comment, Comment.share_link_token == ShareLink.token)
        .where(Comment.parent_id.is_(None), Comment.resolved.is_(False))
        .group_by(ShareLink.client_slug, ShareLink.campaign_slug)
    )
    unresolved_totals = {
        (row[0], row[1]): row[2] for row in unresolved_totals_q.all()
    }

    # Enrich campaign dicts with stats
    for camp in client_campaigns:
        key = (camp["client_slug"], camp["campaign_slug"])
        camp["link_count"] = link_counts.get(key, 0)
        camp["comment_count"] = comment_totals.get(key, 0)
        camp["unresolved_count"] = unresolved_totals.get(key, 0)

    # Group by client
    campaigns_by_client: dict[str, list[dict]] = {}
    for camp in client_campaigns:
        campaigns_by_client.setdefault(camp["client_slug"], []).append(camp)

    return templates.TemplateResponse("admin/campaigns.html", {
        "request": request,
        "clients": clients,
        "campaigns_by_client": campaigns_by_client,
        "user": user,
    })


@router.get("/campaigns/{client_slug}/{campaign_slug}", response_class=HTMLResponse)
async def admin_campaign_detail(
    request: Request,
    client_slug: str,
    campaign_slug: str,
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
):
    """Campaign detail — content browser with admin powers."""
    registry = content_svc.load_registry(client_slug, campaign_slug)
    if not registry:
        raise HTTPException(status_code=404, detail=f"Campaign {client_slug}/{campaign_slug} not found.")

    # Group entries by type
    groups: dict[str, list] = {}
    for entry in registry.get("entries", []):
        t = entry.get("type", "other")
        groups.setdefault(t, []).append(entry)

    tabs = _build_tabs(groups)

    # Find active share links for this campaign
    links_q = await db.execute(
        select(ShareLink)
        .where(
            ShareLink.client_slug == client_slug,
            ShareLink.campaign_slug == campaign_slug,
        )
        .order_by(desc(ShareLink.created_at))
    )
    share_links = links_q.scalars().all()
    active_link = next((lnk for lnk in share_links if lnk.is_active), None)

    # Comment counts per content path (aggregate across all share links for this campaign)
    link_tokens = [lnk.token for lnk in share_links]
    comment_counts: dict[str, int] = {}
    unresolved_counts: dict[str, int] = {}

    if link_tokens:
        cc_q = await db.execute(
            select(Comment.content_path, func.count(Comment.id))
            .where(
                Comment.share_link_token.in_(link_tokens),
                Comment.parent_id.is_(None),
            )
            .group_by(Comment.content_path)
        )
        comment_counts = dict(cc_q.all())

        uc_q = await db.execute(
            select(Comment.content_path, func.count(Comment.id))
            .where(
                Comment.share_link_token.in_(link_tokens),
                Comment.parent_id.is_(None),
                Comment.resolved.is_(False),
            )
            .group_by(Comment.content_path)
        )
        unresolved_counts = dict(uc_q.all())

    return templates.TemplateResponse("admin/campaign_detail.html", {
        "request": request,
        "registry": registry,
        "groups": groups,
        "tabs": tabs,
        "client_slug": client_slug,
        "campaign_slug": campaign_slug,
        "share_links": share_links,
        "active_link": active_link,
        "comment_counts": comment_counts,
        "unresolved_counts": unresolved_counts,
        "base_url": BASE_URL,
        "user": user,
    })


@router.post("/campaigns/{client_slug}/{campaign_slug}/share-link")
async def admin_campaign_create_share_link(
    request: Request,
    client_slug: str,
    campaign_slug: str,
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
):
    """Create a share link from the campaign detail page."""
    registry = content_svc.load_registry(client_slug, campaign_slug)
    if not registry:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    link = ShareLink(
        client_slug=client_slug,
        campaign_slug=campaign_slug,
        label=f"{client_slug} / {campaign_slug}",
    )
    db.add(link)
    await db.commit()

    return RedirectResponse(
        url=f"/admin/campaigns/{client_slug}/{campaign_slug}",
        status_code=303,
    )


@router.get("/campaigns/{client_slug}/{campaign_slug}/{content_path:path}", response_class=HTMLResponse)
async def admin_content_detail(
    request: Request,
    client_slug: str,
    campaign_slug: str,
    content_path: str,
    db: AsyncSession = Depends(get_db),
    user: dict | None = Depends(require_admin),
):
    """Content detail view with admin comment management."""
    registry = content_svc.load_registry(client_slug, campaign_slug)
    if not registry:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    entry = next((e for e in registry.get("entries", []) if e["path"] == content_path), None)
    if not entry:
        raise HTTPException(status_code=404, detail="Content piece not found.")

    rendered_html = content_svc.get_content_html(client_slug, campaign_slug, content_path)
    if rendered_html is None:
        raise HTTPException(status_code=404, detail="Unable to read content file.")

    # Find share links for this campaign to load comments
    links_q = await db.execute(
        select(ShareLink).where(
            ShareLink.client_slug == client_slug,
            ShareLink.campaign_slug == campaign_slug,
        )
    )
    share_links = links_q.scalars().all()
    link_tokens = [lnk.token for lnk in share_links]

    comments: list = []
    replies_map: dict[int, list] = {}

    if link_tokens:
        comments_q = await db.execute(
            select(Comment)
            .where(
                Comment.share_link_token.in_(link_tokens),
                Comment.content_path == content_path,
                Comment.parent_id.is_(None),
            )
            .order_by(Comment.created_at.desc())
        )
        comments = list(comments_q.scalars().all())

        comment_ids = [c.id for c in comments]
        replies_map = {cid: [] for cid in comment_ids}
        if comment_ids:
            replies_q = await db.execute(
                select(Comment)
                .where(Comment.parent_id.in_(comment_ids))
                .order_by(Comment.created_at.asc())
            )
            for reply in replies_q.scalars().all():
                replies_map.setdefault(reply.parent_id, []).append(reply)

    # Build prev/next navigation within same content type
    all_entries = registry.get("entries", [])
    same_type = [e for e in all_entries if e["type"] == entry["type"]]
    current_idx = next((i for i, e in enumerate(same_type) if e["path"] == content_path), 0)
    prev_entry = same_type[current_idx - 1] if current_idx > 0 else None
    next_entry = same_type[current_idx + 1] if current_idx < len(same_type) - 1 else None

    return templates.TemplateResponse("admin/content_detail.html", {
        "request": request,
        "entry": entry,
        "content_html": rendered_html,
        "comments": comments,
        "replies_map": replies_map,
        "client_slug": client_slug,
        "campaign_slug": campaign_slug,
        "content_path": content_path,
        "prev_entry": prev_entry,
        "next_entry": next_entry,
        "nav_position": f"{current_idx + 1} of {len(same_type)}",
        "user": user,
    })
