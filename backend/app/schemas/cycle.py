from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CycleLogCreate(BaseModel):
    start_date: date
    end_date: Optional[date] = None
    duration_days: Optional[int] = Field(default=4, ge=1, le=20)
    flow_intensity: str = Field(default="medium")  # spotting, light, medium, heavy
    notes: Optional[str] = None


class CycleLogUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    flow_intensity: Optional[str] = None
    notes: Optional[str] = None


class CycleLogResponse(BaseModel):
    id: int
    user_id: int
    start_date: date
    end_date: Optional[date] = None
    duration_days: Optional[int] = None
    flow_intensity: str
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CycleEstimateResponse(BaseModel):
    historical_intervals: List[int]
    average_cycle_length: float
    estimation_method: str = "PCOS Adaptive Interval Heuristic (±5 Days)"
    estimated_arrival_window: str
    window_start: Optional[date] = None
    window_end: Optional[date] = None
    current_cycle_day: Optional[int] = None
    phase_name: Optional[str] = None
    uncertainty_notice: str = "PCOS cycles exhibit natural biological variability. Dates are estimated windows rather than guaranteed exact days."
    has_sufficient_history: bool
