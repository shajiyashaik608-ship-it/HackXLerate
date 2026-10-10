from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ReminderCompletionBase(BaseModel):
    scheduled_occurrence: datetime
    is_completed: bool = True
    completed_at: Optional[datetime] = None
    snoozed_until: Optional[datetime] = None


class ReminderCompletionResponse(ReminderCompletionBase):
    id: int
    reminder_id: int

    model_config = ConfigDict(from_attributes=True)


class ReminderCreate(BaseModel):
    title: str = Field(..., max_length=200)
    category: str = Field(default="medication", description="medication, appointment, hydration, activity, custom")
    scheduled_time: str = Field(..., description="E.g. 08:30, 14:00, 20:30")
    timezone: str = "Asia/Kolkata"
    start_date: date = Field(default_factory=date.today)
    recurrence: str = Field(default="daily", description="daily, weekly, weekdays, once")
    notes: Optional[str] = None
    is_active: bool = True


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    scheduled_time: Optional[str] = None
    timezone: Optional[str] = None
    start_date: Optional[date] = None
    recurrence: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ReminderSnoozeRequest(BaseModel):
    snooze_minutes: int = Field(default=30, ge=5, le=1440)


class ReminderResponse(BaseModel):
    id: int
    user_id: int
    title: str
    category: str
    scheduled_time: str
    timezone: str
    start_date: date
    recurrence: str
    notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    completions: List[ReminderCompletionResponse] = []

    model_config = ConfigDict(from_attributes=True)
