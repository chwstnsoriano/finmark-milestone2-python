import sqlite3
from typing import Optional

from fastapi import APIRouter, HTTPException, Header

from app.database import DATABASE_NAME
from app.services.financial_service import get_financial_summary
from app.services.order_service import get_order_summary
from app.services.payment_service import get_payment_summary
from app.services.product_service import get_product_summary
from app.utils.resilience import get_rate_limit_status
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


def check_database_health():
    try:
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        required_tables = [
            "users",
            "service_catalog",
            "service_orders",
            "payments",
            "audit_logs",
            "event_bus"
        ]

        existing_tables = [
            table[0]
            for table in cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        ]

        missing_tables = [
            table
            for table in required_tables
            if table not in existing_tables
        ]

        connection.close()

        if missing_tables:
            return {
                "status": "degraded",
                "message": "Some required database tables are missing.",
                "missing_tables": missing_tables
            }

        return {
            "status": "healthy",
            "message": "All required prototype database tables are available."
        }

    except Exception as error:
        return {
            "status": "unavailable",
            "message": "Database health check failed.",
            "error": str(error)
        }


def safe_service_check(service_name, check_function):
    try:
        check_function()

        return {
            "status": "healthy",
            "fallback_available": True
        }

    except Exception as error:
        return {
            "status": "degraded",
            "fallback_available": True,
            "error": str(error)
        }


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


@router.get("/system/health")
def system_health():
    database_health = check_database_health()

    service_health = {
        "financial_service": safe_service_check(
            "financial_service",
            lambda: get_financial_summary("coo", "executive")
        ),
        "order_service": safe_service_check(
            "order_service",
            lambda: get_order_summary("coo", "executive")
        ),
        "payment_service": safe_service_check(
            "payment_service",
            lambda: get_payment_summary("coo", "executive")
        ),
        "product_service": safe_service_check(
            "product_service",
            lambda: get_product_summary("coo", "executive")
        )
    }

    has_degraded_service = any(
        service["status"] != "healthy"
        for service in service_health.values()
    )

    overall_status = "healthy"

    if database_health["status"] != "healthy" or has_degraded_service:
        overall_status = "degraded"

    return {
        "overall_status": overall_status,
        "database": database_health,
        "services": service_health,
        "rate_limiting": get_rate_limit_status(),
        "fallback_behavior": {
            "enabled": True,
            "message": "Dashboard service has fallback responses if a backend service fails."
        },
        "monitoring": {
            "audit_logs": "enabled",
            "event_bus_records": "enabled",
            "request_timing_headers": "enabled"
        }
    }


@router.get("/system/resilience")
def system_resilience():
    return {
        "message": "FinMark prototype resilience features are enabled.",
        "features": {
            "input_validation": "Missing, null, and invalid user inputs return clear error messages.",
            "rate_limiting": get_rate_limit_status(),
            "fallback_responses": "Dashboard returns safe fallback data if a service summary fails.",
            "audit_logging": "Important user and system actions are recorded in audit_logs.",
            "event_bus": "Service actions publish records to the event_bus table.",
            "database_health_check": "The system checks required SQLite prototype tables.",
            "request_monitoring": "Each request receives X-Process-Time-ms and gateway headers."
        }
    }