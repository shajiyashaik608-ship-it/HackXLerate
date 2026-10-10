from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.chat import Conversation, ChatMessage
from app.repositories.chat_repo import chat_repo
from app.repositories.user_repo import user_repo
from app.services.retrieval_service import retrieval_service
from app.integrations.llm_provider import get_llm_provider
from app.utils.guardrails import (
    check_urgent_symptoms,
    sanitize_ai_output,
    get_standard_safety_notice,
    EMERGENCY_DISCLAIMER_EN,
    EMERGENCY_DISCLAIMER_TE,
)
from app.core.exceptions import NotFoundException


SYSTEM_INSTRUCTION = (
    "You are Health Saathi (PCOS Saathi), an empathetic, culturally grounded healthcare copilot "
    "focused on women's metabolic health, PCOS awareness, Indian nutrition, and doctor visit preparation. "
    "Rules: "
    "1. Do NOT diagnose medical conditions. "
    "2. Do NOT prescribe medications or adjust dosages. "
    "3. Never promise to cure PCOS. "
    "4. Explain medical terms, lab results, and menstrual variability clearly in accessible terms. "
    "5. Encourage thoughtful collaboration with certified clinicians."
)


class AssistantService:
    async def chat(
        self,
        db: Session,
        user_id: int,
        message: str,
        language: str = "en",
        conversation_id: Optional[int] = None,
        include_health_context: bool = True
    ) -> Dict[str, Any]:
        """
        Coordinates emergency red-flag screening, knowledge retrieval, and AI answering.
        """
        # 1. Immediate deterministic red-flag emergency screening
        is_urgent, urgent_msg = check_urgent_symptoms(message, language=language)
        if is_urgent:
            # Short-circuit immediately without delaying for LLM inference
            return {
                "conversation_id": conversation_id or 0,
                "answer": urgent_msg,
                "language": language,
                "sources": ["Emergency Medical Safety Protocol (112 Emergency Care)"],
                "safety_notice": urgent_msg,
                "urgent_care_flag": True,
                "is_mock_response": False,
                "suggested_followups": [
                    "Where is the nearest hospital emergency department?",
                    "How do I contact emergency services?"
                ]
            }

        # 2. Manage or create conversation
        if conversation_id:
            conv = chat_repo.get_by_id_and_user(db, conversation_id=conversation_id, user_id=user_id)
            if not conv:
                conv = Conversation(user_id=user_id, language=language)
                db.add(conv)
                db.commit()
                db.refresh(conv)
        else:
            conv = Conversation(user_id=user_id, language=language)
            db.add(conv)
            db.commit()
            db.refresh(conv)

        # Log user query
        user_msg_record = ChatMessage(
            conversation_id=conv.id,
            role="user",
            content=message
        )
        chat_repo.add_message(db, user_msg_record)

        # 3. Retrieve grounded context passages
        passages = retrieval_service.retrieve_relevant_passages(message, top_k=2)

        # 4. Generate response via configured LLM provider (Gemini or Mock)
        llm = get_llm_provider()
        llm_output = await llm.generate_response(
            prompt=message,
            system_instruction=SYSTEM_INSTRUCTION,
            context_passages=passages,
            language=language
        )

        raw_answer = llm_output.get("answer", "")
        # Sanitize against any forbidden diagnosis or cure claims
        safe_answer = sanitize_ai_output(raw_answer, language=language)
        sources = llm_output.get("sources", [])
        is_mock = llm_output.get("is_mock_response", True)

        # Log assistant response
        assistant_msg_record = ChatMessage(
            conversation_id=conv.id,
            role="assistant",
            content=safe_answer
        )
        chat_repo.add_message(db, assistant_msg_record)

        # Suggested followups based on topic
        if language == "te":
            followups = [
                "PCOS లో ఇన్సులిన్ నిరోధకత అంటే ఏమిటి?",
                "డాక్టర్‌ని సంప్రదించినప్పుడు ఏ ప్రశ్నలు అడగాలి?",
                "భారతీయ భోజనంలో ఏ మార్పులు చేసుకోవాలి?"
            ]
        else:
            followups = [
                "What questions should I ask my doctor about my cycle?",
                "How does insulin sensitivity affect PCOS?",
                "Which Indian foods support balanced energy?"
            ]

        return {
            "conversation_id": conv.id,
            "message_id": assistant_msg_record.id,
            "answer": safe_answer,
            "language": language,
            "sources": sources,
            "safety_notice": get_standard_safety_notice(language),
            "urgent_care_flag": False,
            "is_mock_response": is_mock,
            "suggested_followups": followups
        }

    def get_user_conversations(self, db: Session, user_id: int) -> List[Conversation]:
        return chat_repo.get_by_user(db, user_id=user_id)

    def get_conversation_details(self, db: Session, conversation_id: int, user_id: int) -> Conversation:
        conv = chat_repo.get_by_id_and_user(db, conversation_id=conversation_id, user_id=user_id)
        if not conv:
            raise NotFoundException("Conversation not found.")
        return conv

    def delete_conversation(self, db: Session, conversation_id: int, user_id: int) -> bool:
        conv = self.get_conversation_details(db, conversation_id=conversation_id, user_id=user_id)
        return chat_repo.delete(db, conv.id)


assistant_service = AssistantService()
