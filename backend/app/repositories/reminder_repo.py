from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.reminder import CareReminder, ReminderCompletion


class ReminderRepository(BaseRepository[CareReminder]):
    def __init__(self):
        super().__init__(CareReminder)

    def get_by_user(self, db: Session, user_id: int) -> List[CareReminder]:
        stmt = (
            select(CareReminder)
            .options(joinedload(CareReminder.completions))
            .where(CareReminder.user_id == user_id)
            .order_by(desc(CareReminder.created_at))
        )
        return list(db.scalars(stmt).unique().all())

    def get_active_by_user(self, db: Session, user_id: int) -> List[CareReminder]:
        stmt = (
            select(CareReminder)
            .options(joinedload(CareReminder.completions))
            .where(CareReminder.user_id == user_id, CareReminder.is_active == True)
            .order_by(CareReminder.scheduled_time)
        )
        return list(db.scalars(stmt).unique().all())

    def get_by_id_and_user(self, db: Session, reminder_id: int, user_id: int) -> Optional[CareReminder]:
        stmt = (
            select(CareReminder)
            .options(joinedload(CareReminder.completions))
            .where(CareReminder.id == reminder_id, CareReminder.user_id == user_id)
        )
        return db.scalars(stmt).first()


class ReminderCompletionRepository(BaseRepository[ReminderCompletion]):
    def __init__(self):
        super().__init__(ReminderCompletion)

    def get_by_reminder(self, db: Session, reminder_id: int) -> List[ReminderCompletion]:
        stmt = select(ReminderCompletion).where(ReminderCompletion.reminder_id == reminder_id)
        return list(db.scalars(stmt).all())


reminder_repo = ReminderRepository()
reminder_completion_repo = ReminderCompletionRepository()
