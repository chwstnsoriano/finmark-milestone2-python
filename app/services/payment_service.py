from app.database import get_payments


def get_payment_summary(role: str, department: str):
    payments = get_payments()

    successful_statuses = ["paid", "completed", "successful"]
    pending_statuses = ["pending"]
    failed_statuses = ["failed", "cancelled"]

    successful_payments = 0
    pending_payments = 0
    failed_payments = 0
    total_payment_amount = 0

    for payment in payments:
        status = payment["payment_status"].lower()

        total_payment_amount += payment["amount"]

        if status in successful_statuses:
            successful_payments += 1
        elif status in pending_statuses:
            pending_payments += 1
        elif status in failed_statuses:
            failed_payments += 1

    return {
        "source": "Payment Service - SQLite Payments",
        "scope": "all payment records",
        "total_payment_records": len(payments),
        "successful_payments": successful_payments,
        "pending_payments": pending_payments,
        "failed_payments": failed_payments,
        "total_payment_amount": total_payment_amount,
        "recent_payments": payments[:5]
    }