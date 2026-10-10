from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.reminder_service import reminder_service
from app.schemas.reminder import (
    ReminderCreate,
    ReminderUpdate,
    ReminderResponse,
    ReminderCompletionResponse,
    ReminderSnoozeRequest,
)

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    payload: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reminder_service.create_reminder(
        db=db,
        user_id=current_user.id,
        title=payload.title,
        category=payload.category,
        scheduled_time=payload.scheduled_time,
        timezone=payload.timezone,
        start_date=payload.start_date,
        recurrence=payload.recurrence,
        notes=payload.notes
    )


@router.get("", response_model=List[ReminderResponse])
def list_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reminder_service.get_user_reminders(db, user_id=current_user.id)


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reminder_service.get_reminder_by_id(db, reminder_id=reminder_id, user_id=current_user.id)


@router.patch("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    payload: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = payload.model_dump(exclude_unset=True)
    return reminder_service.update_reminder(
        db=db, reminder_id=reminder_id, user_id=current_user.id, update_data=update_data
    )


@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reminder_service.delete_reminder(db, reminder_id=reminder_id, user_id=current_user.id)
    return {"message": "Reminder deleted successfully."}


@router.post("/{reminder_id}/complete", response_model=ReminderCompletionResponse)
def complete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reminder_service.complete_reminder(db, reminder_id=reminder_id, user_id=current_user.id)


@router.post("/{reminder_id}/snooze", response_model=ReminderCompletionResponse)
def snooze_reminder(
    reminder_id: int,
    payload: ReminderSnoozeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reminder_service.snooze_reminder(
        db, reminder_id=reminder_id, user_id=current_user.id, snooze_minutes=payload.snooze_minutes
    )
