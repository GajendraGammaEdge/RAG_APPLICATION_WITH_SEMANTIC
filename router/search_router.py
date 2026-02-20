# router/search_router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db_configuration.pgdb_config import get_db
from service.search_service import SearchService
from service.rag_service import RAGService
from schema.user_detailed import UserDetails
from utils.security import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/search")
async def search_documents(
    query: str = Query(...),
    top_k: int = Query(5, le=15, ge=1),
    search_type: str = Query("cosine"),
    current_user: UserDetails = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SearchService(db)
    results = await service.semantic_search_process(
        query,
        top_k,
        search_type
    )
    return {
        "query": query,
        "top_k": top_k,
        "results": results
    }


@router.post("/ask")
async def ask_question(
    query: str = Query(...),
    top_k: int = Query(5, le=15, ge=1),
    ai_model: str = Query("gemini2"),
    current_user: UserDetails = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = RAGService(db)

    answer = await service.answer_question(
        query=query,
        top_k=top_k,
        ai_model=ai_model,
        user_id=current_user.id
    )

    return {"query": query, "answer": answer}
