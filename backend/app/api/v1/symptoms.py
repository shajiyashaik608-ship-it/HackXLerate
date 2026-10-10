from fastapi import APIRouter, Depends, status
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.cycle_service import cycle_service
from app.schemas.symptom import (
    SymptomLogCreate,
    SymptomLogUpdate,
    SymptomLogResponse,
    SymptomSummaryResponse,
)

router = APIRouter(prefix="/symptoms", tags=["Symptoms"])


@router.post("/log", response_model=SymptomLogResponse, status_code=status.HTTP_201_CREATED)
def log_symptom(
    payload: SymptomLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cycle_service.log_symptom(
        db=db,
        user_id=current_user.id,
        symptom_type=payload.symptom_type,
        severity=payload.severity,
        recorded_date=payload.recorded_date,
        notes=payload.notes
    )


@router.get("/history", response_model=List[SymptomLogResponse])
def get_symptom_history(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cycle_service.get_symptom_history(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/summary", response_model=SymptomSummaryResponse)
def get_symptom_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cycle_service.summarize_symptoms(db, user_id=current_user.id)


@router.patch("/{symptom_id}", response_model=SymptomLogResponse)
def update_symptom(
    symptom_id: int,
    payload: SymptomLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = payload.model_dump(exclude_unset=True)
    return cycle_service.update_symptom(
        db=db,
        symptom_id=symptom_id,
        user_id=current_user.id,
        update_data=update_data
    )


@router.delete("/{symptom_id}")
def delete_symptom(
    symptom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cycle_service.delete_symptom(db, symptom_id=symptom_id, user_id=current_user.id)
    return {"message": "Symptom record deleted successfully."}
