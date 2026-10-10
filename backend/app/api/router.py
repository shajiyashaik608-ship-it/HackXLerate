from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.services.consultation_service import consultation_service
from app.services.nutrition_service import nutrition_service

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.profile import router as profile_router
from app.api.v1.reports import router as reports_router
from app.api.v1.biomarkers import router as biomarkers_router
from app.api.v1.assistant import router as assistant_router
from app.api.v1.cycles import router as cycles_router
from app.api.v1.symptoms import router as symptoms_router
from app.api.v1.nutrition import router as nutrition_router
from app.api.v1.reminders import router as reminders_router
from app.api.v1.consultations import router as consultations_router
from app.api.v1.timeline import router as timeline_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.community import router as community_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.privacy import router as privacy_router

api_router = APIRouter(prefix="/api/v1")

# Mount official v1 domain modules
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(profile_router)
api_router.include_router(reports_router)
api_router.include_router(biomarkers_router)
api_router.include_router(assistant_router)
api_router.include_router(cycles_router)
api_router.include_router(symptoms_router)
api_router.include_router(nutrition_router)
api_router.include_router(reminders_router)
api_router.include_router(consultations_router)
api_router.include_router(timeline_router)
api_router.include_router(dashboard_router)
api_router.include_router(community_router)
api_router.include_router(notifications_router)
api_router.include_router(privacy_router)

# Compatibility Routers for existing React Frontend
compat_router = APIRouter(tags=["Frontend Compatibility"])


@compat_router.get("/doctor-prep/summary")
def get_compat_doctor_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brief = consultation_service.generate_brief(db, user_id=current_user.id)
    return {
        "patient_overview": f"{brief.patient_name or current_user.full_name or 'Patient'}, {brief.patient_age or 26} years old",
        "chief_concerns": brief.primary_concerns or "Menstrual cycle regularity and metabolic wellness tracking.",
        "menstrual_history": brief.recent_cycle_info or "Cycle regularity tracking active.",
        "pertinent_lab_findings": brief.lab_flags_summary.split("; ") if brief.lab_flags_summary else [],
        "active_medications": brief.active_medications or [],
        "recommended_questions_to_ask": brief.prioritized_questions.split("\n") if brief.prioritized_questions else [],
        "clinical_disclaimer": "Prepared by Health Saathi to facilitate patient-clinician communication. Not an automated diagnosis."
    }


@compat_router.get("/food/recommendations")
def get_compat_food_recommendations(
    diet_type: str = "vegetarian",
    meal_type: Optional[str] = None,
    budget_friendly: bool = False,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    norm_diet = "veg" if "veg" in diet_type else ("egg" if "egg" in diet_type else "non-veg")
    # If user is authenticated, personalize using their profile; otherwise use generalized diet recommendation without touching user 1
    recs = nutrition_service.get_recommendations(
        db, user_id=current_user.id if current_user else 0, diet_type_override=norm_diet
    )
    flat_meals = []
    for slot in ["breakfast", "lunch", "dinner", "snacks"]:
        for m in recs.get(slot, []):
            if meal_type and m.category != meal_type:
                continue
            if budget_friendly and not m.is_budget_friendly:
                continue
            flat_meals.append({
                "dish_name": m.name,
                "meal_type": m.category,
                "diet_type": m.diet_type,
                "ingredients": m.ingredients.split(", ") if m.ingredients else [],
                "why_it_works_for_pcos": m.pcos_benefits or "Supports low glycemic load and satiety.",
                "protein_grams": m.protein_grams or 10,
                "fibre_grams": m.fibre_grams or 6,
                "glycemic_index": "low",
                "budget_friendly": m.is_budget_friendly
            })
    return {
        "recommendations": flat_meals,
        "lifestyle_note": recs.get("educational_guidance", "Pair carbohydrates with protein to avoid rapid glucose surges.")
    }



api_router.include_router(compat_router)
