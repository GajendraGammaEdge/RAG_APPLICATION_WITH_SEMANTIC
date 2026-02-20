from sqlalchemy.orm import Session
from sqlalchemy import select
from schema.documents_chunks import DocumentChunks


class SemanticSearch:
    def __init__(self, db: Session):
        self.db = db

    async def cosine_search(self, query_vector: list[float], top_k: int = 5):
        stmt = (
            select(DocumentChunks.content)
            .order_by(DocumentChunks.embedding.cosine_distance(query_vector))
            .limit(top_k)
        )
        return self.db.execute(stmt).scalars().all()

    async def euclidean_search(
            self,
            query_vector: list[float],
            top_k: int = 5):
        stmt = (
            select(DocumentChunks.content)
            .order_by(DocumentChunks.embedding.l2_distance(query_vector))
            .limit(top_k)
        )
        return self.db.execute(stmt).scalars().all()

    async def inner_product_search(
            self,
            query_vector: list[float],
            top_k: int = 5
            ):
        stmt = (
            select(DocumentChunks.content)
            .order_by(DocumentChunks.embedding.max_inner_product(query_vector))
            .limit(top_k)
        )
        return self.db.execute(stmt).scalars().all()
