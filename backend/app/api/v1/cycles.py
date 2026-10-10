from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.cycle_service import cycle_service
from app.schemas.cycle import (
    CycleLogCreate,
    CycleLogUpdate,
    CycleLogResponse,
    CycleEstimateResponse,
)

router = APIRouter(prefix="/cycles", tags=["Menstrual Cycles"])


@router.post("/log", response_model=CycleLogResponse, status_code=status.HTTP_201_CREATED)
def log_cycle(
    payload: CycleLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cycle_service.log_cycle(
        db=db,
        user_id=current_user.id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        duration_days=payload.duration_days,
        flow_intensity=payload.flow_intensity,
        notes=payload.notes
    )


@router.get("/history", response_model=List[CycleLogResponse])
def get_cycle_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cycle_service.get_cycle_history(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/estimate", response_model=CycleEstimateResponse)
def estimate_cycle(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cycle_service.estimate_cycle(db, user_id=current_user.id)


@router.patch("/{cycle_id}", response_model=CycleLogResponse)
def update_cycle(
    cycle_id: int,
    payload: CycleLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = payload.model_dump(exclude_unset=True)
    return cycle_service.update_cycle(
        db=db,
        cycle_id=cycle_id,
        user_id=current_user.id,
        update_data=update_data
    )


@router.delete("/{cycle_id}")
def delete_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cycle_service.delete_cycle(db, cycle_id=cycle_id, user_id=current_user.id)
    return {"message": "Cycle entry deleted successfully."}
