from datetime import datetime, date
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories.document_repo import document_repo, biomarker_repo
from app.repositories.cycle_repo import cycle_repo, symptom_repo
from app.repositories.reminder_repo import reminder_repo
from app.repositories.nutrition_repo import meal_plan_repo


class TimelineService:
    def get_timeline_events(
        self,
        db: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        events: List[Dict[str, Any]] = []

        # 1. Document uploads
        docs = document_repo.get_by_user(db, user_id=user_id, limit=30)
        for d in docs:
            events.append({
                "id": f"doc_{d.id}",
                "event_type": "report_upload",
                "title": f"Medical Report Uploaded: {d.file_name}",
                "description": f"Status: {d.processing_status}. Extracted {len(d.biomarkers)} parameters.",
                "timestamp": d.upload_date,
                "category": "medical",
                "metadata": {"document_id": d.id, "status": d.processing_status}
            })

        # 2. Flagged Biomarkers
        biomarkers = biomarker_repo.get_by_user(db, user_id=user_id, limit=50)
        for b in biomarkers:
            if b.status in ["elevated", "low"]:
                dt = datetime.combine(b.test_date, datetime.min.time()) if b.test_date else b.created_at
                events.append({
                    "id": f"bio_{b.id}",
                    "event_type": "biomarker_flag",
                    "title": f"Lab Parameter Flagged: {b.test_name}",
                    "description": f"Observed: {b.observed_value} {b.unit} ({b.status.upper()}). Ref: {b.reference_range_text or 'N/A'}",
                    "timestamp": dt or datetime.utcnow(),
                    "category": "medical",
                    "metadata": {"biomarker_id": b.id, "status": b.status}
                })

        # 3. Menstrual Cycles
        cycles = cycle_repo.get_by_user(db, user_id=user_id, limit=20)
        for c in cycles:
            dt = datetime.combine(c.start_date, datetime.min.time())
            events.append({
                "id": f"cycle_{c.id}",
                "event_type": "cycle_start",
                "title": f"Menstrual Cycle Began",
                "description": f"Recorded flow intensity: {c.flow_intensity}. Duration: {c.duration_days or 4} days.",
                "timestamp": dt,
                "category": "cycle",
                "metadata": {"cycle_id": c.id, "flow": c.flow_intensity}
            })

        # 4. Symptoms
        symptoms = symptom_repo.get_by_user(db, user_id=user_id, limit=30)
        for s in symptoms:
            dt = datetime.combine(s.recorded_date, datetime.min.time())
            events.append({
                "id": f"symp_{s.id}",
                "event_type": "symptom_entry",
                "title": f"Symptom Noted: {s.symptom_type.title()}",
                "description": f"Severity: {s.severity}. {s.notes or ''}".strip(),
                "timestamp": dt,
                "category": "symptom",
                "metadata": {"symptom_id": s.id, "severity": s.severity}
            })

        # Sort all chronologically descending
        events.sort(key=lambda e: e["timestamp"], reverse=True)

        total_events = len(events)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_events = events[start_idx:end_idx]

        return {
            "total_events": total_events,
            "events": paginated_events,
            "page": page,
            "page_size": page_size
        }


timeline_service = TimelineService()
