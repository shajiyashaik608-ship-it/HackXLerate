from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class MedicalReport(Base):
    __tablename__ = "medical_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    report_type = Column(String, default="blood_test")  # blood_test, ultrasound, prescription
    file_path = Column(String, nullable=True)
    extracted_text = Column(Text, nullable=True)
    structured_data = Column(JSON, nullable=True)  # List of {test_name, value, unit, reference_range, flag}
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
