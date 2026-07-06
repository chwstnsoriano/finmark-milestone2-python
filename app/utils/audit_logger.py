from app.database import create_audit_log


def log_action(action: str, actor_email=None, details=None):
    try:
        return create_audit_log(action, actor_email, details)

    except Exception as error:
        print(f"Audit logging failed: {error}")
        return None