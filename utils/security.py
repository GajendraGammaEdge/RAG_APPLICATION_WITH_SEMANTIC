from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from encryption_and_jwt.jwt_handler import verify_token
from db_configuration.pgdb_config import get_db
from schema.user_detailed import UserDetails


def get_current_user(
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    payload = token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(UserDetails).filter(UserDetails.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
