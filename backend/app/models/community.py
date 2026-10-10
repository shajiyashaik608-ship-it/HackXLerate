from typing import Optional, List
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class CommunityPost(Base, TimestampMixin):
    __tablename__ = "community_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    pseudonym: Mapped[str] = mapped_column(String(100), default="Anonymous Saathi", nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    helpful_votes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_flagged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    replies: Mapped[List["CommunityReply"]] = relationship("CommunityReply", back_populates="post", cascade="all, delete-orphan")
    reports: Mapped[List["ContentReport"]] = relationship("ContentReport", back_populates="post", cascade="all, delete-orphan")


class CommunityReply(Base, TimestampMixin):
    __tablename__ = "community_replies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("community_posts.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    pseudonym: Mapped[str] = mapped_column(String(100), default="Anonymous Saathi", nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    post: Mapped["CommunityPost"] = relationship("CommunityPost", back_populates="replies")


class ContentReport(Base, TimestampMixin):
    __tablename__ = "content_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("community_posts.id", ondelete="CASCADE"), index=True, nullable=False)
    reporter_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending_review", nullable=False)

    post: Mapped["CommunityPost"] = relationship("CommunityPost", back_populates="reports")
