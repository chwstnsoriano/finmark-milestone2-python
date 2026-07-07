import sqlite3
import re

from app.database import create_user, find_user_by_email
from app.utils.security import hash_password, verify_password, create_access_token


STANDARD_MINI_EMAIL = re.compile(r"^(?P<local_part>[\w\-]+([\.%\+][\w\-]+){0,})@(?P<domain>([a-zA-Z0-9](-*[a-zA-Z0-9]+){0,})(\.[\w]+){1,})$")
ALLOWED_ROLES = ["coo", "admin", "finance", "operations", "staff", "customer"]


def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


# def validate_email(email: str):
#     if "@" not in email or "." not in email:
#         raise ValueError("A valid email address is required.")


# Simple syntax-based email validation. Covers most email addresses
# that comply with the RFC standard that follow this common format:
# local-part@domain. Does not currently account for email provider
# rules like those from Gmail, so the address -.-@gmail.com works in
# the RFC syntax rules, but Gmail will reject this.
def validate_email(email: str):
    email_matches = STANDARD_MINI_EMAIL.match(email)
    if not email_matches:
        raise ValueError("A valid email address is required.")
    elif len(email) > 254:
        raise ValueError("Full email address must be shorter than 255 characters.")
    elif len(email_matches.group("local_part")) > 64:
        raise ValueError("First section of address must be less than 64 characters.")


def register_user(name: str, email: str, password: str, role: str, department: str):
    name = clean_text(name)
    email = clean_text(email).lower()
    password = clean_text(password)
    role = clean_text(role).lower()
    department = clean_text(department).lower()

    if not name:
        raise ValueError("Name is required.")

    if not email:
        raise ValueError("Email is required.")

    validate_email(email)

    if not password:
        raise ValueError("Password is required.")

    if len(password) < 8:
        raise ValueError("Password is too short. Minimum password length is 8 characters.")

    if not role:
        raise ValueError("Role is required.")

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid role selected.")

    if not department:
        raise ValueError("Department is required.")

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
    email = clean_text(email).lower()
    password = clean_text(password)

    if not email:
        raise ValueError("Email is required.")

    validate_email(email)

    if not password:
        raise ValueError("Password is required.")

    user = find_user_by_email(email)

    if not (
        user
        and verify_password(password, user["password_hash"])
    ):
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