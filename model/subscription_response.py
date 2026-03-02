from pydantic import BaseModel


class SubscriptionUpgradeResponse(BaseModel):
    message: str
    old_plan: str
    new_plan: str
    transaction_id: int