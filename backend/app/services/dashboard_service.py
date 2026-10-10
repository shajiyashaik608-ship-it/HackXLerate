from datetime import date
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.repositories.document_repo import document_repo, biomarker_repo
from app.repositories.cycle_repo import cycle_repo, symptom_repo
from app.repositories.reminder_repo import reminder_repo
from app.repositories.nutrition_repo import meal_plan_repo
from app.services.cycle_service import cycle_service
from app.utils.guardrails import check_urgent_symptoms


class DashboardService:
    def get_summary(self, db: Session, user_id: int) -> Dict[str, Any]:
        user = user_repo.get_by_id(db, user_id)
        user_name = user.full_name if user else "Friend"

        # 1. Documents & Biomarkers
        reports = document_repo.get_by_user(db, user_id=user_id, limit=3)
        biomarkers = biomarker_repo.get_by_user(db, user_id=user_id, limit=10)
        flagged_count = sum(1 for b in biomarkers if b.status in ["elevated", "low"])

        # 2. Cycles & Symptoms
        cycle_estimate = cycle_service.estimate_cycle(db, user_id=user_id)
        cycles = cycle_repo.get_by_user(db, user_id=user_id, limit=1)
        last_cycle = cycles[0] if cycles else None

        recent_symptoms = symptom_repo.get_by_user(db, user_id=user_id, limit=4)
        urgent_flag = False
        for s in recent_symptoms:
            if s.severity == "severe" or s.notes:
                is_urgent, _ = check_urgent_symptoms(f"{s.symptom_type} {s.notes or ''}")
                if is_urgent:
                    urgent_flag = True

        # 3. Active Reminders
        active_reminders = reminder_repo.get_active_by_user(db, user_id=user_id)

        # 4. Today's Meal Plan
        today = date.today()
        todays_plan = meal_plan_repo.get_by_user_and_date(db, user_id=user_id, plan_date=today)

        # 5. Personalized Insight
        insight = "Maintaining steady low-GI meals and 20 minutes of restorative movement supports metabolic balance."
        if flagged_count > 0:
            insight = f"You have {flagged_count} lab parameters marked for clinical review. Consider preparing your doctor brief."

        return {
            "user_name": user_name,
            "recent_reports": reports,
            "reviewed_biomarkers": biomarkers[:5],
            "flagged_biomarkers_count": flagged_count,
            "cycle_status": cycle_estimate,
            "last_cycle": last_cycle,
            "recent_symptoms": recent_symptoms,
            "active_reminders": active_reminders,
            "todays_meal_plan": todays_plan,
            "health_score_insight": insight,
            "urgent_warning_present": urgent_flag
        }


dashboard_service = DashboardService()
