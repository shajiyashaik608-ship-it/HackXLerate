from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.services.assistant_service import assistant_service
from app.schemas.assistant import (
    ChatMessageCreate,
    AssistantChatResponse,
    ConversationResponse,
)

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


@router.post("/chat", response_model=AssistantChatResponse)
async def chat_with_assistant(
    payload: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await assistant_service.chat(
        db=db,
        user_id=current_user.id,
        message=payload.message,
        language=payload.language,
        conversation_id=payload.conversation_id,
        include_health_context=payload.include_health_context
    )


@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return assistant_service.get_user_conversations(db, user_id=current_user.id)


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return assistant_service.get_conversation_details(
        db, conversation_id=conversation_id, user_id=current_user.id
    )


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assistant_service.delete_conversation(db, conversation_id=conversation_id, user_id=current_user.id)
    return {"message": "Conversation history deleted."}
