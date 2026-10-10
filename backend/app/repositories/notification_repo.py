from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.notification import Notification


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self):
        super().__init__(Notification)

    def get_pending_by_user(self, db: Session, user_id: int) -> List[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id, Notification.is_read == False)
            .order_by(desc(Notification.created_at))
        )
        return list(db.scalars(stmt).all())

    def mark_read(self, db: Session, notification_id: int, user_id: int) -> Optional[Notification]:
        stmt = select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
        notif = db.scalars(stmt).first()
        if notif:
            notif.is_read = True
            db.commit()
            db.refresh(notif)
        return notif


notification_repo = NotificationRepository()
