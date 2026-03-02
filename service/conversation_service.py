import json
from fastapi import HTTPException
from sqlalchemy import desc

from schema.chat_session import ChatSession
from schema.chat_message import ChatMessage, MessageRole
from constant.subscription import RagModeEnum, is_rag_mode_allowed
from service.page_index_rag import page_index_rag
from service.rag_service import RAGService


class ConversationService:
    def __init__(self, db):
        self.db = db
        self.vector_rag = RAGService(db)

    async def ask(self, user, query: str, rag_mode: str, top_k: int):
        rag_mode_enum = RagModeEnum(rag_mode)

        if not is_rag_mode_allowed(user.subscription_own, rag_mode_enum):
            raise HTTPException(
                status_code=403,
                detail=f"{rag_mode} not allowed for {user.subscription_own.value}"
            )

        session = (
            self.db.query(ChatSession)
            .filter(ChatSession.user_id == user.id)
            .order_by(desc(ChatSession.created_at))
            .first()
        )

        if not session:
            session = ChatSession(
                user_id=user.id,
                session_name=query
            )
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)

        
        self.db.add(ChatMessage(
            user_id=user.id,
            session_id=session.session_id,
            role=MessageRole.USER,
            user_query=query,
            rag_mode=rag_mode
        ))
        self.db.commit()

        if rag_mode == "VECTOR":
            answer = await self.vector_rag.answer_question(
                query=query,
                top_k=top_k,
                user_id=user.id
            )
            page_refs = []

        elif rag_mode == "PAGE_INDEX":
            context, page_refs = await page_index_rag(self.db, query)
            answer = context  

        else:  
            context, page_refs = await page_index_rag(self.db, query)
            answer = context


        self.db.add(ChatMessage(
            user_id=user.id,
            session_id=session.session_id,
            role=MessageRole.AI,
            ai_response=str(answer),
            rag_mode=rag_mode,
            page_references=json.dumps(page_refs)
        ))
        self.db.commit()

        return {
            "answer": answer,
            "rag_mode": rag_mode,
            "page_references": page_refs
        }