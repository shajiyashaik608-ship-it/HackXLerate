from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author_alias = Column(String, default="Anonymous Saathi")
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tag = Column(String, default="lifestyle")  # nutrition, symptoms, doctor_visit, emotional_health
    moderation_status = Column(String, default="approved")  # approved, pending, flagged
    answers = Column(JSON, default=list)  # List of answers/educational resources
    created_at = Column(DateTime(timezone=True), server_default=func.now())
