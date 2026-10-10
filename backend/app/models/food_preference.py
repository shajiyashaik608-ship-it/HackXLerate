from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.database import Base

class FoodPreference(Base):
    __tablename__ = "food_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    diet_type = Column(String, default="vegetarian")  # vegetarian, non_vegetarian, eggitarian, jain
    budget_tier = Column(String, default="budget_friendly")  # budget_friendly, everyday, premium
    allergies = Column(JSON, default=list)  # ["dairy", "gluten", "nuts"]
    regional_preference = Column(String, default="south_indian")  # south_indian, north_indian
