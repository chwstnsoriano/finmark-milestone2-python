from typing import Optional

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from app.services.order_service import (
    list_services,
    list_service_orders,
    place_service_order
)
from app.utils.audit_logger import log_action

router = APIRouter()


class ServiceOrderRequest(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    client_type: Optional[str] = None
    service_id: Optional[int] = None
    order_notes: Optional[str] = None


@router.get("/services/catalog")
def service_catalog():
    return {
        "message": "FinMark service catalog retrieved successfully",
        "services": list_services()
    }


@router.post("/orders/place")
def create_order(payload: Optional[ServiceOrderRequest] = Body(default=None)):
    if payload is None:
        log_action(
            action="service_order_failed",
            actor_email=None,
            details="Request body is required."
        )
        raise HTTPException(status_code=400, detail="Request body is required.")

    try:
        result = place_service_order(
            customer_name=payload.customer_name,
            customer_email=payload.customer_email,
            client_type=payload.client_type,
            service_id=payload.service_id,
            order_notes=payload.order_notes
        )

        return {
            "message": "Service order placed successfully",
            "order": result
        }

    except ValueError as error:
        log_action(
            action="service_order_validation_failed",
            actor_email=payload.customer_email,
            details=str(error)
        )
        raise HTTPException(status_code=400, detail=str(error))

    except Exception:
        log_action(
            action="service_order_system_error",
            actor_email=payload.customer_email,
            details="Unable to place service order."
        )
        raise HTTPException(
            status_code=500,
            detail="Unable to place service order at this time."
        )


@router.get("/orders/list")
def orders_list():
    return {
        "message": "Service orders retrieved successfully",
        "orders": list_service_orders()
    }