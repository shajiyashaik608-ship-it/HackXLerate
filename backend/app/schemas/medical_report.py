from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class BiomarkerItem(BaseModel):
    test_name: str
    value: str
    unit: str
    reference_range: str
    status: str  # "normal", "elevated", "low", "review_needed"
    plain_explanation: str

class ReportCreate(BaseModel):
    title: str
    report_type: str = "blood_test"
    extracted_text: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    user_id: int
    title: str
    report_type: str
    structured_data: Optional[List[BiomarkerItem]] = None
    explanation: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReportAnalyzeRequest(BaseModel):
    raw_text: Optional[str] = None
    report_type: Optional[str] = "blood_test"
