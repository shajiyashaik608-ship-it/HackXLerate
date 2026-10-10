from datetime import date, datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict


class SymptomLogCreate(BaseModel):
    recorded_date: date = Field(default_factory=date.today)
    symptom_type: str = Field(..., description="E.g., acne, hirsutism, cramps, mood_swings, bloating, fatigue")
    severity: str = Field(default="mild", description="mild, moderate, or severe")
    notes: Optional[str] = None


class SymptomLogUpdate(BaseModel):
    recorded_date: Optional[date] = None
    symptom_type: Optional[str] = None
    severity: Optional[str] = None
    notes: Optional[str] = None


class SymptomLogResponse(BaseModel):
    id: int
    user_id: int
    recorded_date: date
    symptom_type: str
    severity: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SymptomSummaryItem(BaseModel):
    symptom_type: str
    count: int
    most_common_severity: str
    last_reported_date: Optional[date] = None


class SymptomSummaryResponse(BaseModel):
    total_entries: int
    symptoms: List[SymptomSummaryItem]
    frequent_symptom: Optional[str] = None
    urgent_warning_flag: bool = False
    safety_message: Optional[str] = None
