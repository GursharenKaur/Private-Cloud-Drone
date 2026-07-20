from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.crud.login_attempt import (
    get_or_create_login_attempt,
    update_login_attempt,
)
from app.core.config import settings
from app.core.logging import log_security_event

# ==========================================================
# Configuration
# ==========================================================

MAX_LOGIN_FAILURES = settings.LOGIN_MAX_FAILURES

LOCKOUT_DURATION = timedelta(
    minutes=settings.LOGIN_LOCKOUT_MINUTES
)


# ==========================================================
# Lock Status
# ==========================================================

def is_user_locked(db: Session, username: str) -> bool:
    """
    Returns True if the user is currently locked.
    Automatically clears expired lockouts.
    """

    login_attempt = get_or_create_login_attempt(db, username)

    if login_attempt.locked_until is None:
        return False

    current_time = datetime.now(timezone.utc)

    if current_time >= login_attempt.locked_until:
        login_attempt.failure_count = 0
        login_attempt.locked_until = None

        update_login_attempt(db, login_attempt)

        return False

    return True


# ==========================================================
# Failed Login
# ==========================================================

def record_failed_login(db: Session, username: str) -> None:
    """
    Record a failed login attempt.
    Lock the account if the threshold is reached.
    """

    login_attempt = get_or_create_login_attempt(db, username)

    login_attempt.failure_count += 1
    login_attempt.last_failure_at = datetime.now(timezone.utc)

    if login_attempt.failure_count == MAX_LOGIN_FAILURES:
        login_attempt.locked_until = (
            datetime.now(timezone.utc) + LOCKOUT_DURATION
        )

        log_security_event(
            f"USER_ACCOUNT_LOCKED | "
            f"username={username} | "
            f"failure_count={login_attempt.failure_count} | "
            f"locked_until={login_attempt.locked_until}"
        )

    update_login_attempt(db, login_attempt)


# ==========================================================
# Successful Login
# ==========================================================

def reset_login_failures(db: Session, username: str) -> None:
    """
    Clear all failure tracking after a successful login.
    """

    login_attempt = get_or_create_login_attempt(db, username)

    login_attempt.failure_count = 0
    login_attempt.locked_until = None

    update_login_attempt(db, login_attempt)