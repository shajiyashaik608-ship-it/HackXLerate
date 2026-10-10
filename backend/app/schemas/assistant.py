from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator


class ChatMessageCreate(BaseModel):
    message: Optional[str] = None
    question: Optional[str] = None
    language: str = Field(default="en", description="en or te")
    conversation_id: Optional[int] = None
    include_health_context: bool = True

    @model_validator(mode="after")
    def populate_message(self):
        effective = (self.message or self.question or "").strip()
        if not effective:
            raise ValueError("Either 'message' or 'question' must be provided.")
        self.message = effective
        return self


class ChatMessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str  # user, assistant, system
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssistantChatResponse(BaseModel):
    conversation_id: int
    message_id: Optional[int] = None
    answer: str
    language: str = "en"
    sources: List[str] = []
    educational_sources: List[str] = []  # Frontend client compatibility
    audio_text: Optional[str] = None      # Frontend client compatibility
    escalate_to_doctor: bool = False     # Frontend client compatibility
    safety_notice: str = "Educational health information only. Not a medical diagnosis or treatment prescription. Always consult a certified healthcare professional."
    urgent_care_flag: bool = False
    is_mock_response: bool = False
    suggested_followups: List[str] = []

    @model_validator(mode="after")
    def populate_compat_fields(self):
        if not self.educational_sources and self.sources:
            self.educational_sources = self.sources
        if not self.audio_text:
            self.audio_text = self.answer.split("⚠️")[0].split("🚨")[0].strip()
        self.escalate_to_doctor = self.urgent_care_flag
        return self


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    language: str
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    model_config = ConfigDict(from_attributes=True)
