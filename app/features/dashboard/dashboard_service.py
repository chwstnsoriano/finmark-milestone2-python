import time

from app.config import CACHE_TTL_SECONDS
from app.services.financial_service import get_financial_summary
from app.services.order_service import get_order_summary
from app.services.payment_service import get_payment_summary
from app.services.product_service import get_product_summary
from app.utils.audit_logger import log_action

CACHE = {}


def get_dashboard_summary(user: dict):
    start_time = time.perf_counter()

    role = user.get("role", "unknown")
    department = user.get("department", "unknown")
    email = user.get("email", "unknown")

    cache_key = f"dashboard:{role}:{department}"
    current_time = time.time()

    cached_response = CACHE.get(cache_key)

    if cached_response:
        cache_age = current_time - cached_response["created_at"]

        if cache_age < CACHE_TTL_SECONDS:
            response = cached_response["data"]
            response["cache_status"] = "hit"
            response["load_time_ms"] = round((time.perf_counter() - start_time) * 1000, 2)

            log_action(
                action="dashboard_accessed_cache_hit",
                actor_email=email,
                details="Dashboard data served from in-memory cache."
            )

            return response

    try:
        financials = get_financial_summary(role, department)
    except Exception as error:
        financials = {
            "source": "Financial Service Fallback",
            "scope": "fallback",
            "total_revenue": 0,
            "total_expenses": 0,
            "net_profit": 0,
            "error": str(error)
        }

    try:
        orders = get_order_summary(role, department)
    except Exception as error:
        orders = {
            "source": "Order Service Fallback",
            "scope": "fallback",
            "total_orders": 0,
            "orders": [],
            "error": str(error)
        }

    try:
        payments = get_payment_summary(role, department)
    except Exception as error:
        payments = {
            "source": "Payment Service Fallback",
            "scope": "fallback",
            "total_payment_records": 0,
            "successful_payments": 0,
            "pending_payments": 0,
            "failed_payments": 0,
            "error": str(error)
        }

    try:
        products = get_product_summary(role, department)
    except Exception as error:
        products = {
            "source": "Product Service Fallback",
            "scope": "fallback",
            "active_products": 0,
            "low_stock_products": 0,
            "active_services": 0,
            "error": str(error)
        }

    response = {
        "user_scope": {
            "role": role,
            "department": department
        },
        "financials": financials,
        "orders": orders,
        "payments": payments,
        "products": products,
        "optimization_used": "SQLite-backed services with in-memory dashboard caching and fallback responses",
        "performance_target": "Dashboard response should remain below 3 seconds under normal prototype usage.",
        "cache_status": "miss",
        "load_time_ms": round((time.perf_counter() - start_time) * 1000, 2)
    }

    CACHE[cache_key] = {
        "created_at": current_time,
        "data": response
    }

    log_action(
        action="dashboard_accessed",
        actor_email=email,
        details="Dashboard data retrieved from database-backed services."
    )

    return response