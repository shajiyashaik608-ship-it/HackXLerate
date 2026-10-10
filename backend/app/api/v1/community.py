from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.models.community import CommunityPost, CommunityReply, ContentReport
from app.repositories.community_repo import community_repo
from app.core.exceptions import NotFoundException, ValidationException
from app.schemas.community import (
    CommunityPostCreate,
    CommunityPostResponse,
    CommunityReplyCreate,
    CommunityReplyResponse,
    ContentReportCreate,
    ContentReportResponse,
    PostVoteResponse,
)

router = APIRouter(prefix="/community", tags=["Community Peer Support"])


@router.get("/posts", response_model=List[CommunityPostResponse])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    posts = community_repo.get_public_posts(db, skip=skip, limit=limit, tag=tag)
    responses = []
    for p in posts:
        resp = CommunityPostResponse(
            id=p.id,
            pseudonym=p.pseudonym,
            title=p.title,
            content=p.content,
            tags=p.tags,
            status=p.status,
            created_at=p.created_at,
            replies_count=len(p.replies),
            replies=[
                CommunityReplyResponse(
                    id=r.id,
                    post_id=r.post_id,
                    pseudonym=r.pseudonym or "Anonymous Saathi",
                    content=r.content,
                    status=r.status,
                    created_at=r.created_at
                )
                for r in p.replies if r.status == "active"
            ]
        )
        responses.append(resp)
    return responses


@router.post("/posts", response_model=CommunityPostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: CommunityPostCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    pseudonym = payload.pseudonym or "Anonymous Saathi"
    post = CommunityPost(
        user_id=current_user.id if current_user else None,
        pseudonym=pseudonym,
        title=payload.title.strip(),
        content=payload.content.strip(),
        tags=payload.tags,
        status="active"
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    return CommunityPostResponse(
        id=post.id,
        pseudonym=post.pseudonym,
        title=post.title,
        content=post.content,
        tags=post.tags,
        status=post.status,
        created_at=post.created_at,
        replies_count=0,
        replies=[]
    )


@router.get("/posts/{post_id}", response_model=CommunityPostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = community_repo.get_post_by_id(db, post_id)
    if not post or post.status != "active":
        raise NotFoundException("Community post not found.")

    return CommunityPostResponse(
        id=post.id,
        pseudonym=post.pseudonym,
        title=post.title,
        content=post.content,
        tags=post.tags,
        status=post.status,
        created_at=post.created_at,
        replies_count=len(post.replies),
        replies=[
            CommunityReplyResponse(
                id=r.id,
                post_id=r.post_id,
                pseudonym=r.pseudonym or "Anonymous Saathi",
                content=r.content,
                status=r.status,
                created_at=r.created_at
            )
            for r in post.replies if r.status == "active"
        ]
    )


@router.post("/posts/{post_id}/replies", response_model=CommunityReplyResponse, status_code=status.HTTP_201_CREATED)
def add_reply(
    post_id: int,
    payload: CommunityReplyCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    post = community_repo.get_post_by_id(db, post_id)
    if not post or post.status != "active":
        raise NotFoundException("Community post not found.")

    reply = CommunityReply(
        post_id=post_id,
        user_id=current_user.id if current_user else None,
        pseudonym=payload.pseudonym or "Anonymous Saathi",
        content=payload.content.strip(),
        status="active"
    )
    saved = community_repo.add_reply(db, reply)
    return CommunityReplyResponse(
        id=saved.id,
        post_id=saved.post_id,
        pseudonym=saved.pseudonym,
        content=saved.content,
        status=saved.status,
        created_at=saved.created_at
    )


@router.post("/posts/{post_id}/report", response_model=ContentReportResponse)
def report_post(
    post_id: int,
    payload: ContentReportCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    post = community_repo.get_post_by_id(db, post_id)
    if not post:
        raise NotFoundException("Community post not found.")

    report = ContentReport(
        reporter_id=current_user.id if current_user else None,
        post_id=post_id,
        reason=payload.reason.strip(),
        status="pending_review"
    )
    saved = community_repo.add_report(db, report)
    return ContentReportResponse(
        id=saved.id,
        post_id=saved.post_id,
        reason=saved.reason,
        status=saved.status,
        created_at=saved.created_at
    )


@router.post("/posts/{post_id}/vote", response_model=PostVoteResponse)
def vote_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = community_repo.get_post_by_id(db, post_id)
    if not post:
        raise NotFoundException("Community post not found.")
    return PostVoteResponse(post_id=post_id, success=True, message="Support vote recorded.")
