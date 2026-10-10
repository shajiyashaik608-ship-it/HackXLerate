from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.meal import MealItem, MealPlan, MealPlanItem


class MealItemRepository(BaseRepository[MealItem]):
    def __init__(self):
        super().__init__(MealItem)

    def search_meals(
        self,
        db: Session,
        category: Optional[str] = None,
        diet_type: Optional[str] = None,
        is_budget_friendly: Optional[bool] = None,
        search_term: Optional[str] = None,
        limit: int = 50
    ) -> List[MealItem]:
        stmt = select(MealItem)
        if category:
            stmt = stmt.where(MealItem.category.ilike(category))
        if diet_type:
            stmt = stmt.where(MealItem.diet_type.ilike(diet_type))
        if is_budget_friendly is not None:
            stmt = stmt.where(MealItem.is_budget_friendly == is_budget_friendly)
        if search_term:
            stmt = stmt.where(
                MealItem.name.ilike(f"%{search_term}%") | 
                MealItem.ingredients.ilike(f"%{search_term}%")
            )
        stmt = stmt.limit(limit)
        return list(db.scalars(stmt).all())


class MealPlanRepository(BaseRepository[MealPlan]):
    def __init__(self):
        super().__init__(MealPlan)

    def get_by_user_and_date(self, db: Session, user_id: int, plan_date: date) -> Optional[MealPlan]:
        stmt = (
            select(MealPlan)
            .options(joinedload(MealPlan.items).joinedload(MealPlanItem.meal_item))
            .where(MealPlan.user_id == user_id, MealPlan.plan_date == plan_date)
        )
        return db.scalars(stmt).first()

    def get_latest_by_user(self, db: Session, user_id: int) -> Optional[MealPlan]:
        stmt = (
            select(MealPlan)
            .options(joinedload(MealPlan.items).joinedload(MealPlanItem.meal_item))
            .where(MealPlan.user_id == user_id)
            .order_by(desc(MealPlan.plan_date))
        )
        return db.scalars(stmt).first()


meal_item_repo = MealItemRepository()
meal_plan_repo = MealPlanRepository()
