from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Float, Integer, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.document import MedicalDocument


class Biomarker(Base, TimestampMixin):
    __tablename__ = "biomarkers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("medical_documents.id", ondelete="SET NULL"), index=True, nullable=True)

    test_name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    observed_value: Mapped[str] = mapped_column(String(50), nullable=False)
    numeric_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    
    reference_range_lower: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reference_range_upper: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reference_range_text: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="normal", nullable=False)  # normal, elevated, low, borderline
    test_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    extraction_confidence: Mapped[float] = mapped_column(Float, default=0.95, nullable=False)
    source_page: Mapped[Optional[int]] = mapped_column(Integer, default=1, nullable=True)
    is_user_corrected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    plain_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    document: Mapped[Optional["MedicalDocument"]] = relationship("MedicalDocument", back_populates="biomarkers")
