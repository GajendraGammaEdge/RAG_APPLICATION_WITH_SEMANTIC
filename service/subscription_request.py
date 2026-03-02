from fastapi import HTTPException
from sqlalchemy.orm import Session
from constant.subscription import SubscriptionEnum
from schema.user_detailed import UserDetails
from schema.subscription_request import SubscriptionTransaction


class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def upgrade_subscription(
        self,
        user: UserDetails,
        new_plan: SubscriptionEnum
    ):
        old_plan = user.subscription_own

        if old_plan == new_plan:
            raise HTTPException(
                status_code=400,
                detail="You are already on this plan"
            )

        if old_plan == SubscriptionEnum.GOLD:
            raise HTTPException(
                status_code=400,
                detail="You are already on the highest plan"
            )

        user.subscription_own = new_plan
        self.db.add(user)

        transaction = SubscriptionTransaction(
            user_id=user.id,
            old_plan=old_plan,
            new_plan=new_plan,
            amount=self._get_plan_price(new_plan),
            currency="INR",
            payment_status="SUCCESS",
            payment_method="INTERNAL"
        )

        self.db.add(transaction)
        self.db.commit()

        return {
            "message": "Subscription upgraded successfully",
            "old_plan": old_plan.value,
            "new_plan": new_plan.value,
            "transaction_id": transaction.id
        }

    def _get_plan_price(self, plan: SubscriptionEnum) -> int:
        prices = {
            SubscriptionEnum.FREE: 0,
            SubscriptionEnum.SILVER: 900,  
            SubscriptionEnum.GOLD: 1190     
        }
        return prices.get(plan, 0)