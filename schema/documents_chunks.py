from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from db_configuration.pgdb_config import Base
from pgvector.sqlalchemy import Vector
import uuid


class DocumentChunks(Base):
    __tablename__ = "document_chunks"

    chunk_id = Column(UUID(as_uuid=True), primary_key=True,
                      default=uuid.uuid4)
    doc_id = Column(Integer,
                    ForeignKey("document_metadata.doc_id", ondelete="CASCADE"))
    content = Column(String, nullable=False)
    embedding = Column(Vector(384))
    created_at = Column(DateTime, default=datetime.now)
    document = relationship("DocumentMetadata", back_populates="chunks")
