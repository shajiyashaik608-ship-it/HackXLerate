from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class CycleRecord(Base, TimestampMixin):
    __tablename__ = "cycle_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    start_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    duration_days: Mapped[Optional[int]] = mapped_column(Integer, default=4, nullable=True)
    flow_intensity: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)  # spotting, light, medium, heavy
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="cycles")
