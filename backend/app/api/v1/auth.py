from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import ValidationException, UnauthorizedException
from app.models.user import User
from app.models.profile import HealthProfile
from app.repositories.user_repo import user_repo
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, TokenRefreshRequest
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    normalized_email = payload.email.lower().strip()
    existing_user = user_repo.get_by_email(db, normalized_email)
    if existing_user:
        raise ValidationException("An account with this email address already exists.")

    hashed_pw = get_password_hash(payload.password)
    new_user = User(
        email=normalized_email,
        hashed_password=hashed_pw,
        full_name=payload.full_name.strip(),
        is_active=True,
        is_verified=False,
        consent_given=payload.consent_given
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize default health profile
    profile = HealthProfile(
        user_id=new_user.id,
        diet_type="veg",
        preferred_language=payload.preferred_language or "en",
        timezone="Asia/Kolkata"
    )
    db.add(profile)
    db.commit()

    token_data = {"sub": new_user.email, "user_id": new_user.id}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    normalized_email = payload.email.lower().strip()
    user = user_repo.get_by_email(db, normalized_email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise UnauthorizedException("Incorrect email or password.")

    if not user.is_active:
        raise UnauthorizedException("Account is inactive.")

    token_data = {"sub": user.email, "user_id": user.id}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: TokenRefreshRequest, db: Session = Depends(get_db)):
    decoded = decode_token(payload.refresh_token)
    if not decoded or decoded.get("type") != "refresh":
        raise UnauthorizedException("Invalid or expired refresh token.")

    user_id = decoded.get("user_id")
    user = user_repo.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise UnauthorizedException("User associated with token not found or inactive.")

    token_data = {"sub": user.email, "user_id": user.id}
    new_access = create_access_token(token_data)
    new_refresh = create_refresh_token(token_data)

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out. Client sessions revoked."}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
