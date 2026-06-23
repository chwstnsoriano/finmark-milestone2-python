import sqlite3

from app.database import create_user, find_user_by_email
from app.utils.security import hash_password, verify_password, create_access_token


ALLOWED_ROLES = ["coo", "admin", "finance", "operations", "staff"]


def register_user(name: str, email: str, password: str, role: str, department: str):
    if not name or not email or not password or not role or not department:
        raise ValueError("All fields are required.")

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid role selected.")

    existing_user = find_user_by_email(email)

    if existing_user:
        raise ValueError("Email is already registered.")

    password_hash = hash_password(password)

    try:
        user_id = create_user(name, email, password_hash, role, department)
    except sqlite3.IntegrityError:
        raise ValueError("Email is already registered.")

    return {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "department": department
    }


def login_user(email: str, password: str):
    if not email or not password:
        raise ValueError("Email and password are required.")

    user = find_user_by_email(email)

    if not user:
        raise PermissionError("Invalid email or password.")

    if not verify_password(password, user["password_hash"]):
        raise PermissionError("Invalid email or password.")

    token = create_access_token(user)

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "department": user["department"]
        }
    }