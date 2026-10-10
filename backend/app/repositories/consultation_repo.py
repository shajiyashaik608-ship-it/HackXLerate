from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.consultation import ConsultationBrief


class ConsultationRepository(BaseRepository[ConsultationBrief]):
    def __init__(self):
        super().__init__(ConsultationBrief)

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[ConsultationBrief]:
        stmt = (
            select(ConsultationBrief)
            .where(ConsultationBrief.user_id == user_id)
            .order_by(desc(ConsultationBrief.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def get_by_id_and_user(self, db: Session, brief_id: int, user_id: int) -> Optional[ConsultationBrief]:
        stmt = select(ConsultationBrief).where(
            ConsultationBrief.id == brief_id,
            ConsultationBrief.user_id == user_id
        )
        return db.scalars(stmt).first()


consultation_repo = ConsultationRepository()
