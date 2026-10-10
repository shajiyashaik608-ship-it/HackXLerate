from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.consultation_service import consultation_service
from app.schemas.consultation import (
    ConsultationBriefCreate,
    ConsultationBriefUpdate,
    ConsultationBriefResponse,
)

router = APIRouter(prefix="/consultations", tags=["Doctor Consultation"])


@router.post("/brief", response_model=ConsultationBriefResponse, status_code=status.HTTP_201_CREATED)
def create_consultation_brief(
    payload: ConsultationBriefCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return consultation_service.generate_brief(
        db=db,
        user_id=current_user.id,
        primary_concerns=payload.primary_concerns,
        symptoms_summary=payload.symptoms_summary,
        lab_flags_summary=payload.lab_flags_summary,
        prioritized_questions=payload.prioritized_questions,
        include_active_reminders=payload.include_active_reminders,
        include_recent_cycles=payload.include_recent_cycles
    )


@router.get("/briefs", response_model=List[ConsultationBriefResponse])
def list_consultation_briefs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return consultation_service.get_user_briefs(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/briefs/{brief_id}", response_model=ConsultationBriefResponse)
def get_consultation_brief(
    brief_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return consultation_service.get_brief_by_id(db, brief_id=brief_id, user_id=current_user.id)


@router.patch("/briefs/{brief_id}", response_model=ConsultationBriefResponse)
def update_consultation_brief(
    brief_id: int,
    payload: ConsultationBriefUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = payload.model_dump(exclude_unset=True)
    return consultation_service.update_brief(
        db=db, brief_id=brief_id, user_id=current_user.id, update_data=update_data
    )


@router.delete("/briefs/{brief_id}")
def delete_consultation_brief(
    brief_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    consultation_service.delete_brief(db, brief_id=brief_id, user_id=current_user.id)
    return {"message": "Consultation brief deleted successfully."}
