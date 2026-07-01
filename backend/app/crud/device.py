from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate

def create_device(
    db: Session,
    device: DeviceCreate,
):
    db_device = Device(
        device_name=device.device_name,
        device_type=device.device_type,
        serial_number=device.serial_number,
        status="offline",
    )

    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return db_device


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
