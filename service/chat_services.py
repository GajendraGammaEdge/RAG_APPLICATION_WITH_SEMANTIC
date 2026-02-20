# service/chat_service.py
from sqlalchemy.orm import Session
from schema.chat_session import ChatSession
from sqlalchemy import desc, asc
from schema.chat_message import ChatMessage


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def get_chat_sessions(
        self,
        user_id: int,
        limit: int = 10,
        offset: int = 0
    ):
        sessions = (
            self.db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(desc(ChatSession.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )

        total = (
            self.db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .count()
        )

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "sessions": [
                {
                    "session_id": s.session_id,
                    "session_name": s.session_name,
                    "created_at": s.created_at
                }
                for s in sessions
            ]
        }

    def get_chat_messages(self, session_id: int, user_id: int):
        messages = (
            self.db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id,
                ChatMessage.user_id == user_id
            )
            .order_by(asc(ChatMessage.created_at))
            .all()
        )

        if not messages:
            return {
                "session_id": session_id,
                "messages": []
            }

        return {
            "session_id": session_id,
            "messages": [
                {
                    "message_id": m.message_id,
                    "role": m.role.value,
                    "user_query": m.user_query,
                    "ai_response": m.ai_response,
                    "created_at": m.created_at
                }
                for m in messages
            ]
        }
