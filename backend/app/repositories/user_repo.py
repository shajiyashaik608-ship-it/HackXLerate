from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.user import User
from app.models.profile import HealthProfile


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        normalized_email = email.lower().strip()
        stmt = select(User).where(User.email == normalized_email)
        return db.scalars(stmt).first()

    def get_profile_by_user_id(self, db: Session, user_id: int) -> Optional[HealthProfile]:
        stmt = select(HealthProfile).where(HealthProfile.user_id == user_id)
        return db.scalars(stmt).first()

    def create_profile(self, db: Session, profile: HealthProfile) -> HealthProfile:
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile


user_repo = UserRepository()
