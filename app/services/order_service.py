from typing import Any

from app.config import ORDER_SERVICE_FALLBACK_ENABLED
from app.database import (
    create_payment,
    create_service_order,
    find_service_by_id,
    get_service_catalog,
    get_service_orders,
)
from app.services.event_bus_service import publish_event
from app.services.order_service_client import (
    OrderServiceResponseError,
    OrderServiceUnavailableError,
    create_remote_order,
    external_order_service_enabled,
    fetch_remote_order_summary,
    fetch_remote_orders,
    fetch_remote_services,
)
from app.utils.audit_logger import log_action


ALLOWED_CLIENT_TYPES = [
    "retail",
    "e-commerce",
    "healthcare",
    "manufacturing",
    "other",
]


def clean_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def validate_email(email: str) -> None:
    if "@" not in email or "." not in email:
        raise ValueError(
            "A valid customer email address is required."
        )


def validate_order_input(
    customer_name: Any,
    customer_email: Any,
    client_type: Any,
    service_id: Any,
    order_notes: Any = None,
) -> tuple[str, str, str, int, str]:
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
    except (TypeError, ValueError):
        raise ValueError(
            "Service selection must be a valid number."
        )

    return (
        customer_name,
        customer_email,
        client_type,
        service_id,
        order_notes,
    )


def list_services() -> list[dict[str, Any]]:
    if external_order_service_enabled():
        try:
            return fetch_remote_services()

        except (
            OrderServiceUnavailableError,
            OrderServiceResponseError,
        ) as error:
            if not ORDER_SERVICE_FALLBACK_ENABLED:
                raise

            log_action(
                action="order_service_catalog_fallback",
                actor_email=None,
                details=(
                    "External service catalog unavailable. "
                    f"Using SQLite fallback. Reason: {error}"
                ),
            )

    return get_service_catalog()


def place_local_service_order(
    customer_name: str,
    customer_email: str,
    client_type: str,
    service_id: int,
    order_notes: str,
    fallback_reason: str | None = None,
) -> dict[str, Any]:
    service = find_service_by_id(service_id)

    if not service:
        raise ValueError(
            "Selected FinMark service was not found."
        )

    order_id = create_service_order(
        customer_name=customer_name,
        customer_email=customer_email,
        client_type=client_type,
        service_id=service_id,
        order_notes=order_notes,
    )

    payment_id = create_payment(
        order_id=order_id,
        amount=service["base_price"],
        payment_status="pending",
        payment_method="simulation",
    )

    publish_event(
        event_type="service_order_created",
        source_service="Order Service",
        payload={
            "order_id": order_id,
            "customer_email": customer_email,
            "client_type": client_type,
            "service_name": service["service_name"],
            "status": "pending",
            "storage": "sqlite",
        },
    )

    publish_event(
        event_type="payment_record_created",
        source_service="Payment Service",
        payload={
            "payment_id": payment_id,
            "order_id": order_id,
            "amount": service["base_price"],
            "status": "pending",
        },
    )

    action = (
        "service_order_fallback_created"
        if fallback_reason
        else "service_order_created"
    )

    details = (
        f"{customer_name} created a service order for "
        f"{service['service_name']} using SQLite."
    )

    if fallback_reason:
        details += f" Fallback reason: {fallback_reason}"

    log_action(
        action=action,
        actor_email=customer_email,
        details=details,
    )

    return {
        "order_id": order_id,
        "payment_id": payment_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "client_type": client_type,
        "service": service,
        "order_status": "pending",
        "payment_status": "pending",
        "handled_by_instance": "local-finmark-app",
        "source": (
            "Local SQLite fallback"
            if fallback_reason
            else "Local SQLite Order Service"
        ),
    }


def create_local_mirror_for_remote_order(
    remote_result: dict[str, Any],
    customer_name: str,
    customer_email: str,
    client_type: str,
    service_id: int,
    order_notes: str,
) -> tuple[int | None, int | None]:
    remote_order = remote_result["order"]

    try:
        local_order_id = create_service_order(
            customer_name=customer_name,
            customer_email=customer_email,
            client_type=client_type,
            service_id=service_id,
            order_notes=order_notes,
        )

        payment_id = create_payment(
            order_id=local_order_id,
            amount=remote_order["base_price"],
            payment_status="pending",
            payment_method="simulation",
        )

        publish_event(
            event_type="service_order_created",
            source_service="External Order Service",
            payload={
                "external_order_id": remote_order["order_id"],
                "local_mirror_order_id": local_order_id,
                "customer_email": customer_email,
                "client_type": client_type,
                "service_name": remote_order["service_name"],
                "status": remote_order["order_status"],
                "handled_by_instance": remote_result.get(
                    "instance_id",
                    "",
                ),
                "storage": "postgresql",
            },
        )

        publish_event(
            event_type="payment_record_created",
            source_service="Payment Service",
            payload={
                "payment_id": payment_id,
                "local_order_id": local_order_id,
                "external_order_id": remote_order["order_id"],
                "amount": remote_order["base_price"],
                "status": "pending",
            },
        )

        log_action(
            action="external_service_order_created",
            actor_email=customer_email,
            details=(
                f"{customer_name} created external order "
                f"{remote_order['order_id']} for "
                f"{remote_order['service_name']}. "
                f"Handled by {remote_result.get('instance_id', '')}."
            ),
        )

        return local_order_id, payment_id

    except Exception as error:
        log_action(
            action="external_order_local_mirror_failed",
            actor_email=customer_email,
            details=(
                "The PostgreSQL order was created, but the "
                f"local mirror failed: {error}"
            ),
        )

        return None, None


def place_remote_service_order(
    customer_name: str,
    customer_email: str,
    client_type: str,
    service_id: int,
    order_notes: str,
) -> dict[str, Any]:
    remote_result = create_remote_order(
        {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "client_type": client_type,
            "service_id": service_id,
            "order_notes": order_notes,
        }
    )

    remote_order = remote_result["order"]

    local_order_id, payment_id = (
        create_local_mirror_for_remote_order(
            remote_result=remote_result,
            customer_name=customer_name,
            customer_email=customer_email,
            client_type=client_type,
            service_id=service_id,
            order_notes=order_notes,
        )
    )

    service = {
        "service_id": remote_order["service_id"],
        "id": remote_order["service_id"],
        "service_name": remote_order["service_name"],
        "name": remote_order["service_name"],
        "base_price": remote_order["base_price"],
    }

    return {
        "order_id": remote_order["order_id"],
        "external_order_id": remote_order["order_id"],
        "local_mirror_order_id": local_order_id,
        "payment_id": payment_id,
        "customer_name": remote_order["customer_name"],
        "customer_email": remote_order["customer_email"],
        "client_type": remote_order["client_type"],
        "service": service,
        "order_status": remote_order["order_status"],
        "payment_status": (
            "pending"
            if payment_id is not None
            else "local_record_not_created"
        ),
        "handled_by_instance": remote_result.get(
            "instance_id",
            remote_order.get("handled_by_instance", ""),
        ),
        "source": "External PostgreSQL Order Service",
    }


def place_service_order(
    customer_name: Any,
    customer_email: Any,
    client_type: Any,
    service_id: Any,
    order_notes: Any = None,
) -> dict[str, Any]:
    (
        customer_name,
        customer_email,
        client_type,
        service_id,
        order_notes,
    ) = validate_order_input(
        customer_name=customer_name,
        customer_email=customer_email,
        client_type=client_type,
        service_id=service_id,
        order_notes=order_notes,
    )

    if external_order_service_enabled():
        try:
            return place_remote_service_order(
                customer_name=customer_name,
                customer_email=customer_email,
                client_type=client_type,
                service_id=service_id,
                order_notes=order_notes,
            )

        except OrderServiceResponseError as error:
            raise ValueError(error.detail)

        except OrderServiceUnavailableError as error:
            if not ORDER_SERVICE_FALLBACK_ENABLED:
                raise

            return place_local_service_order(
                customer_name=customer_name,
                customer_email=customer_email,
                client_type=client_type,
                service_id=service_id,
                order_notes=order_notes,
                fallback_reason=str(error),
            )

    return place_local_service_order(
        customer_name=customer_name,
        customer_email=customer_email,
        client_type=client_type,
        service_id=service_id,
        order_notes=order_notes,
    )


def list_service_orders() -> list[dict[str, Any]]:
    if external_order_service_enabled():
        try:
            return fetch_remote_orders()

        except (
            OrderServiceUnavailableError,
            OrderServiceResponseError,
        ) as error:
            if not ORDER_SERVICE_FALLBACK_ENABLED:
                raise

            log_action(
                action="order_list_fallback",
                actor_email=None,
                details=(
                    "External order list unavailable. "
                    f"Using SQLite fallback. Reason: {error}"
                ),
            )

    return get_service_orders()


def local_order_summary(
    role: str,
    department: str,
) -> dict[str, Any]:
    orders = get_service_orders()
    status_counts: dict[str, int] = {}

    for order in orders:
        status = order["order_status"]
        status_counts[status] = (
            status_counts.get(status, 0) + 1
        )

    summary = [
        {
            "status": status,
            "count": count,
        }
        for status, count in status_counts.items()
    ]

    if not summary:
        summary = [
            {
                "status": "pending",
                "count": 0,
            }
        ]

    scope = (
        department
        if role == "operations"
        else "all departments"
    )

    return {
        "source": "Order Service - SQLite Service Orders",
        "scope": scope,
        "total_orders": len(orders),
        "orders": summary,
    }


def get_order_summary(
    role: str,
    department: str,
) -> dict[str, Any]:
    if external_order_service_enabled():
        try:
            remote_summary = fetch_remote_order_summary()

            status_values = [
                (
                    "pending",
                    remote_summary["pending_orders"],
                ),
                (
                    "processing",
                    remote_summary["processing_orders"],
                ),
                (
                    "completed",
                    remote_summary["completed_orders"],
                ),
            ]

            summary = [
                {
                    "status": status,
                    "count": count,
                }
                for status, count in status_values
                if count > 0
            ]

            if not summary:
                summary = [
                    {
                        "status": "pending",
                        "count": 0,
                    }
                ]

            scope = (
                department
                if role == "operations"
                else "all departments"
            )

            return {
                "source": (
                    "External Order Service - PostgreSQL"
                ),
                "scope": scope,
                "total_orders": remote_summary[
                    "total_orders"
                ],
                "orders": summary,
                "projected_revenue": remote_summary[
                    "projected_revenue"
                ],
                "instance_id": remote_summary[
                    "instance_id"
                ],
            }

        except (
            OrderServiceUnavailableError,
            OrderServiceResponseError,
        ) as error:
            if not ORDER_SERVICE_FALLBACK_ENABLED:
                raise

            log_action(
                action="order_summary_fallback",
                actor_email=None,
                details=(
                    "External order summary unavailable. "
                    f"Using SQLite fallback. Reason: {error}"
                ),
            )

    return local_order_summary(
        role=role,
        department=department,
    )
