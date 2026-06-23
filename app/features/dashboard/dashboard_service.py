import time

from app.config import CACHE_TTL_SECONDS
from app.services.order_service import get_order_summary
from app.services.financial_service import get_financial_summary
from app.services.payment_service import get_payment_summary
from app.services.product_service import get_product_summary

CACHE = {}


def get_dashboard_summary(user: dict):
    start_time = time.perf_counter()

    role = user["role"]
    department = user["department"]

    cache_key = f"dashboard:{role}:{department}"
    current_time = time.time()

    if cache_key in CACHE:
        cached_at, cached_data = CACHE[cache_key]

        if current_time - cached_at <= CACHE_TTL_SECONDS:
            load_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

            return {
                **cached_data,
                "cache_status": "hit",
                "load_time_ms": load_time_ms
            }

    financials = get_financial_summary(role, department)
    orders = get_order_summary(role, department)
    payments = get_payment_summary(role, department)
    products = get_product_summary(role, department)

    response = {
        "user_scope": {
            "role": role,
            "department": department
        },
        "financials": financials,
        "orders": orders,
        "payments": payments,
        "products": products,
        "optimization_used": [
            "Role-based access",
            "Reduced unnecessary data pulls",
            "Simple in-memory cache",
            "Dashboard API aggregation",
            "Response time logging"
        ],
        "performance_target": "Dashboard should load under 3 seconds."
    }

    CACHE[cache_key] = (current_time, response)

    load_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return {
        **response,
        "cache_status": "miss",
        "load_time_ms": load_time_ms
    }