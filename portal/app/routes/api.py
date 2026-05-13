"""API routes for comments and share link management."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import ShareLink, Comment

router = APIRouter(prefix="/api")


class CommentCreate(BaseModel):
    author_name: str
    author_email: str | None = None
    body: str
    highlight_text: str | None = None
    parent_id: int | None = None
    anchor_prefix: str | None = None
    anchor_suffix: str | None = None
    anchor_start_offset: int | None = None
    anchor_end_offset: int | None = None
    anchor_heading: str | None = None
    anchor_paragraph_index: int | None = None
    pin_x_percent: float | None = None
    pin_y_percent: float | None = None
    pin_pane: str | None = None


class CommentResolve(BaseModel):
    resolved: bool


@router.post("/review/{token}/comments/{content_path:path}")
async def create_comment(
    token: uuid.UUID,
    content_path: str,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Invalid share link.")

    if not payload.body.strip():
        raise HTTPException(status_code=422, detail="Comment body cannot be empty.")
    if len(payload.body) > 10_000:
        raise HTTPException(status_code=422, detail="Comment too long (max 10,000 characters).")

    if payload.parent_id:
        parent_q = await db.execute(select(Comment).where(Comment.id == payload.parent_id))
        parent = parent_q.scalar_one_or_none()
        if not parent or parent.share_link_token != token:
            raise HTTPException(status_code=404, detail="Parent comment not found.")

    comment = Comment(
        share_link_token=token,
        content_path=content_path,
        author_name=payload.author_name.strip(),
        author_email=payload.author_email.strip() if payload.author_email else None,
        body=payload.body.strip(),
        highlight_text=payload.highlight_text,
        parent_id=payload.parent_id,
        anchor_prefix=payload.anchor_prefix,
        anchor_suffix=payload.anchor_suffix,
        anchor_start_offset=payload.anchor_start_offset,
        anchor_end_offset=payload.anchor_end_offset,
        anchor_heading=payload.anchor_heading,
        anchor_paragraph_index=payload.anchor_paragraph_index,
        pin_x_percent=payload.pin_x_percent,
        pin_y_percent=payload.pin_y_percent,
        pin_pane=payload.pin_pane,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    return JSONResponse({"id": comment.id, "status": "created"}, status_code=201)


@router.patch("/review/{token}/comments/{comment_id}/resolve")
async def resolve_comment(
    token: uuid.UUID,
    comment_id: int,
    payload: CommentResolve,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Invalid share link.")

    result = await db.execute(select(Comment).where(Comment.id == comment_id, Comment.share_link_token == token))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")

    comment.resolved = payload.resolved
    comment.resolved_at = datetime.now(timezone.utc) if payload.resolved else None
    await db.commit()

    return {"id": comment.id, "resolved": comment.resolved}


@router.post("/process/{token}/compare/{filename:path}")
async def process_content(
    token: uuid.UUID,
    filename: str,
    db: AsyncSession = Depends(get_db),
):
    """Trigger HTML processing for a specific page (runs build-html-before-after.py)."""
    import asyncio
    from pathlib import Path

    from ..config import CONTENT_ROOT

    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Invalid share link.")

    scripts_dir = Path(CONTENT_ROOT).parent / "scripts"
    script = scripts_dir / "build-html-before-after.py"
    if not script.exists():
        raise HTTPException(status_code=500, detail="Build script not found.")

    campaign_dir = Path(CONTENT_ROOT) / link.client_slug / "campaigns" / link.campaign_slug

    proc = await asyncio.create_subprocess_exec(
        "python3", str(script),
        cwd=str(campaign_dir.parent.parent.parent),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        return JSONResponse(
            {"status": "error", "detail": stderr.decode(errors="replace")[:2000]},
            status_code=500,
        )

    return {"status": "processed", "filename": filename}


@router.get("/review/{token}/compare-comments/{filename:path}")
async def get_compare_comments(
    token: uuid.UUID,
    filename: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all pin comments for a compare view page."""
    result = await db.execute(select(ShareLink).where(ShareLink.token == token))
    link = result.scalar_one_or_none()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Invalid share link.")

    content_path = f"compare:{filename}"
    comments_q = await db.execute(
        select(Comment)
        .where(
            Comment.share_link_token == token,
            Comment.content_path == content_path,
            Comment.parent_id.is_(None),
        )
        .order_by(Comment.created_at.asc())
    )
    comments = comments_q.scalars().all()

    return [
        {
            "id": c.id,
            "author_name": c.author_name,
            "body": c.body,
            "pin_x_percent": c.pin_x_percent,
            "pin_y_percent": c.pin_y_percent,
            "pin_pane": c.pin_pane,
            "highlight_text": c.highlight_text,
            "resolved": c.resolved,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in comments
    ]
