import time
from collections import defaultdict

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 120

rate_limit_store = defaultdict(list)


def is_rate_limited(client_id: str):
    current_time = time.time()
    request_times = rate_limit_store[client_id]

    recent_requests = [
        request_time
        for request_time in request_times
        if current_time - request_time < RATE_LIMIT_WINDOW_SECONDS
    ]

    rate_limit_store[client_id] = recent_requests

    if len(recent_requests) >= RATE_LIMIT_MAX_REQUESTS:
        return True

    rate_limit_store[client_id].append(current_time)
    return False


def get_rate_limit_status():
    return {
        "enabled": True,
        "max_requests": RATE_LIMIT_MAX_REQUESTS,
        "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
        "message": "Simple in-memory rate limiting is active for API routes."
    }