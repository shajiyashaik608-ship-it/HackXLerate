from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.consultation import ConsultationBrief
from app.repositories.consultation_repo import consultation_repo
from app.repositories.user_repo import user_repo
from app.repositories.cycle_repo import cycle_repo, symptom_repo
from app.repositories.document_repo import biomarker_repo
from app.repositories.reminder_repo import reminder_repo
from app.core.exceptions import NotFoundException


class ConsultationService:
    def generate_brief(
        self,
        db: Session,
        user_id: int,
        primary_concerns: Optional[str] = None,
        symptoms_summary: Optional[str] = None,
        lab_flags_summary: Optional[str] = None,
        prioritized_questions: Optional[str] = None,
        include_active_reminders: bool = True,
        include_recent_cycles: bool = True
    ) -> ConsultationBrief:
        user = user_repo.get_by_id(db, user_id)
        profile = user_repo.get_profile_by_user_id(db, user_id)

        # 1. Gather menstrual history
        cycles = cycle_repo.get_by_user(db, user_id=user_id, limit=5)
        if cycles:
            latest = cycles[0]
            cycle_desc = f"{len(cycles)} cycles tracked. Most recent began {latest.start_date.strftime('%b %d, %Y')} ({latest.flow_intensity} flow)."
        else:
            cycle_desc = "No recent cycle logs recorded."

        # 2. Gather symptoms
        if not symptoms_summary:
            symptoms = symptom_repo.get_by_user(db, user_id=user_id, limit=10)
            if symptoms:
                s_types = list(set([f"{s.symptom_type} ({s.severity})" for s in symptoms]))
                symptoms_summary = ", ".join(s_types)
            else:
                symptoms_summary = "Menstrual cycle irregularity and metabolic wellness tracking."

        # 3. Gather flagged labs
        if not lab_flags_summary:
            biomarkers = biomarker_repo.get_by_user(db, user_id=user_id, limit=20)
            flagged = [b for b in biomarkers if b.status in ["elevated", "low", "needs_review"]]
            if flagged:
                lab_flags_summary = "; ".join([
                    f"{b.test_name}: {b.observed_value} {b.unit} ({b.status.upper()}, Ref: {b.reference_range_text or 'Unspecified'})"
                    for b in flagged
                ])
            else:
                lab_flags_summary = "No flagged laboratory abnormalities detected in uploaded reports."

        # 4. Gather active medications
        med_reminders = reminder_repo.get_active_by_user(db, user_id=user_id)
        active_meds = [r.title for r in med_reminders if r.category == "medication"]

        # 5. Prioritized questions
        if not prioritized_questions:
            questions = [
                "1. Given my recent cycle interval and symptoms, what targeted evaluation do you recommend?",
                "2. Do my observed lab values (e.g. fasting insulin / thyroid) warrant medication or continued lifestyle therapy?",
                "3. What specific red flags should prompt me to contact your clinic before our next visit?"
            ]
            prioritized_questions = "\n".join(questions)

        if not primary_concerns:
            primary_concerns = "Review menstrual cycle variability, metabolic lab findings, and discuss individualized care plan."

        brief = ConsultationBrief(
            user_id=user_id,
            primary_concerns=primary_concerns,
            symptoms_summary=symptoms_summary,
            lab_flags_summary=lab_flags_summary,
            prioritized_questions=prioritized_questions
        )
        saved = consultation_repo.create(db, brief)

        # Attach dynamic fields for frontend printable representation
        saved.patient_name = user.full_name if user else "Patient"
        saved.patient_age = profile.age if profile else None
        saved.recent_cycle_info = cycle_desc
        saved.active_medications = active_meds

        return saved

    def get_user_briefs(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[ConsultationBrief]:
        return consultation_repo.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

    def get_brief_by_id(self, db: Session, brief_id: int, user_id: int) -> ConsultationBrief:
        brief = consultation_repo.get_by_id_and_user(db, brief_id=brief_id, user_id=user_id)
        if not brief:
            raise NotFoundException("Consultation brief not found.")

        user = user_repo.get_by_id(db, user_id)
        profile = user_repo.get_profile_by_user_id(db, user_id)
        med_reminders = reminder_repo.get_active_by_user(db, user_id=user_id)

        brief.patient_name = user.full_name if user else "Patient"
        brief.patient_age = profile.age if profile else None
        brief.active_medications = [r.title for r in med_reminders if r.category == "medication"]
        return brief

    def update_brief(self, db: Session, brief_id: int, user_id: int, update_data: dict) -> ConsultationBrief:
        brief = self.get_brief_by_id(db, brief_id=brief_id, user_id=user_id)
        return consultation_repo.update(db, brief, update_data)

    def delete_brief(self, db: Session, brief_id: int, user_id: int) -> bool:
        brief = self.get_brief_by_id(db, brief_id=brief_id, user_id=user_id)
        return consultation_repo.delete(db, brief.id)


consultation_service = ConsultationService()
