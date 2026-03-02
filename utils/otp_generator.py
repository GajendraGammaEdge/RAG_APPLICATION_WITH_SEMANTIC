import math
import random
import string

def OTPgenerator():
    digits_in_otp = string.digits + string.ascii_lowercase + string.ascii_uppercase  
    OTP = ""
    for i in range(8):
        OTP += random.choice(digits_in_otp)  
    return OTP