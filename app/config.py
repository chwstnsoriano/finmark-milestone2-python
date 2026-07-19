import os

from dotenv import load_dotenv


load_dotenv()


def get_boolean_setting(name: str, default: bool) -> bool:
    default_value = "true" if default else "false"
    value = os.getenv(name, default_value)

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "default_secret",
)

PASSWORD_SALT = os.getenv(
    "PASSWORD_SALT",
    "default_salt",
)

TOKEN_ALGORITHM = os.getenv(
    "TOKEN_ALGORITHM",
    "HS256",
)

CACHE_TTL_SECONDS = int(
    os.getenv("CACHE_TTL_SECONDS", "30")
)

# Empty by default so the original local tests continue using SQLite.
# Docker Compose will override this with:
# http://order-service:8001
ORDER_SERVICE_URL = os.getenv(
    "ORDER_SERVICE_URL",
    "",
).rstrip("/")

ORDER_SERVICE_TIMEOUT_SECONDS = float(
    os.getenv(
        "ORDER_SERVICE_TIMEOUT_SECONDS",
        "5",
    )
)

ORDER_SERVICE_FALLBACK_ENABLED = get_boolean_setting(
    "ORDER_SERVICE_FALLBACK_ENABLED",
    True,
)
