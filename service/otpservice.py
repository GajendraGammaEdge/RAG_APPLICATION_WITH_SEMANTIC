from fastapi import HTTPException, BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session
from service.notification_service import sending_mail
from utils.otp_generator import OTPgenerator
from db_configuration.config import settings
from constant.email_subject import FORGOT_PASSWORD
from schema.user_otp import UserOtp
from model.user_info import ForgotPwd, Otpverification, ResendOtp
from schema.user_detailed import UserDetails
from encryption_and_jwt.pass_hashing import get_hashed_password

class OtpSerivces:

    def __init__(self, db: Session):
        self.db = db

    def forgotpwd(self, usermail: ForgotPwd, background_tasks: BackgroundTasks):  # Added background_tasks
        email = usermail.user_email
        user = self.db.query(UserDetails).filter(
            UserDetails.email == email,
        ).first()

        print(f"User_emailid_forgotpwd{usermail}")
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"This user_name is not correct, enter the correct one: {email}"
            )

        print(f"user_info {user.user_name}")
        username = user.user_name
        user_id = user.id
        one_time_otp = OTPgenerator()
        curr_time = datetime.now()
        validate_time = settings.otp_expiration_time

        # Check if user is verifying or generating OTP for the first time
        user_verfiying = self.db.query(UserOtp).filter(
            UserOtp.user_id == user_id
        ).first()

        if not user_verfiying:
            userotp = {
                "otp_number": one_time_otp,
                "user_id": user_id,
                "email": email,
                "expired_time": validate_time,
                "created_time": datetime.now(),
                "update_time": datetime.now()
            }
            new_userotp = UserOtp(**userotp)
            self.db.add(new_userotp)
            self.db.commit()
        else:
            # Updating the OTP table for the user
            user_verfiying.update_time = datetime.now()
            user_verfiying.otp_number = one_time_otp
            user_verfiying.expired_time = validate_time
            self.db.add(user_verfiying)
            self.db.commit()

        body = {
            "username": username,
            "curr_time": curr_time,
            "one_time_otp": one_time_otp,
            "validate_time": validate_time
        }

        print("email_sending_started")
        # Send the email in the background
        background_tasks.add_task(sending_mail, subject=FORGOT_PASSWORD, email_to=email, body=body)
        print("email_ended_successfully")
        
        return {
            "message": "Open your user_mail id to get the otp"
        }

    def updatepassword(self, user_info: Otpverification):
        user_mailid = user_info.user_email
        userotp_curr = user_info.otp
        user = self.db.query(UserDetails).filter(
            UserDetails.email == user_mailid,
        ).first()
        
        if not user:
            raise ValueError("User is not found")

        user_verfiying = self.db.query(UserOtp).filter(
            UserOtp.user_id == user.id
        ).first()
        userotp = user_verfiying.otp_number

        if userotp_curr != userotp:
            raise HTTPException(
                status_code=422,
                detail="Your OTP does not match. Please enter the correct one."
            )

        # Update password
        pwd = user_info.password
        hash_pwd = get_hashed_password(pwd)
        user.password = hash_pwd
        self.db.add(user)
        self.db.commit()

        return {
            "message": "User password is successfully updated"
        }

    def resendotp(self, resend: ResendOtp, background_tasks: BackgroundTasks):  # Added background_tasks
        email = resend.user_email
        user = self.db.query(UserDetails).filter(
            UserDetails.email == email,
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"This user_name is not correct, enter the correct one: {email}"
            )

        print(f"user_info {user.user_name}")
        username = user.user_name
        user_id = user.id
        one_time_otp = OTPgenerator()
        curr_time = datetime.now()
        validate_time = settings.otp_expiration_time

        user_verfiying = self.db.query(UserOtp).filter(
            UserOtp.user_id == user_id
        ).first()

        if not user_verfiying:
            userotp = {
                "otp_number": one_time_otp,
                "user_id": user_id,
                "email" : email,
                "expired_time": validate_time,
                "created_time": datetime.now(),
                "update_time": datetime.now()
            }
            new_userotp = UserOtp(**userotp)
            self.db.add(new_userotp)
            self.db.commit()
        else:
            user_verfiying.update_time = datetime.now()
            user_verfiying.otp_number = one_time_otp
            user_verfiying.expired_time = validate_time
            self.db.add(user_verfiying)
            self.db.commit()

        body = {
            "username": username,
            "curr_time": curr_time,
            "one_time_otp": one_time_otp,
            "validate_time": validate_time
        }

        background_tasks.add_task(sending_mail, subject=FORGOT_PASSWORD, email_to=email, body=body)
        
        return {
            "message": "Please check your mail. OTP has been resent to your email."
        }