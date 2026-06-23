import hashlib
import jwt
from datetime import datetime, timedelta, timezone

from app.config import SECRET_KEY, PASSWORD_SALT, TOKEN_ALGORITHM


def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        PASSWORD_SALT.encode(),
        100000
    ).hex()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_access_token(user: dict) -> str:
    payload = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "department": user["department"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=TOKEN_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])