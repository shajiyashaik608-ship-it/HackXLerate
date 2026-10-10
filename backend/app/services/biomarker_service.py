from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.biomarker import Biomarker
from app.repositories.document_repo import biomarker_repo
from app.core.exceptions import NotFoundException, ValidationException


class BiomarkerService:
    def get_user_biomarkers(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Biomarker]:
        return biomarker_repo.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

    def get_biomarker(self, db: Session, biomarker_id: int, user_id: int) -> Biomarker:
        marker = biomarker_repo.get_by_id_and_user(db, biomarker_id=biomarker_id, user_id=user_id)
        if not marker:
            raise NotFoundException("Biomarker entry not found.")
        return marker

    def correct_biomarker(
        self,
        db: Session,
        biomarker_id: int,
        user_id: int,
        update_data: dict
    ) -> Biomarker:
        marker = self.get_biomarker(db, biomarker_id=biomarker_id, user_id=user_id)

        for field, value in update_data.items():
            if hasattr(marker, field) and value is not None:
                setattr(marker, field, value)

        if marker.numeric_value is not None and marker.reference_range_lower is not None and marker.reference_range_upper is not None:
            if marker.numeric_value < marker.reference_range_lower:
                marker.status = "low"
            elif marker.numeric_value > marker.reference_range_upper:
                marker.status = "elevated"
            else:
                marker.status = "normal"

        marker.is_user_corrected = True
        db.commit()
        db.refresh(marker)
        return marker

    def get_trends(
        self,
        db: Session,
        user_id: int,
        test_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Groups biomarkers by test name and unit, comparing only compatible observations.
        """
        all_markers = biomarker_repo.get_trends(db, user_id=user_id, test_name=test_name)
        groups: Dict[str, List[Biomarker]] = {}

        for m in all_markers:
            key = f"{m.test_name} ({m.unit})"
            if key not in groups:
                groups[key] = []
            groups[key].append(m)

        trends_data = []
        for test_key, items in groups.items():
            history = []
            for item in items:
                history.append({
                    "id": item.id,
                    "date": item.test_date,
                    "numeric_value": item.numeric_value,
                    "observed_value": item.observed_value,
                    "unit": item.unit,
                    "status": item.status,
                    "reference_range": item.reference_range_text
                })

            trends_data.append({
                "test_name": items[0].test_name,
                "unit": items[0].unit,
                "history": history,
                "data_points_count": len(history)
            })

        return {
            "trends": trends_data,
            "comparability_notice": "Trends are computed strictly across records with identical test names and units."
        }

    def explain_biomarker(
        self,
        db: Session,
        biomarker_id: int,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Provides non-diagnostic plain-language educational context.
        """
        marker = self.get_biomarker(db, biomarker_id=biomarker_id, user_id=user_id)

        has_range = marker.reference_range_lower is not None and marker.reference_range_upper is not None

        if not has_range:
            educational_context = (
                f"{marker.test_name} is currently recorded with observed value {marker.observed_value} {marker.unit}. "
                "Because an explicit laboratory reference range was not identified on this document, this parameter cannot "
                "be categorized as high or low. Different clinical laboratories calibrate assays using distinct analytical platforms."
            )
        elif marker.status == "elevated":
            educational_context = (
                f"Your observed {marker.test_name} value ({marker.observed_value} {marker.unit}) is higher than this laboratory's "
                f"normal interval ({marker.reference_range_text}). In reproductive and metabolic health, elevated values are often "
                "reviewed alongside menstrual cycle timing, ultrasound imaging, and physical symptoms. An isolated high value does "
                "not constitute a diagnosis."
            )
        elif marker.status == "low":
            educational_context = (
                f"Your observed {marker.test_name} value ({marker.observed_value} {marker.unit}) is below the laboratory's reference range "
                f"({marker.reference_range_text}). Low levels may reflect suppression or variation based on the menstrual cycle phase. "
                "Discuss this with your doctor during your consultation."
            )
        else:
            educational_context = (
                f"Your observed {marker.test_name} value ({marker.observed_value} {marker.unit}) is within this laboratory's reference range "
                f"({marker.reference_range_text}). Balanced levels indicate standard biochemical range for this specific test."
            )

        questions = [
            f"How does my {marker.test_name} result relate to my overall cycle symptoms?",
            "Was this blood test taken during a specific phase of my menstrual cycle?",
            "Are follow-up metabolic tests (like fasting glucose or lipid panel) recommended?"
        ]

        return {
            "biomarker_id": marker.id,
            "test_name": marker.test_name,
            "observed_value": marker.observed_value,
            "status": marker.status,
            "explanation": educational_context,
            "suggested_questions": questions,
            "safety_disclaimer": "Laboratory tests must be clinically interpreted by a qualified doctor in combination with your medical history."
        }


biomarker_service = BiomarkerService()
