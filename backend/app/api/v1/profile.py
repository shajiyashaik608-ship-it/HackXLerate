from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.profile import HealthProfile
from app.repositories.user_repo import user_repo
from app.schemas.profile import HealthProfileResponse, HealthProfileUpdate

router = APIRouter(prefix="/profile", tags=["Health Profile"])


@router.get("", response_model=HealthProfileResponse)
def get_health_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = user_repo.get_profile_by_user_id(db, current_user.id)
    if not profile:
        profile = HealthProfile(user_id=current_user.id, diet_type="veg", preferred_language="en", timezone="Asia/Kolkata")
        profile = user_repo.create_profile(db, profile)
    return profile


@router.patch("", response_model=HealthProfileResponse)
def update_health_profile(
    payload: HealthProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = user_repo.get_profile_by_user_id(db, current_user.id)
    if not profile:
        profile = HealthProfile(user_id=current_user.id, diet_type="veg", preferred_language="en", timezone="Asia/Kolkata")
        db.add(profile)
        db.commit()
        db.refresh(profile)

    update_dict = payload.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        if hasattr(profile, field):
            setattr(profile, field, val)

    db.commit()
    db.refresh(profile)
    return profile
