from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PrivacyPurgeRequest(BaseModel):
    confirm_phrase: str = Field(..., description="Must equal 'DELETE MY HEALTH DATA'")
    reason: Optional[str] = None


class PrivacyPurgeResponse(BaseModel):
    status: str = "completed"
    message: str = "All personal health records, cycle entries, uploaded reports, and account data have been permanently deleted."
    records_deleted: Dict[str, int] = {}
    purged_at: datetime


class PrivacyExportResponse(BaseModel):
    export_version: str = "1.0"
    exported_at: datetime
    user_info: Dict[str, Any]
    health_profile: Optional[Dict[str, Any]] = None
    medical_documents: List[Dict[str, Any]] = []
    biomarkers: List[Dict[str, Any]] = []
    cycle_records: List[Dict[str, Any]] = []
    symptom_records: List[Dict[str, Any]] = []
    reminders: List[Dict[str, Any]] = []
    meal_plans: List[Dict[str, Any]] = []
    consultations: List[Dict[str, Any]] = []
    conversations: List[Dict[str, Any]] = []
    data_retention_notice: str = "Export contains encrypted and normalized copies of all primary health entries recorded to date."
