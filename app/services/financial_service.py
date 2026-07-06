from app.database import get_payments, get_service_orders


def get_financial_summary(role: str, department: str):
    orders = get_service_orders()
    payments = get_payments()

    projected_revenue = 0
    confirmed_revenue = 0
    pending_revenue = 0

    for order in orders:
        projected_revenue += order["base_price"]

    for payment in payments:
        status = payment["payment_status"].lower()

        if status in ["paid", "completed", "successful"]:
            confirmed_revenue += payment["amount"]

        if status == "pending":
            pending_revenue += payment["amount"]

    estimated_expenses = round(projected_revenue * 0.35, 2)
    estimated_profit = round(projected_revenue - estimated_expenses, 2)

    return {
        "source": "Financial Service - SQLite Orders and Payments",
        "scope": "all FinMark service orders",
        "total_revenue": projected_revenue,
        "total_expenses": estimated_expenses,
        "net_profit": estimated_profit,
        "projected_revenue": projected_revenue,
        "confirmed_revenue": confirmed_revenue,
        "pending_revenue": pending_revenue,
        "total_service_orders": len(orders),
        "total_payment_records": len(payments)
    }