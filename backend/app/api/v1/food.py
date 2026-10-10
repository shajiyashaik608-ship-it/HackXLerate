import sys, os
from fastapi import APIRouter
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ai-ml")))
from food_recommender import FoodRecommender

from app.schemas.food import MealSuggestionResponse
from app.utils.safety_guardrails import STANDARD_DISCLAIMER_EN

router = APIRouter(prefix="/food", tags=["Indian PCOS Nutrition"])

@router.get("/recommendations", response_model=MealSuggestionResponse)
def get_pcos_meal_recommendations(
    diet_type: str = "vegetarian",
    meal_type: Optional[str] = None,
    budget_friendly: bool = False
):
    meals = FoodRecommender.get_recommendations(
        diet_type=diet_type,
        meal_type=meal_type,
        budget_friendly_only=budget_friendly
    )
    lifestyle_note = FoodRecommender.get_lifestyle_guidance()
    
    return {
        "recommendations": meals,
        "lifestyle_note": lifestyle_note,
        "disclaimer": STANDARD_DISCLAIMER_EN
    }
