from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CommunityReplyCreate(BaseModel):
    content: str = Field(..., min_length=3, max_length=2000)
    pseudonym: Optional[str] = Field(None, max_length=50)


class CommunityReplyResponse(BaseModel):
    id: int
    post_id: int
    pseudonym: str = "Anonymous Saathi"
    content: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommunityPostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=5, max_length=5000)
    pseudonym: Optional[str] = Field(None, max_length=50)
    tags: Optional[str] = Field(default="lifestyle,pcos", description="Comma-separated tags")


class ContentReportCreate(BaseModel):
    reason: str = Field(..., min_length=3, max_length=500)


class ContentReportResponse(BaseModel):
    id: int
    post_id: int
    reason: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommunityPostResponse(BaseModel):
    id: int
    pseudonym: str
    title: str
    content: str
    tags: Optional[str] = None
    status: str
    created_at: datetime
    replies_count: int = 0
    replies: List[CommunityReplyResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PostVoteResponse(BaseModel):
    post_id: int
    success: bool = True
    message: str = "Vote recorded"
