def get_order_summary(role: str, department: str):
    all_orders = [
        {"status": "completed", "count": 125},
        {"status": "pending", "count": 18},
        {"status": "processing", "count": 32},
        {"status": "failed", "count": 4}
    ]

    if role == "operations":
        return {
            "source": "Order Service Placeholder",
            "scope": department,
            "orders": [
                {"status": "processing", "count": 32},
                {"status": "failed", "count": 4}
            ]
        }

    return {
        "source": "Order Service Placeholder",
        "scope": "all departments",
        "orders": all_orders
    }