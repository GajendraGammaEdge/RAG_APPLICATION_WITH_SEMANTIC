from sqlalchemy import  Column , Integer , ForeignKey , Text , DateTime
from datetime import datetime
from db_configuration.pgdb_config import  Base


class DocumentPages(Base):
    __tablename__ = "document_pages"

    page_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(
        Integer,
        ForeignKey("document_metadata.doc_id", ondelete="CASCADE"),
        nullable=False
    )
    page_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.now)