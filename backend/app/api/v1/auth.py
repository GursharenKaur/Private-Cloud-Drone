from app.core.login_rate_limit import (
    is_user_locked,
    record_failed_login,
    reset_login_failures,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.logging import log_security_event
from app.core.security import create_access_token, verify_password
from app.database.database import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if user is None:

        log_security_event(
            f"USER_LOGIN_FAILED | "
            f"email={form_data.username} | "
            f"reason=user_not_found"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )
    if is_user_locked(
        db=db,
        username=user.email,
    ):

        log_security_event(
            f"USER_ACCOUNT_LOCKED | "
            f"user_id={user.id} | "
            f"email={user.email}"
        )

        raise HTTPException(
            status_code=429,
            detail=(
                "Too many failed login attempts. "
                "Please try again later."
            ),
        )

    if not verify_password(
        form_data.password,
        user.password_hash,
    ):
        record_failed_login(
            db=db,
            username=user.email,
        )

        log_security_event(
            f"USER_LOGIN_FAILED | "
            f"user_id={user.id} | "
            f"email={user.email} | "
            f"reason=invalid_password"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    payload = {
        "sub": str(user.id),
        "type": "user",
        "email": user.email,
        "role": user.role,
    }

    print("LOGIN PAYLOAD:", payload)

    access_token = create_access_token(payload)
    reset_login_failures(
        db=db,
        username=user.email,
    )

    log_security_event(
        f"USER_LOGIN_SUCCESS | "
        f"user_id={user.id} | "
        f"email={user.email}"
    )

    return TokenResponse(
        access_token=access_token,
    )