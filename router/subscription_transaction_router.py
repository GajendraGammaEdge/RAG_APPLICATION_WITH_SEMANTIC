from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_configuration.pgdb_config import get_db
from utils.security import get_current_user
from schema.user_detailed import UserDetails
from service.subscription_transaction_service import SubscriptionTransactionService

router = APIRouter(
    prefix="/subscription/transactions",
    tags=["Subscription"]
)


@router.get("")
def get_my_transactions(
    current_user: UserDetails = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = SubscriptionTransactionService(db)
    return service.get_user_transactions(current_user.id)