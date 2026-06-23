from fastapi import APIRouter, Header, HTTPException, Depends

from app.utils.security import decode_access_token
from app.features.dashboard.dashboard_service import get_dashboard_summary

router = APIRouter()


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is required.")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format.")

    token = authorization.replace("Bearer ", "")

    try:
        return decode_access_token(token)

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")


@router.get("/summary")
def dashboard_summary(current_user: dict = Depends(get_current_user)):
    try:
        return get_dashboard_summary(current_user)

    except Exception:
        raise HTTPException(status_code=500, detail="Unable to load dashboard summary.")