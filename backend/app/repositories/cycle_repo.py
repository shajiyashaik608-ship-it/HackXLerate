from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.cycle import CycleRecord
from app.models.symptom import SymptomRecord


class CycleRepository(BaseRepository[CycleRecord]):
    def __init__(self):
        super().__init__(CycleRecord)

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[CycleRecord]:
        stmt = (
            select(CycleRecord)
            .where(CycleRecord.user_id == user_id)
            .order_by(desc(CycleRecord.start_date))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def get_by_id_and_user(self, db: Session, cycle_id: int, user_id: int) -> Optional[CycleRecord]:
        stmt = select(CycleRecord).where(
            CycleRecord.id == cycle_id,
            CycleRecord.user_id == user_id
        )
        return db.scalars(stmt).first()


class SymptomRepository(BaseRepository[SymptomRecord]):
    def __init__(self):
        super().__init__(SymptomRecord)

    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[SymptomRecord]:
        stmt = select(SymptomRecord).where(SymptomRecord.user_id == user_id)
        if start_date:
            stmt = stmt.where(SymptomRecord.recorded_date >= start_date)
        if end_date:
            stmt = stmt.where(SymptomRecord.recorded_date <= end_date)
        stmt = stmt.order_by(desc(SymptomRecord.recorded_date)).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def get_by_id_and_user(self, db: Session, symptom_id: int, user_id: int) -> Optional[SymptomRecord]:
        stmt = select(SymptomRecord).where(
            SymptomRecord.id == symptom_id,
            SymptomRecord.user_id == user_id
        )
        return db.scalars(stmt).first()


cycle_repo = CycleRepository()
symptom_repo = SymptomRepository()
