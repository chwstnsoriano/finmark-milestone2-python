from app.database import get_service_catalog


def get_product_summary(role: str, department: str):
    services = get_service_catalog()

    return {
        "source": "Product Service - SQLite Service Catalog",
        "scope": "FinMark service catalog",
        "active_products": len(services),
        "low_stock_products": 0,
        "active_services": len(services),
        "available_services": [
            {
                "id": service["id"],
                "service_name": service["service_name"],
                "service_category": service["service_category"],
                "base_price": service["base_price"]
            }
            for service in services
        ],
        "note": "Product Service is represented as FinMark's service catalog because FinMark provides business services."
    }