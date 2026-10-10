from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BiomarkerResponse(BaseModel):
    id: int
    user_id: int
    document_id: Optional[int] = None
    test_name: str
    observed_value: str
    numeric_value: Optional[float] = None
    unit: str
    reference_range_lower: Optional[float] = None
    reference_range_upper: Optional[float] = None
    reference_range_text: Optional[str] = None
    status: str  # normal, elevated, low, borderline
    test_date: Optional[date] = None
    extraction_confidence: float
    source_page: Optional[int] = 1
    is_user_corrected: bool
    plain_explanation: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BiomarkerCorrectionRequest(BaseModel):
    test_name: Optional[str] = None
    observed_value: Optional[str] = None
    numeric_value: Optional[float] = None
    unit: Optional[str] = None
    reference_range_lower: Optional[float] = None
    reference_range_upper: Optional[float] = None
    status: Optional[str] = None


BiomarkerCorrectionUpdate = BiomarkerCorrectionRequest


class BiomarkerExplainResponse(BaseModel):
    biomarker_id: Optional[int] = None
    test_name: str
    observed_value: Optional[str] = None
    status: str
    explanation: Optional[str] = None
    suggested_questions: list[str] = []
    safety_disclaimer: Optional[str] = "Educational only. Not a definitive diagnosis or medical prescription."
    plain_explanation: Optional[str] = None
    pcos_clinical_context: Optional[str] = None
    disclaimer: Optional[str] = None


class BiomarkerTrendItem(BaseModel):
    test_name: str
    unit: str
    history: list[dict] = []
    data_points_count: int


class BiomarkerTrendsResponse(BaseModel):
    trends: list[BiomarkerTrendItem] = []
    comparability_notice: str

