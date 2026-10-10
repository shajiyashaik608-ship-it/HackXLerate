from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class CycleRecordCreate(BaseModel):
    start_date: date
    end_date: Optional[date] = None
    flow_intensity: str = "moderate"
    symptoms: List[str] = []
    notes: Optional[str] = None

class CycleRecordResponse(BaseModel):
    id: int
    user_id: int
    start_date: date
    end_date: Optional[date] = None
    flow_intensity: str
    symptoms: List[str]
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CyclePredictionResponse(BaseModel):
    estimated_next_cycle: Optional[str] = None
    variance_days: str
    phase_estimate: str
    disclaimer: str
