from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.repositories.user_repo import user_repo
from app.schemas.user import UserResponse, UserSettingsUpdate, UserConsentUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/settings", response_model=UserResponse)
def update_user_settings(
    payload: UserSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name.strip()
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/consent", response_model=UserResponse)
def update_consent(
    payload: UserConsentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.consent_given = payload.consent_given
    db.commit()
    db.refresh(current_user)
    return current_user
