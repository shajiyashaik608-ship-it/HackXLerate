from typing import Optional
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class ConsultationBrief(Base, TimestampMixin):
    __tablename__ = "consultation_briefs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    primary_concerns: Mapped[str] = mapped_column(Text, nullable=False)
    symptoms_summary: Mapped[str] = mapped_column(Text, nullable=False)
    lab_flags_summary: Mapped[str] = mapped_column(Text, nullable=False)
    prioritized_questions: Mapped[str] = mapped_column(Text, nullable=False)  # JSON serialized list of questions
