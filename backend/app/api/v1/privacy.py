from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.privacy_service import privacy_service
from app.schemas.privacy import (
    PrivacyExportResponse,
    PrivacyPurgeRequest,
    PrivacyPurgeResponse,
)

router = APIRouter(prefix="/privacy", tags=["Privacy and Data Governance"])


@router.get("/export", response_model=PrivacyExportResponse)
def export_personal_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return privacy_service.export_user_data(db, user_id=current_user.id)


@router.post("/purge", response_model=PrivacyPurgeResponse)
def purge_personal_data(
    payload: PrivacyPurgeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return privacy_service.purge_user_data(
        db=db, user_id=current_user.id, confirm_phrase=payload.confirm_phrase
    )
