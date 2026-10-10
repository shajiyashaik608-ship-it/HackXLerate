from datetime import datetime, timedelta, date
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.reminder import CareReminder, ReminderCompletion
from app.repositories.reminder_repo import reminder_repo, reminder_completion_repo
from app.core.exceptions import NotFoundException, ValidationException


class ReminderService:
    def create_reminder(
        self,
        db: Session,
        user_id: int,
        title: str,
        category: str = "medication",
        scheduled_time: str = "09:00",
        timezone: str = "Asia/Kolkata",
        start_date: Optional[date] = None,
        recurrence: str = "daily",
        notes: Optional[str] = None
    ) -> CareReminder:
        reminder = CareReminder(
            user_id=user_id,
            title=title,
            category=category,
            scheduled_time=scheduled_time,
            timezone=timezone,
            start_date=start_date or date.today(),
            recurrence=recurrence,
            notes=notes,
            is_active=True
        )
        return reminder_repo.create(db, reminder)

    def get_user_reminders(self, db: Session, user_id: int) -> List[CareReminder]:
        return reminder_repo.get_by_user(db, user_id=user_id)

    def get_active_reminders(self, db: Session, user_id: int) -> List[CareReminder]:
        return reminder_repo.get_active_by_user(db, user_id=user_id)

    def get_reminder_by_id(self, db: Session, reminder_id: int, user_id: int) -> CareReminder:
        reminder = reminder_repo.get_by_id_and_user(db, reminder_id=reminder_id, user_id=user_id)
        if not reminder:
            raise NotFoundException("Reminder not found.")
        return reminder

    def update_reminder(self, db: Session, reminder_id: int, user_id: int, update_data: dict) -> CareReminder:
        reminder = self.get_reminder_by_id(db, reminder_id=reminder_id, user_id=user_id)
        return reminder_repo.update(db, reminder, update_data)

    def delete_reminder(self, db: Session, reminder_id: int, user_id: int) -> bool:
        reminder = self.get_reminder_by_id(db, reminder_id=reminder_id, user_id=user_id)
        return reminder_repo.delete(db, reminder.id)

    def complete_reminder(
        self,
        db: Session,
        reminder_id: int,
        user_id: int,
        occurrence_time: Optional[datetime] = None
    ) -> ReminderCompletion:
        reminder = self.get_reminder_by_id(db, reminder_id=reminder_id, user_id=user_id)
        now = datetime.utcnow()
        completion = ReminderCompletion(
            reminder_id=reminder.id,
            scheduled_occurrence=occurrence_time or now,
            is_completed=True,
            completed_at=now
        )
        return reminder_completion_repo.create(db, completion)

    def snooze_reminder(
        self,
        db: Session,
        reminder_id: int,
        user_id: int,
        snooze_minutes: int = 30
    ) -> ReminderCompletion:
        reminder = self.get_reminder_by_id(db, reminder_id=reminder_id, user_id=user_id)
        now = datetime.utcnow()
        snooze_target = now + timedelta(minutes=snooze_minutes)

        completion = ReminderCompletion(
            reminder_id=reminder.id,
            scheduled_occurrence=now,
            is_completed=False,
            snoozed_until=snooze_target
        )
        return reminder_completion_repo.create(db, completion)


reminder_service = ReminderService()
