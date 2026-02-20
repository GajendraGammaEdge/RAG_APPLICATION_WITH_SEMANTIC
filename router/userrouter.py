from fastapi import APIRouter, Depends
from db_configuration.pgdb_config import get_db
from model.user_info import Signup, Login
from service.user_service import UserServices
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/signup")
async def signup(user: Signup, db: Session = Depends(get_db)):
    userservice = UserServices(db)
    return await userservice.sign_up(user)


@router.post("/login")
async def login(login_data: Login, db: Session = Depends(get_db)):
    service = UserServices(db)
    return await service.login(login_data)
