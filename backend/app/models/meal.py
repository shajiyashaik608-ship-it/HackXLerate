from datetime import date
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class MealItem(Base, TimestampMixin):
    __tablename__ = "meal_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # breakfast, lunch, dinner, snack
    diet_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # vegetarian, egg, non_vegetarian
    is_budget_friendly: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    serving_size: Mapped[str] = mapped_column(String(100), default="1 plate / 2 pieces", nullable=False)
    approx_calories: Mapped[int] = mapped_column(Integer, default=250, nullable=False)
    protein_grams: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)
    fibre_grams: Mapped[float] = mapped_column(Float, default=6.0, nullable=False)
    
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)  # JSON or comma-separated
    nutrition_source: Mapped[str] = mapped_column(String(150), default="NIN / ICMR Dietary Guidelines", nullable=False)
    pcos_benefits: Mapped[str] = mapped_column(Text, nullable=False)  # Educational explanation of low-GI and satiety


class MealPlan(Base, TimestampMixin):
    __tablename__ = "meal_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    plan_date: Mapped[date] = mapped_column(Date, default=date.today, index=True, nullable=False)

    items: Mapped[List["MealPlanItem"]] = relationship("MealPlanItem", back_populates="plan", cascade="all, delete-orphan")


class MealPlanItem(Base):
    __tablename__ = "meal_plan_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    meal_plan_id: Mapped[int] = mapped_column(ForeignKey("meal_plans.id", ondelete="CASCADE"), index=True, nullable=False)
    meal_item_id: Mapped[int] = mapped_column(ForeignKey("meal_items.id", ondelete="CASCADE"), index=True, nullable=False)
    meal_slot: Mapped[str] = mapped_column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    servings: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    plan: Mapped["MealPlan"] = relationship("MealPlan", back_populates="items")
    meal_item: Mapped["MealItem"] = relationship("MealItem")
    meal: Mapped["MealItem"] = relationship("MealItem", viewonly=True)

