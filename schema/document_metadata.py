from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    LargeBinary,
  )
from db_configuration.pgdb_config import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from schema.document_page import DocumentPages

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    doc_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_name = Column(String, nullable=False)
    doc_type = Column(String, nullable=False)
    doc_size = Column(Integer, nullable=False)
    file_data = Column(LargeBinary, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer,
                     ForeignKey("user_detailes.id", ondelete="CASCADE"),
                     nullable=False)
    user = relationship("UserDetails", back_populates="documents")
    chunks = relationship(
        "DocumentChunks",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    pages = relationship(
    "DocumentPages",
    cascade="all, delete-orphan"
    )