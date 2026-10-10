from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NotificationCreate(BaseModel):
    title: str = Field(..., max_length=150)
    message: str = Field(..., max_length=500)
    notification_type: str = Field(default="system", description="reminder, lab_result, cycle, tip, system")


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
