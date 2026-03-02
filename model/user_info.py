from pydantic import EmailStr , BaseModel
from datetime import date


class Signup(BaseModel):
    user_name : str
    first_name :str 
    last_name : str
    email : EmailStr
    password :str 
    dob : date


class Login(BaseModel):
    user_name: str 
    password : str     

class ForgotPwd(BaseModel):
    user_email: EmailStr

class Otpverification(BaseModel):
     user_email :EmailStr
     otp: str 
     password : str 
     enter_password: str

class ResendOtp(ForgotPwd):
    otp:str 