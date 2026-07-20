from datetime import datetime

from sqlalchemy.orm import Session

from app.models.login_attempt import LoginAttempt


def get_login_attempt(db: Session, username: str) -> LoginAttempt | None:
    """
    Retrieve the login attempt record for a username.
    """
    return (
        db.query(LoginAttempt)
        .filter(LoginAttempt.username == username)
        .first()
    )


def create_login_attempt(db: Session, username: str) -> LoginAttempt:
    """
    Create a new login attempt record for a username.
    """
    login_attempt = LoginAttempt(
        username=username,
        failure_count=0,
    )

    db.add(login_attempt)
    db.commit()
    db.refresh(login_attempt)

    return login_attempt


def get_or_create_login_attempt(db: Session, username: str) -> LoginAttempt:
    """
    Retrieve an existing login attempt record or create one.
    """
    login_attempt = get_login_attempt(db, username)

    if login_attempt is None:
        login_attempt = create_login_attempt(db, username)

    return login_attempt


def update_login_attempt(db: Session, login_attempt: LoginAttempt) -> LoginAttempt:
    """
    Persist changes made to a login attempt record.
    """
    login_attempt.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(login_attempt)

    return login_attempt


def delete_login_attempt(db: Session, username: str) -> None:
    """
    Remove a login attempt record.
    """
    login_attempt = get_login_attempt(db, username)

    if login_attempt is None:
        return

    db.delete(login_attempt)
    db.commit()