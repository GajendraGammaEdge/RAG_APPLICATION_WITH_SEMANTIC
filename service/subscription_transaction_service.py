from sqlalchemy.orm import Session
from schema.subscription_request import SubscriptionTransaction


class SubscriptionTransactionService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_transactions(self, user_id: int):
        txns = (
            self.db.query(SubscriptionTransaction)
            .filter(SubscriptionTransaction.user_id == user_id)
            .order_by(SubscriptionTransaction.created_at.desc())
            .all()
        )

        return [
            {
                "transaction_id": t.id,
                "old_plan": t.old_plan.value,
                "new_plan": t.new_plan.value,
                "amount": t.amount,
                "currency": t.currency,
                "payment_status": t.payment_status,
                "payment_method": t.payment_method,
                "created_at": t.created_at
            }
            for t in txns
        ]