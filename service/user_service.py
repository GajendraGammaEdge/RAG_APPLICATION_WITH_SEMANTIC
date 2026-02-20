from schema.user_detailed import UserDetails
from sqlalchemy.orm import Session
from fastapi import HTTPException
from model.user_info import Signup, Login
from encryption_and_jwt.pass_hashing import (
     get_hashed_password,
     verify_password,
     )
from utils.helper import calculate_age
from encryption_and_jwt.jwt_handler import create_access_token
from sqlalchemy import or_
from utils.db_calling import get_user_by_id


class UserServices():
    def __init__(self, db: Session):
        self.db = db

    async def sign_up(self, user_data: Signup):
        existing_user_mail = self.db.query(UserDetails).filter(
            or_(
                UserDetails.email == user_data.email,
                UserDetails.user_name == user_data.user_name
            )
        ).first()
        if existing_user_mail:
            raise HTTPException(
                status_code=409,
                detail="User is already present with this username or email",
                )

        age_get = calculate_age(user_data.dob)
        hash_password = get_hashed_password(user_data.password)

        new_user = UserDetails(**user_data.model_dump())
        new_user.password = hash_password
        new_user.age = age_get

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        token = create_access_token({
            "sub": str(new_user.id),
            "email": new_user.email,
            "user_name": new_user.user_name
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "user_name": new_user.user_name,
                "email": new_user.email
            }
        }

    async def login(self, login_data: Login):
        user = self.db.query(UserDetails).filter(
            or_(
                UserDetails.email == login_data.user_name,
                UserDetails.user_name == login_data.user_name
            )
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Credential Is not correct",
                )

        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Credential is not correct",
                )

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "user_name": user.user_name
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    @staticmethod
    def fetch_user_context(db: Session, user_id: int) -> dict:
        user = get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        return {
            "user_name": user.user_name,
            "age": user.age,
            "profession": user.profession
        }
