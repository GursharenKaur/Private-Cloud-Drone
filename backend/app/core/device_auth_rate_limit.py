from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import log_security_event
from app.crud.device_auth_attempt import (
    get_or_create_device_auth_attempt,
    update_device_auth_attempt,
)


# ==========================================================
# Configuration
# ==========================================================

MAX_DEVICE_AUTH_FAILURES = settings.DEVICE_AUTH_MAX_FAILURES

DEVICE_AUTH_LOCKOUT_DURATION = timedelta(
    minutes=settings.DEVICE_AUTH_LOCKOUT_MINUTES
)


# ==========================================================
# Lock Status
# ==========================================================

def is_device_auth_locked(
    db: Session,
    device_uuid: str,
) -> bool:
    """
    Returns True if authentication attempts for the device
    are currently locked.

    Automatically clears expired lockouts.
    """

    auth_attempt = get_or_create_device_auth_attempt(
        db=db,
        device_uuid=device_uuid,
    )

    if auth_attempt.locked_until is None:
        return False

    current_time = datetime.now(timezone.utc)

    if current_time >= auth_attempt.locked_until:
        auth_attempt.failure_count = 0
        auth_attempt.locked_until = None

        update_device_auth_attempt(
            db=db,
            auth_attempt=auth_attempt,
        )

        log_security_event(
            f"DEVICE_AUTH_UNLOCKED | "
            f"device_uuid={device_uuid} | "
            f"reason=lockout_expired"
        )

        return False

    return True


# ==========================================================
# Failed Authentication
# ==========================================================

def record_failed_device_auth(
    db: Session,
    device_uuid: str,
) -> None:
    """
    Record a failed device authentication attempt.

    Temporarily lock authentication attempts for the device
    when the configured failure threshold is reached.
    """

    auth_attempt = get_or_create_device_auth_attempt(
        db=db,
        device_uuid=device_uuid,
    )

    auth_attempt.failure_count += 1
    auth_attempt.last_failure_at = datetime.now(timezone.utc)

    if auth_attempt.failure_count == MAX_DEVICE_AUTH_FAILURES:
        auth_attempt.locked_until = (
            datetime.now(timezone.utc)
            + DEVICE_AUTH_LOCKOUT_DURATION
        )

        log_security_event(
            f"DEVICE_AUTH_LOCKED | "
            f"device_uuid={device_uuid} | "
            f"failure_count={auth_attempt.failure_count} | "
            f"locked_until={auth_attempt.locked_until}"
        )

    update_device_auth_attempt(
        db=db,
        auth_attempt=auth_attempt,
    )


# ==========================================================
# Successful Authentication
# ==========================================================

def reset_device_auth_failures(
    db: Session,
    device_uuid: str,
) -> None:
    """
    Clear device authentication failure tracking
    after successful authentication.
    """

    auth_attempt = get_or_create_device_auth_attempt(
        db=db,
        device_uuid=device_uuid,
    )

    auth_attempt.failure_count = 0
    auth_attempt.locked_until = None

    update_device_auth_attempt(
        db=db,
        auth_attempt=auth_attempt,
    )