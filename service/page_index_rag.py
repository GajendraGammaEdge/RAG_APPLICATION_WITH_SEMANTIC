from schema.document_page import DocumentPages
from utils.rag_utils import RagUtilsGPT


async def page_index_rag(db, query: str, user_id: int, top_k: int = 2):
    pages = (
        db.query(DocumentPages)
        .filter(DocumentPages.content.ilike(f"%{query.split()[0]}%"))
        .limit(top_k)
        .all()
    )

    if not pages:
        return "No relevant pages found.", []

    context = "\n".join(
        f"Page {p.page_number}:\n{p.content}"
        for p in pages
    )

    llm = RagUtilsGPT(db)
    answer = await llm.gemini_2_model(
        query=query,
        user_id=user_id,
        top_k=top_k,
        query_vector=None
    )

    return answer, [p.page_number for p in pages]