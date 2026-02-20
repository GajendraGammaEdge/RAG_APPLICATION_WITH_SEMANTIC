from sqlalchemy import Column, String, Integer, Date, DateTime, Enum
from db_configuration.pgdb_config import Base
from datetime import datetime
from constant.subscription import SubscriptionEnum
from sqlalchemy.orm import relationship


class UserDetails(Base):
    __tablename__ = "user_detailes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    profession = Column(String)
    age = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime)

    subscription_own = Column(
        Enum(SubscriptionEnum, name="subscription_level"),
        default=SubscriptionEnum.FREE,
        nullable=False
    )
    documents = relationship(
        "DocumentMetadata",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    chat_sessions = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    chat_messages = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete-orphan"
    )
