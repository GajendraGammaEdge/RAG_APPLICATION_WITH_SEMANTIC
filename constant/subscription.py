from enum import Enum
from typing import List


class SubscriptionEnum(Enum):
    FREE = "FREE"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"


class RagModeEnum(Enum):
    VECTOR = "VECTOR"
    PAGE_INDEX = "PAGE_INDEX"
    HYBRID = "HYBRID"


SUBSCRIPTION_RAG_ACCESS = {
    SubscriptionEnum.FREE: [RagModeEnum.VECTOR],
    SubscriptionEnum.BRONZE: [RagModeEnum.VECTOR],
    SubscriptionEnum.SILVER: [
        RagModeEnum.VECTOR,
        RagModeEnum.PAGE_INDEX
    ],
    SubscriptionEnum.GOLD: [
        RagModeEnum.VECTOR,
        RagModeEnum.PAGE_INDEX,
        RagModeEnum.HYBRID
    ],
}


def is_rag_mode_allowed(subscription, rag_mode: RagModeEnum) -> bool:
    return rag_mode in SUBSCRIPTION_RAG_ACCESS.get(subscription, [])