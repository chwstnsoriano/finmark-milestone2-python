import asyncio
import os
import re
import socket
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.database import (
    check_database,
    create_order,
    get_order_summary,
    get_service_catalog,
    initialize_database,
    list_orders,
)
from app.schemas import OrderCreate


INSTANCE_ID = os.getenv(
    "INSTANCE_ID",
    os.getenv("HOSTNAME", socket.gethostname()),
)

EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize PostgreSQL before accepting requests."""

    maximum_attempts = 15
    last_error: Exception | None = None

    for attempt in range(1, maximum_attempts + 1):
        try:
            initialize_database()

            print(
                f"Order Service database initialized "
                f"by instance {INSTANCE_ID}"
            )

            last_error = None
            break
        except Exception as error:
            last_error = error

            print(
                f"Database connection attempt "
                f"{attempt}/{maximum_attempts} failed: "
                f"{error.__class__.__name__}"
            )

            await asyncio.sleep(2)

    if last_error is not None:
        raise RuntimeError(
            "Order Service could not connect to PostgreSQL."
        ) from last_error

    yield

    print(f"Order Service instance {INSTANCE_ID} stopped.")


app = FastAPI(
    title="FinMark Order Service",
    version="1.0.0",
    description=(
        "Independent PostgreSQL-backed Order Service "
        "for the FinMark scalable architecture."
    ),
    lifespan=lifespan,
)


@app.get("/")
def service_information():
    return {
        "service": "FinMark Order Service",
        "status": "running",
        "instance_id": INSTANCE_ID,
    }


@app.get("/health/live")
def liveness_check():
    """Confirm that the application process is alive."""

    return {
        "status": "alive",
        "service": "order-service",
        "instance_id": INSTANCE_ID,
    }


@app.get("/health/ready")
def readiness_check():
    """Confirm that the service can reach PostgreSQL."""

    try:
        database_available = check_database()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Order Service database is unavailable.",
        )

    if not database_available:
        raise HTTPException(
            status_code=503,
            detail="Order Service is not ready.",
        )

    return {
        "status": "ready",
        "database": "connected",
        "instance_id": INSTANCE_ID,
    }


@app.get("/instance")
def instance_information():
    """Show which container handled the request."""

    return {
        "service": "order-service",
        "instance_id": INSTANCE_ID,
    }


@app.get("/services")
def service_catalog():
    try:
        services = get_service_catalog()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Service catalog database is unavailable.",
        )

    return {
        "count": len(services),
        "services": services,
        "instance_id": INSTANCE_ID,
    }


@app.post("/orders", status_code=201)
def place_order(order_data: OrderCreate):
    customer_name = order_data.customer_name.strip()
    customer_email = order_data.customer_email.strip().lower()
    client_type = order_data.client_type.strip()
    order_notes = order_data.order_notes.strip()

    if not customer_name:
        raise HTTPException(
            status_code=400,
            detail="Customer name is required.",
        )

    if not EMAIL_PATTERN.fullmatch(customer_email):
        raise HTTPException(
            status_code=400,
            detail="A valid customer email is required.",
        )

    if not client_type:
        raise HTTPException(
            status_code=400,
            detail="Client type is required.",
        )

    try:
        order = create_order(
            customer_name=customer_name,
            customer_email=customer_email,
            client_type=client_type,
            service_id=order_data.service_id,
            order_notes=order_notes,
            instance_id=INSTANCE_ID,
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Order Service database is unavailable.",
        )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="The selected FinMark service does not exist.",
        )

    return {
        "message": "Service order created successfully.",
        "instance_id": INSTANCE_ID,
        "order": order,
    }


@app.get("/orders")
def retrieve_orders(limit: int = 100):
    safe_limit = min(max(limit, 1), 500)

    try:
        orders = list_orders(safe_limit)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Order records are temporarily unavailable.",
        )

    return {
        "count": len(orders),
        "orders": orders,
        "instance_id": INSTANCE_ID,
    }


@app.get("/orders/summary")
def order_summary():
    try:
        summary = get_order_summary()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Order summary is temporarily unavailable.",
        )

    return {
        "summary": summary,
        "instance_id": INSTANCE_ID,
    }