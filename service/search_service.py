from sqlalchemy.orm import Session
from utils.embedding_utils import get_embedding
from utils.semantic_search import SemanticSearch


class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.semantic_search = SemanticSearch(db)

    async def semantic_search_process(
        self,
        query: str,
        top_k: int = 5,
        search_type: str = "cosine",
    ):
        query_vector = get_embedding(query)

        if search_type == "cosine":
            return await self.semantic_search.cosine_search(
                query_vector=query_vector,
                top_k=top_k,
            )

        elif search_type == "euclidean":
            return await self.semantic_search.euclidean_search(
                query_vector=query_vector,
                top_k=top_k,
            )

        elif search_type == "inner_product":
            return await self.semantic_search.inner_product_search(
                query_vector=query_vector,
                top_k=top_k,
            )

        else:
            raise ValueError("Invalid semantic search type")
