from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_configuration.pgdb_config import get_db
from utils.security import get_current_user
from service.conversation_service import ConversationService
from schema.user_detailed import UserDetails
from pydantic import BaseModel


router = APIRouter(prefix="/conversation", tags=["Conversation"])


class ConversationRequest(BaseModel):
    query: str
    rag_mode: str = "VECTOR"
    top_k: int = 5


@router.post("/ask")
async def ask_conversation(
    payload: ConversationRequest,
    current_user: UserDetails = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ConversationService(db)
    return await service.ask(
        user=current_user,
        query=payload.query,
        rag_mode=payload.rag_mode,
        top_k=payload.top_k
    )