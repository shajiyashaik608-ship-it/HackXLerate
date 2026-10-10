from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class CareReminder(Base, TimestampMixin):
    __tablename__ = "care_reminders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="medication", nullable=False)  # medication, supplement, lifestyle, hydration, appointment
    scheduled_time: Mapped[str] = mapped_column(String(20), default="08:30 AM", nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Kolkata", nullable=False)
    start_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    recurrence: Mapped[str] = mapped_column(String(50), default="Daily", nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="reminders")
    completions: Mapped[List["ReminderCompletion"]] = relationship("ReminderCompletion", back_populates="reminder", cascade="all, delete-orphan")


class ReminderCompletion(Base):
    __tablename__ = "reminder_completions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reminder_id: Mapped[int] = mapped_column(ForeignKey("care_reminders.id", ondelete="CASCADE"), index=True, nullable=False)

    scheduled_occurrence: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    snoozed_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    reminder: Mapped["CareReminder"] = relationship("CareReminder", back_populates="completions")
