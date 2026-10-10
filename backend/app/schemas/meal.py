from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class MealItemBase(BaseModel):
    name: str
    category: str = Field(..., description="breakfast, lunch, dinner, snack")
    diet_type: str = Field(default="veg", description="veg, egg, non-veg")
    is_budget_friendly: bool = True
    serving_size: str = "1 bowl / 2 pcs"
    approx_calories: Optional[int] = None
    protein_grams: Optional[float] = None
    fibre_grams: Optional[float] = None
    ingredients: Optional[str] = None
    nutrition_source: str = "NIN / ICMR Dietary Guidelines for Indians"
    pcos_benefits: Optional[str] = None


class MealItemCreate(MealItemBase):
    pass


class MealItemResponse(MealItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MealPlanItemBase(BaseModel):
    meal_item_id: int
    meal_slot: str = "breakfast"  # breakfast, lunch, dinner, snack
    servings: float = 1.0


class MealPlanItemCreate(MealPlanItemBase):
    pass


class MealPlanItemResponse(MealPlanItemBase):
    id: int
    meal_plan_id: int
    meal_item: Optional[MealItemResponse] = None

    model_config = ConfigDict(from_attributes=True)


class MealPlanCreate(BaseModel):
    plan_date: date = Field(default_factory=date.today)
    items: List[MealPlanItemCreate] = []


class MealPlanUpdate(BaseModel):
    plan_date: Optional[date] = None
    items: Optional[List[MealPlanItemCreate]] = None


class MealPlanResponse(BaseModel):
    id: int
    user_id: int
    plan_date: date
    created_at: datetime
    items: List[MealPlanItemResponse] = []
    total_calories: Optional[int] = None
    total_protein_grams: Optional[float] = None
    total_fibre_grams: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class NutritionRecommendationResponse(BaseModel):
    diet_type: str
    target_focus: str = "Insulin Resistance & Satiety"
    breakfast: List[MealItemResponse] = []
    lunch: List[MealItemResponse] = []
    dinner: List[MealItemResponse] = []
    snacks: List[MealItemResponse] = []
    educational_guidance: str = "Emphasize low glycemic index grains (ragi, foxtail millet, whole legumes) paired with ample dietary fibre and plant protein."
