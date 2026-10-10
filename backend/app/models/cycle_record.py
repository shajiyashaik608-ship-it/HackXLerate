from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class CycleRecord(Base):
    __tablename__ = "cycle_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    flow_intensity = Column(String, default="moderate")  # light, moderate, heavy, spotting
    symptoms = Column(JSON, default=list)  # ["cramps", "acne", "fatigue", "mood_swings"]
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
