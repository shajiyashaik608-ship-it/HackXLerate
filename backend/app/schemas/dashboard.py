from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.document import MedicalDocumentResponse
from app.schemas.biomarker import BiomarkerResponse
from app.schemas.cycle import CycleLogResponse, CycleEstimateResponse
from app.schemas.symptom import SymptomLogResponse
from app.schemas.reminder import ReminderResponse
from app.schemas.meal import MealPlanResponse


class DashboardSummaryResponse(BaseModel):
    user_name: str
    recent_reports: List[MedicalDocumentResponse] = []
    reviewed_biomarkers: List[BiomarkerResponse] = []
    flagged_biomarkers_count: int = 0
    cycle_status: Optional[CycleEstimateResponse] = None
    last_cycle: Optional[CycleLogResponse] = None
    recent_symptoms: List[SymptomLogResponse] = []
    active_reminders: List[ReminderResponse] = []
    todays_meal_plan: Optional[MealPlanResponse] = None
    health_score_insight: str = "Focus on nutrient-dense meals and balanced rest this week."
    urgent_warning_present: bool = False
