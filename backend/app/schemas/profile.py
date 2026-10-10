from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProfileCreate(BaseModel):
    age: Optional[int] = Field(default=None, ge=10, le=100)
    diet_type: str = Field(default="vegetarian")  # vegetarian, egg, non_vegetarian
    baseline_cycle_length: Optional[int] = Field(default=33, ge=20, le=90)
    period_duration: Optional[int] = Field(default=4, ge=1, le=15)
    wellness_goals: Optional[str] = None
    allergies: Optional[str] = "None"
    preferred_language: str = "en"
    timezone: str = "Asia/Kolkata"


class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    diet_type: Optional[str] = None
    baseline_cycle_length: Optional[int] = None
    period_duration: Optional[int] = None
    wellness_goals: Optional[str] = None
    allergies: Optional[str] = None
    preferred_language: Optional[str] = None
    timezone: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int] = None
    diet_type: str
    baseline_cycle_length: Optional[int] = None
    period_duration: Optional[int] = None
    wellness_goals: Optional[str] = None
    allergies: Optional[str] = None
    preferred_language: str
    timezone: str

    model_config = ConfigDict(from_attributes=True)


HealthProfileCreate = ProfileCreate
HealthProfileUpdate = ProfileUpdate
HealthProfileResponse = ProfileResponse
