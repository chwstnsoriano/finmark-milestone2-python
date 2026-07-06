from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Body
from pydantic import BaseModel

from app.features.auth.auth_service import register_user, login_user
from app.utils.security import decode_access_token

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


@router.post("/register")
def register(payload: Optional[RegisterRequest] = Body(default=None)):
    if payload is None:
        raise HTTPException(status_code=400, detail="Request body is required.")

    try:
        user = register_user(
            payload.name,
            payload.email,
            payload.password,
            payload.role,
            payload.department
        )

        return {
            "message": "User registered successfully",
            "user": user
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        raise HTTPException(status_code=500, detail="Unable to register user.")


@router.post("/login")
def login(payload: Optional[LoginRequest] = Body(default=None)):
    if payload is None:
        raise HTTPException(status_code=400, detail="Request body is required.")

    try:
        result = login_user(payload.email, payload.password)

        return {
            "message": "Login successful",
            "token": result["token"],
            "user": result["user"]
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except PermissionError as error:
        raise HTTPException(status_code=401, detail=str(error))

    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong during login.")


@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Valid authorization token is required.")

    token = authorization.replace("Bearer ", "")

    try:
        user = decode_access_token(token)

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "department": user["department"]
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")