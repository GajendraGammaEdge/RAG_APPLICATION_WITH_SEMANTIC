from fastapi import APIRouter, BackgroundTasks, Depends
from service.otpservice import OtpSerivces
from model.user_info import ForgotPwd, Otpverification, ResendOtp
from sqlalchemy.orm import Session
from db_configuration.pgdb_config import get_db

router = APIRouter()


@router.post("/forgot-password")
def forgotpwd(user_email: ForgotPwd, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    service = OtpSerivces(db)
    return service.forgotpwd(user_email, background_tasks)  # Pass background_tasks


@router.patch("/updatingpassword")
def updatepwd(user_info: Otpverification, db: Session = Depends(get_db)):
    service = OtpSerivces(db)
    return service.updatepassword(user_info)


@router.post("/resendotp")
def resendopt(resendotp: ResendOtp, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    service = OtpSerivces(db)
    return service.resendotp(resendotp, background_tasks)  # Pass background_tasks