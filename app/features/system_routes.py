from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from app.services.financial_service import get_financial_summary
from app.services.order_service import get_order_summary
from app.services.payment_service import get_payment_summary
from app.services.product_service import get_product_summary
from app.utils.security import decode_access_token

router = APIRouter()


def get_user_from_token(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Valid authorization token is required.")

    token = authorization.replace("Bearer ", "")

    try:
        return decode_access_token(token)

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")


@router.get("/orders/summary")
def orders_summary(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)

    return get_order_summary(user["role"], user["department"])


@router.get("/financials/summary")
def financials_summary(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)

    return get_financial_summary(user["role"], user["department"])


@router.get("/payments/summary")
def payments_summary(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)

    return get_payment_summary(user["role"], user["department"])


@router.get("/products/summary")
def products_summary(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)

    return get_product_summary(user["role"], user["department"])


@router.get("/system/services")
def system_services():
    return {
        "auth_service": "working",
        "dashboard_service": "working",
        "order_service": "database-backed",
        "product_service": "database-backed service catalog",
        "payment_service": "database-backed",
        "financial_service": "database-backed",
        "cache": "simple in-memory cache",
        "database": "SQLite prototype database",
        "audit_log_storage": "working",
        "event_bus": "working"
    }