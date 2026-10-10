from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class HealthProfile(Base, TimestampMixin):
    __tablename__ = "health_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    diet_type: Mapped[str] = mapped_column(String(50), default="vegetarian", nullable=False)
    baseline_cycle_length: Mapped[Optional[int]] = mapped_column(Integer, default=33, nullable=True)
    period_duration: Mapped[Optional[int]] = mapped_column(Integer, default=4, nullable=True)
    wellness_goals: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    allergies: Mapped[Optional[str]] = mapped_column(String(255), default="None", nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata", nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="profile")
