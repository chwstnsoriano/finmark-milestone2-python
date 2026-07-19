from typing import Any

import httpx

from app.config import (
    ORDER_SERVICE_TIMEOUT_SECONDS,
    ORDER_SERVICE_URL,
)


class OrderServiceUnavailableError(RuntimeError):
    """Raised when the external Order Service cannot be reached."""


class OrderServiceResponseError(RuntimeError):
    """Raised when the external Order Service rejects a request."""

    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def external_order_service_enabled() -> bool:
    """Return whether an external Order Service URL is configured."""

    return bool(ORDER_SERVICE_URL)


def build_url(path: str) -> str:
    cleaned_path = path.lstrip("/")
    return f"{ORDER_SERVICE_URL}/{cleaned_path}"


def extract_error_detail(
    payload: Any,
    default_message: str,
) -> str:
    if isinstance(payload, dict):
        detail = payload.get("detail")

        if isinstance(detail, str) and detail.strip():
            return detail.strip()

        message = payload.get("message")

        if isinstance(message, str) and message.strip():
            return message.strip()

    return default_message


def request_order_service(
    method: str,
    path: str,
    json_body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Send one request to the external Order Service."""

    if not external_order_service_enabled():
        raise OrderServiceUnavailableError(
            "External Order Service is not configured."
        )

    url = build_url(path)

    try:
        response = httpx.request(
            method=method,
            url=url,
            json=json_body,
            timeout=ORDER_SERVICE_TIMEOUT_SECONDS,
        )

    except httpx.RequestError as error:
        raise OrderServiceUnavailableError(
            "External Order Service is temporarily unavailable."
        ) from error

    try:
        payload = response.json()
    except ValueError:
        payload = {}

    if response.status_code >= 500:
        detail = extract_error_detail(
            payload,
            "External Order Service encountered an error.",
        )

        raise OrderServiceUnavailableError(detail)

    if response.status_code >= 400:
        detail = extract_error_detail(
            payload,
            "External Order Service rejected the request.",
        )

        raise OrderServiceResponseError(
            status_code=response.status_code,
            detail=detail,
        )

    if not isinstance(payload, dict):
        raise OrderServiceUnavailableError(
            "External Order Service returned an invalid response."
        )

    return payload


def normalize_service(
    service: dict[str, Any],
) -> dict[str, Any]:
    """Support both external and original FinMark field names."""

    service_id = service.get(
        "service_id",
        service.get("id"),
    )

    service_name = service.get(
        "service_name",
        service.get("name"),
    )

    return {
        "service_id": service_id,
        "id": service_id,
        "service_name": service_name,
        "name": service_name,
        "base_price": service.get("base_price", 0),
        "category": service.get("category", ""),
        "description": service.get("description", ""),
        "is_active": service.get("is_active", True),
    }


def normalize_order(
    order: dict[str, Any],
) -> dict[str, Any]:
    """Convert an external order into the original UI-compatible shape."""

    order_id = order.get(
        "order_id",
        order.get("id"),
    )

    order_status = order.get(
        "order_status",
        order.get("status", "pending"),
    )

    return {
        "order_id": order_id,
        "id": order_id,
        "customer_name": order.get("customer_name", ""),
        "customer_email": order.get("customer_email", ""),
        "client_type": order.get("client_type", ""),
        "service_id": order.get("service_id"),
        "service_name": order.get("service_name", ""),
        "base_price": order.get("base_price", 0),
        "order_notes": order.get("order_notes", ""),
        "order_status": order_status,
        "status": order_status,
        "handled_by_instance": order.get(
            "handled_by_instance",
            "",
        ),
        "created_at": order.get("created_at"),
    }


def fetch_remote_services() -> list[dict[str, Any]]:
    payload = request_order_service(
        method="GET",
        path="/services",
    )

    services = payload.get("services", [])

    if not isinstance(services, list):
        raise OrderServiceUnavailableError(
            "External Order Service returned an invalid service catalog."
        )

    return [
        normalize_service(service)
        for service in services
        if isinstance(service, dict)
    ]


def create_remote_order(
    order_data: dict[str, Any],
) -> dict[str, Any]:
    payload = request_order_service(
        method="POST",
        path="/orders",
        json_body=order_data,
    )

    order = payload.get("order")

    if not isinstance(order, dict):
        raise OrderServiceUnavailableError(
            "External Order Service returned an invalid order."
        )

    return {
        "message": payload.get(
            "message",
            "Service order created successfully.",
        ),
        "instance_id": payload.get("instance_id", ""),
        "order": normalize_order(order),
    }


def fetch_remote_orders() -> list[dict[str, Any]]:
    payload = request_order_service(
        method="GET",
        path="/orders",
    )

    orders = payload.get("orders", [])

    if not isinstance(orders, list):
        raise OrderServiceUnavailableError(
            "External Order Service returned invalid order records."
        )

    return [
        normalize_order(order)
        for order in orders
        if isinstance(order, dict)
    ]


def fetch_remote_order_summary() -> dict[str, Any]:
    payload = request_order_service(
        method="GET",
        path="/orders/summary",
    )

    summary = payload.get("summary")

    if not isinstance(summary, dict):
        raise OrderServiceUnavailableError(
            "External Order Service returned an invalid summary."
        )

    return {
        "total_orders": int(
            summary.get("total_orders", 0)
        ),
        "pending_orders": int(
            summary.get("pending_orders", 0)
        ),
        "processing_orders": int(
            summary.get("processing_orders", 0)
        ),
        "completed_orders": int(
            summary.get("completed_orders", 0)
        ),
        "projected_revenue": float(
            summary.get("projected_revenue", 0)
        ),
        "instance_id": payload.get("instance_id", ""),
    }


def check_remote_order_service() -> dict[str, Any]:
    return request_order_service(
        method="GET",
        path="/health/ready",
    )
