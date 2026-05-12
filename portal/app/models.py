import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class ShareLink(Base):
    __tablename__ = "share_links"

    token: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    client_slug: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    campaign_slug: Mapped[str] = mapped_column(String(200), nullable=False)
    label: Mapped[str] = mapped_column(String(300), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_accessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    access_count: Mapped[int] = mapped_column(default=0)

    comments: Mapped[list["Comment"]] = relationship(back_populates="share_link", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    share_link_token: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("share_links.token", ondelete="CASCADE"), nullable=False, index=True
    )
    content_path: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    author_name: Mapped[str] = mapped_column(String(200), nullable=False)
    author_email: Mapped[str | None] = mapped_column(String(300), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    highlight_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    anchor_prefix: Mapped[str | None] = mapped_column(Text, nullable=True)
    anchor_suffix: Mapped[str | None] = mapped_column(Text, nullable=True)
    anchor_start_offset: Mapped[int | None] = mapped_column(nullable=True)
    anchor_end_offset: Mapped[int | None] = mapped_column(nullable=True)
    anchor_heading: Mapped[str | None] = mapped_column(Text, nullable=True)
    anchor_paragraph_index: Mapped[int | None] = mapped_column(nullable=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    share_link: Mapped["ShareLink"] = relationship(back_populates="comments")
    replies: Mapped[list["Comment"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    parent: Mapped["Comment | None"] = relationship(back_populates="replies", remote_side=[id])
