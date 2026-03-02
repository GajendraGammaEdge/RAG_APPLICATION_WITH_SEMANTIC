from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_configuration.pgdb_config import get_db
from utils.security import get_current_user
from schema.user_detailed import UserDetails
from schema.subscription_request import UpgradeSubscriptionRequest
from service.subscription_request import SubscriptionService

router = APIRouter(prefix="/subscription", tags=["Subscription"])


@router.post("/upgrade")
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