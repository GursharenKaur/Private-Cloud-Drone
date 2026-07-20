from sqlalchemy.orm import Session

from app.models.device_auth_attempt import DeviceAuthAttempt


def get_device_auth_attempt(
    db: Session,
    device_uuid: str,
) -> DeviceAuthAttempt | None:
    """
    Retrieve authentication attempt tracking
    for a device UUID.
    """

    return (
        db.query(DeviceAuthAttempt)
        .filter(
            DeviceAuthAttempt.device_uuid == device_uuid
        )
        .first()
    )


def get_or_create_device_auth_attempt(
    db: Session,
    device_uuid: str,
) -> DeviceAuthAttempt:
    """
    Retrieve the authentication attempt record
    for a device, or create one if it does not exist.
    """

    auth_attempt = get_device_auth_attempt(
        db=db,
        device_uuid=device_uuid,
    )

    if auth_attempt is not None:
        return auth_attempt

    auth_attempt = DeviceAuthAttempt(
        device_uuid=device_uuid,
        failure_count=0,
    )

    db.add(auth_attempt)
    db.commit()
    db.refresh(auth_attempt)

    return auth_attempt


def update_device_auth_attempt(
    db: Session,
    auth_attempt: DeviceAuthAttempt,
) -> DeviceAuthAttempt:
    """
    Persist changes to a device authentication
    attempt record.
    """

    db.add(auth_attempt)
    db.commit()
    db.refresh(auth_attempt)

    return auth_attempt