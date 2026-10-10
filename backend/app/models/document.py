from datetime import date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.biomarker import Biomarker


class MedicalDocument(Base, TimestampMixin):
    __tablename__ = "medical_documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)  # PDF, PNG, JPG
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="Blood Test", nullable=False)
    processing_status: Mapped[str] = mapped_column(String(50), default="uploaded", nullable=False) # uploaded, processing, completed, needs_review, failed
    ocr_raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    doctor_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    upload_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="documents")
    biomarkers: Mapped[List["Biomarker"]] = relationship("Biomarker", back_populates="document", cascade="all, delete-orphan")
