from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from db_configuration.pgdb_config import Base
from constant.subscription import SubscriptionEnum


class SubscriptionTransaction(Base):
    __tablename__ = "subscription_transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("user_detailes.id", ondelete="CASCADE"),
        nullable=False
    )

    old_plan = Column(
        Enum(SubscriptionEnum, name="subscription_level"),
        nullable=False
    )

    new_plan = Column(
        Enum(SubscriptionEnum, name="subscription_level"),
        nullable=False
    )

    amount = Column(Integer, default=0)   # in smallest unit (₹ paise / cents)
    currency = Column(String, default="INR")

    payment_status = Column(
        String,
        default="SUCCESS"   # SUCCESS | FAILED | PENDING
    )

    payment_method = Column(
        String,
        default="INTERNAL"  # INTERNAL | RAZORPAY | STRIPE
    )

    reference_id = Column(String, nullable=True)  # gateway txn id

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserDetails")