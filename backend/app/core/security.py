from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.models.device import Device
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

device_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/devices/auth"
)


def get_current_user(
    token: str = Depends(user_oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        print("Decoded payload:", payload)

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    if payload.get("type") != "user":
        raise HTTPException(
            status_code=401,
            detail="Invalid user token",
        )

    user_id = int(payload["sub"])

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user

def authenticate_device_token(
    token: str,
    db: Session,
) -> Device:
    """
    Validate a device JWT and return
    the authenticated Device.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid device token",
        )

    if payload.get("type") != "device":
        raise HTTPException(
            status_code=401,
            detail="Invalid device token",
        )

    device_uuid = payload["sub"]

    device = (
        db.query(Device)
        .filter(Device.device_uuid == device_uuid)
        .first()
    )

    if device is None:
        raise HTTPException(
            status_code=401,
            detail="Device not found",
        )

    if not device.is_active:
        raise HTTPException(
            status_code=401,
            detail="Device is inactive",
        )

    return device

# def authenticate_user_token(
#     token: str,
#     db: Session,
# ) -> User:
#     """
#     Validate a user JWT and return
#     the authenticated User.
#     """

#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM],
#         )

#     except JWTError:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid user token",
#         )

#     if payload.get("type") != "user":
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid user token",
#         )

#     user_id = int(payload["sub"])

#     user = (
#         db.query(User)
#         .filter(User.id == user_id)
#         .first()
#     )

#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail="User not found",
#         )

#     return user
def authenticate_user_token(
    token: str,
    db: Session,
) -> User:

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        print("USER PAYLOAD:", payload)

    except JWTError as e:

        print("JWT ERROR:", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid user token",
        )

    if payload.get("type") != "user":

        print("TYPE FOUND:", payload.get("type"))

        raise HTTPException(
            status_code=401,
            detail="Invalid user token",
        )

    user_id = int(payload["sub"])

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user

def get_current_device(
    token: str = Depends(device_oauth2_scheme),
    db: Session = Depends(get_db),
):
    return authenticate_device_token(
        token=token,
        db=db,
    )


def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return current_user
