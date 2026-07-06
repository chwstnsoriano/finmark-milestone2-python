from app.database import (
    create_payment,
    create_service_order,
    find_service_by_id,
    get_service_catalog,
    get_service_orders
)
from app.services.event_bus_service import publish_event
from app.utils.audit_logger import log_action


ALLOWED_CLIENT_TYPES = [
    "retail",
    "e-commerce",
    "healthcare",
    "manufacturing",
    "other"
]


def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def validate_email(email: str):
    if "@" not in email or "." not in email:
        raise ValueError("A valid customer email address is required.")


def list_services():
    return get_service_catalog()


def place_service_order(
    customer_name,
    customer_email,
    client_type,
    service_id,
    order_notes=None
):
    customer_name = clean_text(customer_name)
    customer_email = clean_text(customer_email).lower()
    client_type = clean_text(client_type).lower()
    order_notes = clean_text(order_notes)

    if not customer_name:
        raise ValueError("Customer name is required.")

    if not customer_email:
        raise ValueError("Customer email is required.")

    validate_email(customer_email)

    if not client_type:
        raise ValueError("Client type is required.")

    if client_type not in ALLOWED_CLIENT_TYPES:
        raise ValueError("Invalid client type selected.")

    if service_id is None:
        raise ValueError("Service selection is required.")

    try:
        service_id = int(service_id)
    except ValueError:
        raise ValueError("Service selection must be a valid number.")

    service = find_service_by_id(service_id)

    if not service:
        raise ValueError("Selected FinMark service was not found.")

    order_id = create_service_order(
        customer_name=customer_name,
        customer_email=customer_email,
        client_type=client_type,
        service_id=service_id,
        order_notes=order_notes
    )

    payment_id = create_payment(
        order_id=order_id,
        amount=service["base_price"],
        payment_status="pending",
        payment_method="simulation"
    )

    publish_event(
        event_type="service_order_created",
        source_service="Order Service",
        payload={
            "order_id": order_id,
            "customer_email": customer_email,
            "client_type": client_type,
            "service_name": service["service_name"],
            "status": "pending"
        }
    )

    publish_event(
        event_type="payment_record_created",
        source_service="Payment Service",
        payload={
            "payment_id": payment_id,
            "order_id": order_id,
            "amount": service["base_price"],
            "status": "pending"
        }
    )

    log_action(
        action="service_order_created",
        actor_email=customer_email,
        details=f"{customer_name} created a service order for {service['service_name']}."
    )

    return {
        "order_id": order_id,
        "payment_id": payment_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "client_type": client_type,
        "service": service,
        "order_status": "pending",
        "payment_status": "pending"
    }


def list_service_orders():
    return get_service_orders()


def get_order_summary(role: str, department: str):
    orders = get_service_orders()

    status_counts = {}

    for order in orders:
        status = order["order_status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    summary = [
        {
            "status": status,
            "count": count
        }
        for status, count in status_counts.items()
    ]

    if not summary:
        summary = [
            {
                "status": "pending",
                "count": 0
            }
        ]

    if role == "operations":
        scope = department
    else:
        scope = "all departments"

    return {
        "source": "Order Service - SQLite Service Orders",
        "scope": scope,
        "total_orders": len(orders),
        "orders": summary
    }