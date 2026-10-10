from datetime import date
from typing import Optional
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class SymptomRecord(Base, TimestampMixin):
    __tablename__ = "symptom_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    recorded_date: Mapped[date] = mapped_column(Date, default=date.today, index=True, nullable=False)
    symptom_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # cramps, acne, fatigue, bloating, mood
    severity: Mapped[str] = mapped_column(String(50), default="mild", nullable=False)  # mild, moderate, severe
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
