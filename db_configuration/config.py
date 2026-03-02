from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional
class Settings(BaseSettings):

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    port: Optional[int] = 8000
    server: Optional[str] = "localhost"

    secret_key: Optional[str] = None
    refresh_secret_key: Optional[str] = None
    algorithm: str = "RS256"
    access_token_expire_minutes: Optional[int] = 60
    refresh_token_expire_minutes: Optional[int] = 120

    adminapikey: Optional[str] = None
    openai_apikey: Optional[str] = None
    google_api_key: Optional[str] = None

    embedding_model_name: Optional[str] = None
    intfloat_embedding_model: Optional[str] = None
    baai_embedding_model: Optional[str] = None
    nomic_embedding_model: Optional[str] = None
    gemma_embedding_model: Optional[str] = None

    
    smtp_sender :Optional[str] = None
    smtp_password : Optional[str] = None
    smtp_server : Optional[str] = None
    smtp_port : Optional[int] = 587

    otp_expiration_time: Optional[int] = 10

    class Config:
        env_file = Path(".env")
        case_sensitive = False
        extra = "ignore"


settings = Settings()
