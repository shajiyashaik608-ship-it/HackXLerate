from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TimelineEvent(BaseModel):
    id: str
    event_type: str  # report_upload, biomarker_result, cycle_entry, symptom_entry, reminder_done, meal_logged
    title: str
    description: str
    timestamp: datetime
    category: str  # medical, cycle, symptom, nutrition, medication
    metadata: Dict[str, Any] = {}


class TimelineResponse(BaseModel):
    total_events: int
    events: List[TimelineEvent] = []
    page: int = 1
    page_size: int = 20
