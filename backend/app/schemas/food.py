from pydantic import BaseModel
from typing import Optional, List

class MealItem(BaseModel):
    dish_name: str
    meal_type: str  # breakfast, lunch, snack, dinner
    ingredients: List[str]
    why_it_works_for_pcos: str
    protein_grams: int
    fibre_grams: int
    glycemic_index: str  # low, medium
    budget_friendly: bool
    diet_type: str  # vegetarian, non_vegetarian, eggitarian

class MealSuggestionRequest(BaseModel):
    diet_type: Optional[str] = "vegetarian"
    budget_tier: Optional[str] = "budget_friendly"
    meal_type: Optional[str] = None  # breakfast, lunch, dinner, snack

class MealSuggestionResponse(BaseModel):
    recommendations: List[MealItem]
    lifestyle_note: str
    disclaimer: str
