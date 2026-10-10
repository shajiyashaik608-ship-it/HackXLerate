from fastapi import APIRouter, Depends, status
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.nutrition_service import nutrition_service
from app.schemas.meal import (
    MealItemResponse,
    MealPlanCreate,
    MealPlanUpdate,
    MealPlanResponse,
    NutritionRecommendationResponse,
)

router = APIRouter(prefix="/nutrition", tags=["Indian Nutrition"])


@router.get("/meals", response_model=List[MealItemResponse])
def list_meals(
    category: Optional[str] = None,
    diet_type: Optional[str] = None,
    is_budget_friendly: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return nutrition_service.get_meals(
        db=db,
        category=category,
        diet_type=diet_type,
        is_budget_friendly=is_budget_friendly,
        search=search,
        limit=limit
    )


@router.get("/meals/{meal_id}", response_model=MealItemResponse)
def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return nutrition_service.get_meal_by_id(db, meal_id=meal_id)


@router.get("/recommend", response_model=NutritionRecommendationResponse)
def recommend_meals(
    diet_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return nutrition_service.get_recommendations(
        db=db, user_id=current_user.id, diet_type_override=diet_type
    )


@router.get("/plan", response_model=Optional[MealPlanResponse])
def get_meal_plan(
    plan_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_date = plan_date or date.today()
    return nutrition_service.get_or_create_meal_plan(db, user_id=current_user.id, plan_date=target_date)


@router.post("/plan", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
def save_meal_plan(
    payload: MealPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items_dicts = [itm.model_dump() for itm in payload.items]
    return nutrition_service.save_meal_plan(
        db=db,
        user_id=current_user.id,
        plan_date=payload.plan_date,
        items_data=items_dicts
    )


@router.patch("/plan/{plan_id}", response_model=MealPlanResponse)
def update_meal_plan(
    plan_id: int,
    payload: MealPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items_dicts = [itm.model_dump() for itm in payload.items] if payload.items else []
    return nutrition_service.save_meal_plan(
        db=db,
        user_id=current_user.id,
        plan_date=payload.plan_date or date.today(),
        items_data=items_dicts
    )


@router.delete("/plan/{plan_id}")
def delete_meal_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    nutrition_service.delete_meal_plan(db, plan_id=plan_id, user_id=current_user.id)
    return {"message": "Meal plan deleted successfully."}
