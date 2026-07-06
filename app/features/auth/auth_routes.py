from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Body
from pydantic import BaseModel

from app.features.auth.auth_service import register_user, login_user
from app.utils.security import decode_access_token
from app.utils.audit_logger import log_action

router = APIRouter()


class RegisterRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None


class LoginRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


def get_payload_email(payload):
    if payload is None or not getattr(payload, "email", None):
        return None

    return str(payload.email).strip().lower()


@router.post("/register")
def register(payload: Optional[RegisterRequest] = Body(default=None)):
    if payload is None:
        log_action(
            action="register_failed",
            actor_email=None,
            details="Request body is required."
        )
        raise HTTPException(status_code=400, detail="Request body is required.")

    try:
        user = register_user(
            payload.name,
            payload.email,
            payload.password,
            payload.role,
            payload.department
        )

        log_action(
            action="user_registered",
            actor_email=user["email"],
            details=f"New user registered with role: {user['role']}"
        )

        return {
            "message": "User registered successfully",
            "user": user
        }

    except ValueError as error:
        log_action(
            action="register_validation_failed",
            actor_email=get_payload_email(payload),
            details=str(error)
        )
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        log_action(
            action="register_system_error",
            actor_email=get_payload_email(payload),
            details="Unable to register user."
        )
        raise HTTPException(status_code=500, detail="Unable to register user.")


@router.post("/login")
def login(payload: Optional[LoginRequest] = Body(default=None)):
    if payload is None:
        log_action(
            action="login_failed",
            actor_email=None,
            details="Request body is required."
        )
        raise HTTPException(status_code=400, detail="Request body is required.")

    try:
        result = login_user(payload.email, payload.password)

        log_action(
            action="login_success",
            actor_email=result["user"]["email"],
            details="User logged in successfully."
        )

        return {
            "message": "Login successful",
            "token": result["token"],
            "user": result["user"]
        }

    except ValueError as error:
        log_action(
            action="login_validation_failed",
            actor_email=get_payload_email(payload),
            details=str(error)
        )
        raise HTTPException(status_code=400, detail=str(error))

    except PermissionError as error:
        log_action(
            action="login_failed",
            actor_email=get_payload_email(payload),
            details=str(error)
        )
        raise HTTPException(status_code=401, detail=str(error))

    except Exception:
        log_action(
            action="login_system_error",
            actor_email=get_payload_email(payload),
            details="Something went wrong during login."
        )
        raise HTTPException(status_code=500, detail="Something went wrong during login.")


@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Valid authorization token is required.")

    token = authorization.replace("Bearer ", "")

    try:
        user = decode_access_token(token)

        log_action(
            action="profile_accessed",
            actor_email=user["email"],
            details="Current user profile was requested."
        )

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "department": user["department"]
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")