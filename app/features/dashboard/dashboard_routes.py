from typing import Optional

from fastapi import APIRouter, HTTPException, Header

from app.features.dashboard.dashboard_service import get_dashboard_summary
from app.utils.security import decode_access_token

router = APIRouter()


@router.get("/summary")
def dashboard_summary(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Valid authorization token is required.")

    token = authorization.replace("Bearer ", "")

    try:
        user = decode_access_token(token)

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    if user["role"] == "customer":
        raise HTTPException(
            status_code=403,
            detail="Customers can place service orders but cannot access the employee dashboard."
        )

    return get_dashboard_summary(user)