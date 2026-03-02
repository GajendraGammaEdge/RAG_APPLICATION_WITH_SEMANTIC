from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db_configuration.pgdb_config import get_db
from utils.security import get_current_user
from schema.user_detailed import UserDetails

from model.subscription_request import UpgradeSubscriptionRequest
from model.subscription_response import SubscriptionUpgradeResponse
from service.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscription", tags=["Subscription"])


@router.post(
    "/upgrade",
    response_model=SubscriptionUpgradeResponse
)
def upgrade_subscription(
    payload: UpgradeSubscriptionRequest,
    current_user: UserDetails = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SubscriptionService(db)
    return service.upgrade_subscription(
        user=current_user,
        new_plan=payload.plan
    )