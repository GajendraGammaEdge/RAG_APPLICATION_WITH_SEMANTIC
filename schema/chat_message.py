from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from db_configuration.pgdb_config import Base
import enum


class MessageRole(enum.Enum):
    USER = "user"
    AI = "ai"


class ChatMessage(Base):
    __tablename__ = "chat_message"

    message_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("user_detailes.id", ondelete="CASCADE"),
        nullable=False,
    )

    session_id = Column(
        Integer,
        ForeignKey("chat_session.session_id", ondelete="CASCADE"),
        nullable=False,
    )

    role = Column(Enum(MessageRole), nullable=False)

    user_query = Column(Text)
    semantic_context = Column(Text)

    ai_response = Column(Text)

    rag_mode = Column(
        Enum("VECTOR", "PAGE_INDEX", "HYBRID", name="rag_mode_enum"),
        nullable=False,
        default="VECTOR"
    )
    page_references = Column(Text)

    created_at = Column(DateTime, default=datetime.now)

    user = relationship("UserDetails", back_populates="chat_messages")
    session = relationship("ChatSession", back_populates="messages")