# schema/chat_session.py
from sqlalchemy import (
        Column,
        Integer,
        DateTime,
        ForeignKey,
        Text,
        )
from sqlalchemy.orm import relationship
from datetime import datetime
from db_configuration.pgdb_config import Base


class ChatSession(Base):
    __tablename__ = "chat_session"
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,
                     ForeignKey("user_detailes.id", ondelete="CASCADE"),
                     nullable=False)
    session_name = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("UserDetails", back_populates="chat_sessions")
    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan"
    )
