from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.biomarker_service import biomarker_service
from app.schemas.biomarker import (
    BiomarkerResponse,
    BiomarkerCorrectionUpdate,
    BiomarkerExplainResponse,
    BiomarkerTrendsResponse,
)

router = APIRouter(prefix="/biomarkers", tags=["Biomarkers"])


@router.get("", response_model=List[BiomarkerResponse])
def list_biomarkers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return biomarker_service.get_user_biomarkers(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/trends", response_model=BiomarkerTrendsResponse)
def get_biomarker_trends(
    test_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return biomarker_service.get_trends(db, user_id=current_user.id, test_name=test_name)


@router.get("/{biomarker_id}", response_model=BiomarkerResponse)
def get_biomarker_by_id(
    biomarker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return biomarker_service.get_biomarker(db, biomarker_id=biomarker_id, user_id=current_user.id)


@router.patch("/{biomarker_id}", response_model=BiomarkerResponse)
def correct_biomarker_value(
    biomarker_id: int,
    payload: BiomarkerCorrectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = payload.model_dump(exclude_unset=True)
    return biomarker_service.correct_biomarker(
        db=db,
        biomarker_id=biomarker_id,
        user_id=current_user.id,
        update_data=update_data
    )


@router.post("/{biomarker_id}/explain", response_model=BiomarkerExplainResponse)
def explain_biomarker_result(
    biomarker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return biomarker_service.explain_biomarker(db, biomarker_id=biomarker_id, user_id=current_user.id)
