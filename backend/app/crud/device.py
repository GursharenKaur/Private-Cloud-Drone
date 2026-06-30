from sqlalchemy.orm import Session

from app.models.device import Device


def get_device_by_id(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()


def get_device_by_serial(db: Session, serial_number: str):
    return db.query(Device).filter(
        Device.serial_number == serial_number
    ).first()


def get_all_devices(db: Session):
    return db.query(Device).all()


def get_online_devices(db: Session):
    return db.query(Device).filter(
        Device.status == "online"
    ).all()

