from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.community import CommunityPost, CommunityReply, ContentReport


class CommunityRepository(BaseRepository[CommunityPost]):
    def __init__(self):
        super().__init__(CommunityPost)

    def get_public_posts(self, db: Session, skip: int = 0, limit: int = 50, tag: Optional[str] = None) -> List[CommunityPost]:
        stmt = (
            select(CommunityPost)
            .options(joinedload(CommunityPost.replies))
            .where(CommunityPost.status == "active")
        )
        if tag:
            stmt = stmt.where(CommunityPost.tags.ilike(f"%{tag}%"))
        stmt = stmt.order_by(desc(CommunityPost.created_at)).offset(skip).limit(limit)
        return list(db.scalars(stmt).unique().all())

    def get_post_by_id(self, db: Session, post_id: int) -> Optional[CommunityPost]:
        stmt = (
            select(CommunityPost)
            .options(joinedload(CommunityPost.replies))
            .where(CommunityPost.id == post_id)
        )
        return db.scalars(stmt).first()

    def add_reply(self, db: Session, reply: CommunityReply) -> CommunityReply:
        db.add(reply)
        db.commit()
        db.refresh(reply)
        return reply

    def add_report(self, db: Session, report: ContentReport) -> ContentReport:
        db.add(report)
        db.commit()
        db.refresh(report)
        return report


community_repo = CommunityRepository()
