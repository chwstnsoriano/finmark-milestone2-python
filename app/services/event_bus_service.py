import json

from app.database import create_event, get_events


def publish_event(event_type: str, source_service: str, payload: dict):
    try:
        payload_text = json.dumps(payload)

        return create_event(
            event_type=event_type,
            source_service=source_service,
            payload=payload_text,
            status="recorded"
        )

    except Exception as error:
        print(f"Event bus failed: {error}")
        return None


def list_recent_events(limit: int = 50):
    try:
        return get_events(limit)

    except Exception as error:
        print(f"Unable to retrieve events: {error}")
        return []