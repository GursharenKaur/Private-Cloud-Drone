from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate
import secrets
import uuid

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

def create_device(
    db: Session,
    device: DeviceCreate,
):
    device_uuid = str(uuid.uuid4())

    device_secret = secrets.token_urlsafe(32)

    secret_hash = hash_password(device_secret)

    db_device = Device(
        device_uuid=device_uuid,
        device_name=device.device_name,
        device_type=device.device_type,
        firmware_version=device.firmware_version,
        status="offline",
        secret_hash=secret_hash,
        capabilities=device.capabilities,
    )

    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return {
        "device_uuid": device_uuid,
        "device_name": db_device.device_name,
        "device_type": db_device.device_type,
        "device_secret": device_secret,
        "message": "Device registered successfully. Save the device secret securely. It will not be shown again.",
    }

def authenticate_device(
    db: Session,
    device_uuid: str,
    device_secret: str,
):
    device = (
        db.query(Device)
        .filter(Device.device_uuid == device_uuid)
        .first()
    )

    if device is None:
        return None

    if not device.is_active:
        return None

    if not verify_password(
        device_secret,
        device.secret_hash,
    ):
        return None

    access_token = create_access_token(
    data={
        "sub": device.device_uuid,
        "type": "device",
    }
)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

def get_all_devices(db: Session):
    return db.query(Device).all()

def update_device_status(
    db: Session,
    device_id: int,
    status: str,
):
    device = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if device is None:
        return None

    device.status = status

    db.commit()
    db.refresh(device)

    return device
def delete_device(
    db: Session,
    device_id: int,
):
    device = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if device is None:
        return False

    db.delete(device)
    db.commit()

    return True
def get_device_by_id(
    db: Session,
    device_id: int,
):
    return (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )
def count_devices(db: Session):
    return db.query(Device).count()


def count_online_devices(db: Session):
    return (
        db.query(Device)
        .filter(Device.status == "online")
        .count()
    )
