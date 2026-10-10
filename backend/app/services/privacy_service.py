from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.repositories.user_repo import user_repo
from app.repositories.document_repo import document_repo, biomarker_repo
from app.repositories.cycle_repo import cycle_repo, symptom_repo
from app.repositories.reminder_repo import reminder_repo
from app.repositories.nutrition_repo import meal_plan_repo
from app.repositories.consultation_repo import consultation_repo
from app.repositories.chat_repo import chat_repo
from app.integrations.storage_provider import storage_provider
from app.models.user import User
from app.models.profile import HealthProfile
from app.models.document import MedicalDocument
from app.models.biomarker import Biomarker
from app.models.cycle import CycleRecord
from app.models.symptom import SymptomRecord
from app.models.reminder import CareReminder, ReminderCompletion
from app.models.meal import MealPlan, MealPlanItem
from app.models.consultation import ConsultationBrief
from app.models.chat import Conversation, ChatMessage
from app.models.notification import Notification
from app.core.exceptions import ValidationException


class PrivacyService:
    def export_user_data(self, db: Session, user_id: int) -> Dict[str, Any]:
        user = user_repo.get_by_id(db, user_id)
        profile = user_repo.get_profile_by_user_id(db, user_id)
        docs = document_repo.get_by_user(db, user_id=user_id, limit=500)
        biomarkers = biomarker_repo.get_by_user(db, user_id=user_id, limit=500)
        cycles = cycle_repo.get_by_user(db, user_id=user_id, limit=500)
        symptoms = symptom_repo.get_by_user(db, user_id=user_id, limit=500)
        reminders = reminder_repo.get_by_user(db, user_id=user_id)
        briefs = consultation_repo.get_by_user(db, user_id=user_id, limit=500)
        convs = chat_repo.get_by_user(db, user_id=user_id)

        return {
            "export_version": "1.0",
            "exported_at": datetime.utcnow(),
            "user_info": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at.isoformat() if user.created_at else None
            },
            "health_profile": {
                "age": profile.age if profile else None,
                "diet_type": profile.diet_type if profile else None,
                "baseline_cycle_length": profile.baseline_cycle_length if profile else None,
                "preferred_language": profile.preferred_language if profile else None
            } if profile else None,
            "medical_documents": [
                {"id": d.id, "file_name": d.file_name, "category": d.category, "upload_date": d.upload_date.isoformat()}
                for d in docs
            ],
            "biomarkers": [
                {
                    "test_name": b.test_name,
                    "observed_value": b.observed_value,
                    "unit": b.unit,
                    "status": b.status,
                    "reference_range": b.reference_range_text,
                    "test_date": b.test_date.isoformat() if b.test_date else None
                }
                for b in biomarkers
            ],
            "cycle_records": [
                {
                    "start_date": c.start_date.isoformat(),
                    "end_date": c.end_date.isoformat() if c.end_date else None,
                    "flow_intensity": c.flow_intensity,
                    "notes": c.notes
                }
                for c in cycles
            ],
            "symptom_records": [
                {
                    "recorded_date": s.recorded_date.isoformat(),
                    "symptom_type": s.symptom_type,
                    "severity": s.severity,
                    "notes": s.notes
                }
                for s in symptoms
            ],
            "reminders": [
                {"title": r.title, "category": r.category, "scheduled_time": r.scheduled_time, "recurrence": r.recurrence}
                for r in reminders
            ],
            "meal_plans": [],
            "consultations": [
                {"id": cb.id, "primary_concerns": cb.primary_concerns, "created_at": cb.created_at.isoformat()}
                for cb in briefs
            ],
            "conversations": [
                {"id": cv.id, "language": cv.language, "message_count": len(cv.messages)}
                for cv in convs
            ],
            "data_retention_notice": "Health Saathi does not share medical data with external AI providers without consent."
        }

    def purge_user_data(self, db: Session, user_id: int, confirm_phrase: str) -> Dict[str, Any]:
        if confirm_phrase.strip() != "DELETE MY HEALTH DATA":
            raise ValidationException("Confirmation phrase must exactly match 'DELETE MY HEALTH DATA'.")

        counts: Dict[str, int] = {}

        # 1. Purge physical private files
        files_removed = storage_provider.purge_user_files(user_id)
        counts["physical_files"] = files_removed

        # 2. Delete database records in dependency order
        counts["biomarkers"] = db.query(Biomarker).filter(Biomarker.user_id == user_id).delete()
        counts["medical_documents"] = db.query(MedicalDocument).filter(MedicalDocument.user_id == user_id).delete()
        counts["cycle_records"] = db.query(CycleRecord).filter(CycleRecord.user_id == user_id).delete()
        counts["symptom_records"] = db.query(SymptomRecord).filter(SymptomRecord.user_id == user_id).delete()
        
        # Reminders and completions
        user_reminders = reminder_repo.get_by_user(db, user_id)
        rem_ids = [r.id for r in user_reminders]
        if rem_ids:
            counts["reminder_completions"] = db.query(ReminderCompletion).filter(ReminderCompletion.reminder_id.in_(rem_ids)).delete(synchronize_session=False)
        counts["reminders"] = db.query(CareReminder).filter(CareReminder.user_id == user_id).delete()

        # Meal plans
        user_plans = db.query(MealPlan).filter(MealPlan.user_id == user_id).all()
        plan_ids = [p.id for p in user_plans]
        if plan_ids:
            counts["meal_plan_items"] = db.query(MealPlanItem).filter(MealPlanItem.meal_plan_id.in_(plan_ids)).delete(synchronize_session=False)
        counts["meal_plans"] = db.query(MealPlan).filter(MealPlan.user_id == user_id).delete()

        # Consultations
        counts["consultations"] = db.query(ConsultationBrief).filter(ConsultationBrief.user_id == user_id).delete()

        # Chat
        user_convs = db.query(Conversation).filter(Conversation.user_id == user_id).all()
        conv_ids = [c.id for c in user_convs]
        if conv_ids:
            counts["chat_messages"] = db.query(ChatMessage).filter(ChatMessage.conversation_id.in_(conv_ids)).delete(synchronize_session=False)
        counts["conversations"] = db.query(Conversation).filter(Conversation.user_id == user_id).delete()

        # Notifications
        counts["notifications"] = db.query(Notification).filter(Notification.user_id == user_id).delete()

        # Profile & User account
        counts["profile"] = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).delete()
        counts["user"] = db.query(User).filter(User.id == user_id).delete()

        db.commit()

        return {
            "status": "completed",
            "message": "All personal health records, cycle entries, uploaded reports, and account data have been permanently deleted.",
            "records_deleted": counts,
            "purged_at": datetime.utcnow()
        }


privacy_service = PrivacyService()
