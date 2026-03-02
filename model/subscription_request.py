from pydantic import BaseModel
from constant.subscription import SubscriptionEnum


class UpgradeSubscriptionRequest(BaseModel):
    plan: SubscriptionEnum