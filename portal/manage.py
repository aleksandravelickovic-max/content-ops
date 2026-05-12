#!/usr/bin/env python3
"""CLI for managing the Content Review Portal.

Usage:
    python manage.py create-link --client zia-tile --campaign 01-product-collection-pages
    python manage.py list-links
    python manage.py revoke-link <token>
    python manage.py list-comments [--token <token>]
"""

import argparse
import asyncio
import sys
import uuid

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import DATABASE_URL
from app.models import ShareLink, Comment
from app.database import Base
from app import content as content_svc


engine = create_async_engine(DATABASE_URL)
session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")


async def create_link(client: str, campaign: str, label: str | None = None):
    registry = content_svc.load_registry(client, campaign)
    if not registry:
        print(f"Campaign not found: {client}/{campaign}")
        sys.exit(1)

    async with session_factory() as db:
        link = ShareLink(
            client_slug=client,
            campaign_slug=campaign,
            label=label or f"{client} / {campaign}",
        )
        db.add(link)
        await db.commit()
        await db.refresh(link)

    from app.config import BASE_URL
    print("Share link created:")
    print(f"  Token:    {link.token}")
    print(f"  Client:   {link.client_slug}")
    print(f"  Campaign: {link.campaign_slug}")
    print(f"  URL:      {BASE_URL}/review/{link.token}")


async def list_links():
    async with session_factory() as db:
        result = await db.execute(
            select(ShareLink).order_by(desc(ShareLink.created_at))
        )
        links = result.scalars().all()

    if not links:
        print("No share links found.")
        return

    from app.config import BASE_URL
    for lnk in links:
        status = "ACTIVE" if lnk.is_active else "REVOKED"
        print(f"[{status}] {lnk.client_slug}/{lnk.campaign_slug}")
        print(f"  Token:   {lnk.token}")
        print(f"  Label:   {lnk.label}")
        print(f"  Views:   {lnk.access_count}")
        print(f"  Created: {lnk.created_at}")
        print(f"  URL:     {BASE_URL}/review/{lnk.token}")
        print()


async def revoke_link(token_str: str):
    token = uuid.UUID(token_str)
    async with session_factory() as db:
        result = await db.execute(select(ShareLink).where(ShareLink.token == token))
        link = result.scalar_one_or_none()
        if not link:
            print(f"Link not found: {token}")
            sys.exit(1)
        link.is_active = not link.is_active
        await db.commit()
        status = "activated" if link.is_active else "revoked"
        print(f"Link {status}: {link.token}")


async def list_comments(token_str: str | None = None):
    async with session_factory() as db:
        query = (
            select(Comment)
            .where(Comment.parent_id.is_(None))
            .order_by(desc(Comment.created_at))
        )
        if token_str:
            query = query.where(Comment.share_link_token == uuid.UUID(token_str))
        result = await db.execute(query)
        comments = result.scalars().all()

    if not comments:
        print("No comments found.")
        return

    for c in comments:
        resolved = " [RESOLVED]" if c.resolved else ""
        print(f"#{c.id}{resolved} — {c.author_name} ({c.created_at.strftime('%Y-%m-%d %H:%M')})")
        print(f"  File: {c.content_path}")
        print(f"  {c.body[:200]}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Content Review Portal CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init-db", help="Create database tables")

    create = sub.add_parser("create-link", help="Create a share link")
    create.add_argument("--client", required=True)
    create.add_argument("--campaign", required=True)
    create.add_argument("--label")

    sub.add_parser("list-links", help="List all share links")

    revoke = sub.add_parser("revoke-link", help="Toggle a share link active/revoked")
    revoke.add_argument("token")

    comments = sub.add_parser("list-comments", help="List comments")
    comments.add_argument("--token", default=None)

    args = parser.parse_args()

    if args.command == "init-db":
        asyncio.run(init_db())
    elif args.command == "create-link":
        asyncio.run(create_link(args.client, args.campaign, args.label))
    elif args.command == "list-links":
        asyncio.run(list_links())
    elif args.command == "revoke-link":
        asyncio.run(revoke_link(args.token))
    elif args.command == "list-comments":
        asyncio.run(list_comments(args.token))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
