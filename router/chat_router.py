# router/chat_router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db_configuration.pgdb_config import get_db
from service.chat_services import ChatService
from utils.security import get_current_user
from schema.user_detailed import UserDetails

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/sessions")
def get_sessions_of_user(
    current_user: UserDetails = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    service = ChatService(db)

    return service.get_chat_sessions(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )


@router.get("/sessions/{session_id}/messages")
def get_chat_messages(
    session_id: int,
    current_user: UserDetails = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)

    return service.get_chat_messages(
        session_id=session_id,
        user_id=current_user.id
    )
