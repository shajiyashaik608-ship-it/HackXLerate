from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.chat import Conversation, ChatMessage


class ChatRepository(BaseRepository[Conversation]):
    def __init__(self):
        super().__init__(Conversation)

    def get_by_user(self, db: Session, user_id: int) -> List[Conversation]:
        stmt = (
            select(Conversation)
            .options(joinedload(Conversation.messages))
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.created_at))
        )
        return list(db.scalars(stmt).unique().all())

    def get_by_id_and_user(self, db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        stmt = (
            select(Conversation)
            .options(joinedload(Conversation.messages))
            .where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        )
        return db.scalars(stmt).first()

    def add_message(self, db: Session, message: ChatMessage) -> ChatMessage:
        db.add(message)
        db.commit()
        db.refresh(message)
        return message


chat_repo = ChatRepository()
