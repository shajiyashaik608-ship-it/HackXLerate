from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ConsultationBriefCreate(BaseModel):
    primary_concerns: Optional[str] = Field(None, description="User's primary concerns or appointment goals")
    symptoms_summary: Optional[str] = Field(None, description="Summary of active symptoms")
    lab_flags_summary: Optional[str] = Field(None, description="Summary of flagged/out of range lab tests")
    prioritized_questions: Optional[str] = Field(None, description="Prioritized questions for the clinician")
    include_active_reminders: bool = True
    include_recent_cycles: bool = True


class ConsultationBriefUpdate(BaseModel):
    primary_concerns: Optional[str] = None
    symptoms_summary: Optional[str] = None
    lab_flags_summary: Optional[str] = None
    prioritized_questions: Optional[str] = None


class ConsultationBriefResponse(BaseModel):
    id: int
    user_id: int
    primary_concerns: Optional[str] = None
    symptoms_summary: Optional[str] = None
    lab_flags_summary: Optional[str] = None
    prioritized_questions: Optional[str] = None
    created_at: datetime

    # Additional contextual fields for printable brief
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    recent_cycle_info: Optional[str] = None
    active_medications: List[str] = []

    model_config = ConfigDict(from_attributes=True)
