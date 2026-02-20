from utils.embedding_utils import get_embedding
from utils.rag_utils import RagUtilsGPT
from schema.chat_session import ChatSession
from schema.chat_message import ChatMessage, MessageRole
from fastapi import HTTPException
from sqlalchemy import desc


class RAGService:
    def __init__(self, db):
        self.db = db
        self.model_call = RagUtilsGPT(db)

    async def answer_question(
        self,
        query: str,
        top_k: int = 5,
        ai_model: str = "gemini2",
        user_id: int = None
    ):
        if user_id is None:
            raise HTTPException(
                status_code=400,
                detail="user_id is required",
            )
        session = (
            self.db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(desc(ChatSession.created_at))
            .first()
        )

        if session is None:
            session = ChatSession(user_id=user_id, session_name=query)
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)

        session_id = session.session_id
        self.db.add(ChatMessage(
            user_id=user_id,
            session_id=session_id,
            role=MessageRole.USER,
            user_query=query
        ))
        self.db.commit()
        query_vector = get_embedding(query)
        result = None

        if ai_model == "gpt_5":
            result = await self.model_call.gpt_5_model(
                query=query,
                query_vector=query_vector,
                top_k=top_k,
                user_id=user_id
            )
        elif ai_model == "gpt_4":
            result = await self.model_call.gpt_4_model(
                query=query,
                query_vector=query_vector,
                user_id=user_id,
                top_k=top_k
            )
        elif ai_model == "gemini2":
            result = await self.model_call.gemini_2_model(
                query=query,
                query_vector=query_vector,
                user_id=user_id,
                top_k=top_k
            )
        else:
            result = await self.model_call.gemini_25_model(
                query=query,
                query_vector=query_vector,
                user_id=user_id,
                top_k=top_k
            )
        self.db.add(ChatMessage(
            user_id=user_id,
            session_id=session_id,
            role=MessageRole.AI,
            ai_response=str(result)
        ))
        self.db.commit()
        return result
