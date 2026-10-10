from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.profile import HealthProfile
    from app.models.document import MedicalDocument
    from app.models.cycle import CycleRecord
    from app.models.reminder import CareReminder


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_given: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    profile: Mapped[Optional["HealthProfile"]] = relationship("HealthProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    documents: Mapped[List["MedicalDocument"]] = relationship("MedicalDocument", back_populates="user", cascade="all, delete-orphan")
    cycles: Mapped[List["CycleRecord"]] = relationship("CycleRecord", back_populates="user", cascade="all, delete-orphan")
    reminders: Mapped[List["CareReminder"]] = relationship("CareReminder", back_populates="user", cascade="all, delete-orphan")
