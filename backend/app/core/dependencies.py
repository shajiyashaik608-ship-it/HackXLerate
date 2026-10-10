from typing import Optional
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token
from app.core.exceptions import AuthenticationException
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False
)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependency that enforces JWT authentication and returns the User entity."""
    if not token:
        raise AuthenticationException("Authentication token required.")
    
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise AuthenticationException("Invalid or expired authentication token.")
    
    user_id = payload.get("user_id")
    sub = payload.get("sub")
    if not user_id and not sub:
        raise AuthenticationException("Token subject missing.")

    user = None
    if user_id is not None:
        try:
            user = db.query(User).filter(User.id == int(user_id)).first()
        except (ValueError, TypeError):
            pass

    if not user and sub:
        if str(sub).isdigit():
            user = db.query(User).filter(User.id == int(sub)).first()
        else:
            user = db.query(User).filter(User.email == str(sub).lower().strip()).first()
    if not user:
        raise AuthenticationException("Authenticated user not found.")
        
    if not user.is_active:
        raise AuthenticationException("User account is inactive.")
        
    return user


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Dependency for public/demo endpoints that optionally extracts user if provided."""
    if not token:
        return None
    try:
        return get_current_user(token=token, db=db)
    except AuthenticationException:
        return None
