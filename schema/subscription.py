from sqlalchemy import Column, Integer, String
from db_configuration.pgdb_config import Base


class SubscriptionTransaction(Base):
    __tablename__ = "subscription_transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    plan_id = Column(Integer)
    status = Column(String)
