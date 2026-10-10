import json
from pathlib import Path
from datetime import date
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.meal import MealItem, MealPlan, MealPlanItem
from app.repositories.nutrition_repo import meal_item_repo, meal_plan_repo
from app.repositories.user_repo import user_repo
from app.core.exceptions import NotFoundException, ValidationException
from app.core.logging import logger

KNOWLEDGE_FILE = Path(__file__).resolve().parent.parent.parent / "knowledge" / "indian_food_database.json"


class NutritionService:
    def ensure_default_meals_seeded(self, db: Session):
        """Loads default Indian PCOS meals from knowledge base if database table is empty."""
        count = len(meal_item_repo.get_multi(db, limit=1))
        if count == 0 and KNOWLEDGE_FILE.exists():
            try:
                data = json.loads(KNOWLEDGE_FILE.read_text(encoding="utf-8"))
                for item_dict in data:
                    item = MealItem(
                        name=item_dict["name"],
                        category=item_dict["category"],
                        diet_type=item_dict["diet_type"],
                        is_budget_friendly=item_dict.get("is_budget_friendly", True),
                        serving_size=item_dict.get("serving_size", "1 serving"),
                        approx_calories=item_dict.get("approx_calories"),
                        protein_grams=item_dict.get("protein_grams"),
                        fibre_grams=item_dict.get("fibre_grams"),
                        ingredients=item_dict.get("ingredients"),
                        nutrition_source=item_dict.get("nutrition_source", "ICMR-NIN"),
                        pcos_benefits=item_dict.get("pcos_benefits")
                    )
                    db.add(item)
                db.commit()
                logger.info(f"Seeded {len(data)} default Indian meals into database.")
            except Exception as e:
                logger.error(f"Error seeding meals from JSON: {e}")

    def get_meals(
        self,
        db: Session,
        category: Optional[str] = None,
        diet_type: Optional[str] = None,
        is_budget_friendly: Optional[bool] = None,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[MealItem]:
        self.ensure_default_meals_seeded(db)
        return meal_item_repo.search_meals(
            db,
            category=category,
            diet_type=diet_type,
            is_budget_friendly=is_budget_friendly,
            search_term=search,
            limit=limit
        )

    def get_meal_by_id(self, db: Session, meal_id: int) -> MealItem:
        self.ensure_default_meals_seeded(db)
        meal = meal_item_repo.get_by_id(db, meal_id)
        if not meal:
            raise NotFoundException("Meal item not found.")
        return meal

    def get_recommendations(
        self,
        db: Session,
        user_id: int,
        diet_type_override: Optional[str] = None
    ) -> Dict[str, Any]:
        self.ensure_default_meals_seeded(db)
        profile = user_repo.get_profile_by_user_id(db, user_id)
        diet_type = diet_type_override or (profile.diet_type if profile else "veg")

        all_meals = meal_item_repo.get_multi(db, limit=100)

        def matches_diet(item: MealItem) -> bool:
            if diet_type == "veg":
                return item.diet_type == "veg"
            elif diet_type == "egg":
                return item.diet_type in ["veg", "egg"]
            return True  # non-veg covers all

        breakfast = [m for m in all_meals if m.category == "breakfast" and matches_diet(m)]
        lunch = [m for m in all_meals if m.category == "lunch" and matches_diet(m)]
        dinner = [m for m in all_meals if m.category == "dinner" and matches_diet(m)]
        snacks = [m for m in all_meals if m.category == "snack" and matches_diet(m)]

        return {
            "diet_type": diet_type,
            "target_focus": "Insulin Sensitivity & Sustained Satiety",
            "breakfast": breakfast[:4],
            "lunch": lunch[:4],
            "dinner": dinner[:4],
            "snacks": snacks[:4],
            "educational_guidance": (
                "Pair complex carbohydrates (ragi, korralu, whole moong) with adequate dietary protein "
                "and healthy fats (methi, flaxseeds, nuts) to promote stable blood glucose curves throughout the day."
            )
        }

    def get_or_create_meal_plan(self, db: Session, user_id: int, plan_date: date) -> Optional[MealPlan]:
        return meal_plan_repo.get_by_user_and_date(db, user_id=user_id, plan_date=plan_date)

    def save_meal_plan(
        self,
        db: Session,
        user_id: int,
        plan_date: date,
        items_data: List[dict]
    ) -> MealPlan:
        existing = meal_plan_repo.get_by_user_and_date(db, user_id=user_id, plan_date=plan_date)
        if existing:
            # Clear old items to replace with updated list
            for itm in existing.items:
                db.delete(itm)
            db.commit()
            plan = existing
        else:
            plan = MealPlan(user_id=user_id, plan_date=plan_date)
            db.add(plan)
            db.commit()
            db.refresh(plan)

        for itm in items_data:
            meal_item_id = itm.get("meal_item_id")
            slot = itm.get("meal_slot", "breakfast")
            servings = itm.get("servings", 1.0)

            # verify meal item exists
            meal_obj = meal_item_repo.get_by_id(db, meal_item_id)
            if meal_obj:
                plan_item = MealPlanItem(
                    meal_plan_id=plan.id,
                    meal_item_id=meal_item_id,
                    meal_slot=slot,
                    servings=servings
                )
                db.add(plan_item)

        db.commit()
        db.refresh(plan)
        return plan

    def delete_meal_plan(self, db: Session, plan_id: int, user_id: int) -> bool:
        plan = meal_plan_repo.get_by_id(db, plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundException("Meal plan not found.")
        return meal_plan_repo.delete(db, plan_id)


nutrition_service = NutritionService()
