from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

Algorithm = os.getenv("ALGORITHM")
Token_expire_time = int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME", 30))  # default 30 minutes

with open("key/private_key.pem", "rb") as f:
    PRIVATE_KEY = f.read()

with open("key/public_key.pem", "rb") as f:
    PUBLIC_KEY = f.read()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=Token_expire_time)
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        PRIVATE_KEY,
        algorithm=Algorithm
    )
    return token


def verify_token(token: str):
    payload = jwt.decode(
        token,
        PUBLIC_KEY,
        algorithms=[Algorithm]
    )
    return payload
