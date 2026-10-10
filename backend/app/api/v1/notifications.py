from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.repositories.notification_repo import notification_repo
from app.schemas.notification import NotificationResponse
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/pending", response_model=List[NotificationResponse])
def get_pending_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notification_repo.get_pending_by_user(db, user_id=current_user.id)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notif = notification_repo.mark_read(db, notification_id=notification_id, user_id=current_user.id)
    if not notif:
        raise NotFoundException("Notification not found.")
    return notif
