from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, computed_field
from app.schemas.biomarker import BiomarkerResponse


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_type: str
    category: str
    processing_status: str
    doctor_notes: Optional[str] = None
    upload_date: date
    created_at: datetime
    biomarkers: List[BiomarkerResponse] = []

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def title(self) -> str:
        return self.file_name or "Medical Report"

    @computed_field
    @property
    def report_type(self) -> str:
        return self.category or "blood_test"

    @computed_field
    @property
    def explanation(self) -> str:
        if self.doctor_notes:
            return self.doctor_notes
        if self.biomarkers:
            count = len(self.biomarkers)
            elevated = [b.test_name for b in self.biomarkers if b.status == "elevated"]
            if elevated:
                return f"Analyzed {count} biomarker{'s' if count != 1 else ''}. Parameter{'s' if len(elevated) != 1 else ''} flagged for doctor discussion: {', '.join(elevated)}."
            return f"Analyzed {count} biomarker{'s' if count != 1 else ''}. All parameters within standard ranges."
        return "Processed document."

    @computed_field
    @property
    def structured_data(self) -> List[dict]:
        return [
            {
                "test_name": b.test_name,
                "value": b.observed_value,
                "unit": b.unit,
                "reference_range": b.reference_range_text or f"{b.reference_range_lower} - {b.reference_range_upper} {b.unit}".strip(),
                "status": b.status,
                "plain_explanation": b.plain_explanation or f"Tracked value for {b.test_name}."
            }
            for b in self.biomarkers
        ]



class DocumentStatusResponse(BaseModel):
    id: int
    file_name: str
    processing_status: str  # uploaded, processing, needs_review, completed, failed
    error_message: Optional[str] = None


MedicalDocumentResponse = DocumentResponse
MedicalDocumentStatusResponse = DocumentStatusResponse

