import hashlib
from passlib.context import CryptContext

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def _pre_hash(password: str) -> str:
    """
    Pre-hash using SHA256 to avoid bcrypt 72-byte limitation.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_hashed_password(password: str) -> str:
    return password_context.hash(_pre_hash(password))


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(_pre_hash(password), hashed_pass)
