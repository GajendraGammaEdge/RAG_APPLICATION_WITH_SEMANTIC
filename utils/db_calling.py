from sqlalchemy.orm import Session
from schema.user_detailed import UserDetails


def get_user_by_id(db: Session, user_id: int) -> UserDetails | None:
    return db.query(UserDetails).filter(UserDetails.id == user_id).first()
