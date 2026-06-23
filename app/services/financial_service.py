def get_financial_summary(role: str, department: str):
    if role == "operations":
        return {
            "source": "Financial Service Placeholder",
            "scope": department,
            "total_revenue": 95000,
            "total_expenses": 52000,
            "net_profit": 43000
        }

    return {
        "source": "Financial Service Placeholder",
        "scope": "all departments",
        "total_revenue": 375000,
        "total_expenses": 167000,
        "net_profit": 208000
    }