from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.timeline_service import timeline_service
from app.schemas.timeline import TimelineResponse

router = APIRouter(prefix="/timeline", tags=["Health Timeline"])


@router.get("", response_model=TimelineResponse)
def get_user_timeline(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return timeline_service.get_timeline_events(
        db=db, user_id=current_user.id, page=page, page_size=page_size
    )
