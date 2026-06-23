from fastapi import APIRouter, Header, HTTPException, Depends

from app.utils.security import decode_access_token
from app.services.order_service import get_order_summary
from app.services.financial_service import get_financial_summary
from app.services.payment_service import get_payment_summary
from app.services.product_service import get_product_summary

router = APIRouter()


def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Valid authorization token is required.")

    token = authorization.replace("Bearer ", "")

    try:
        return decode_access_token(token)

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")


@router.get("/orders/summary")
def orders_summary(user: dict = Depends(get_current_user)):
    return get_order_summary(user["role"], user["department"])


@router.get("/financials/summary")
def financials_summary(user: dict = Depends(get_current_user)):
    return get_financial_summary(user["role"], user["department"])


@router.get("/payments/summary")
def payments_summary(user: dict = Depends(get_current_user)):
    return get_payment_summary(user["role"], user["department"])


@router.get("/products/summary")
def products_summary(user: dict = Depends(get_current_user)):
    return get_product_summary(user["role"], user["department"])


@router.get("/system/services")
def service_health():
    return {
        "auth_service": "working",
        "dashboard_service": "working",
        "order_service": "placeholder",
        "financial_service": "placeholder",
        "payment_service": "placeholder",
        "product_service": "placeholder",
        "cache": "simple in-memory cache",
        "database": "SQLite user database"
    }