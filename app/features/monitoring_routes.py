from fastapi import APIRouter, HTTPException

from app.database import get_audit_logs
from app.services.event_bus_service import list_recent_events

router = APIRouter()


@router.get("/audit-logs")
def audit_logs():
    try:
        return {
            "message": "Audit logs retrieved successfully",
            "logs": get_audit_logs()
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Audit log storage is temporarily unavailable."
        )


@router.get("/events")
def events():
    try:
        return {
            "message": "Event bus records retrieved successfully",
            "events": list_recent_events()
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Event bus is temporarily unavailable."
        )