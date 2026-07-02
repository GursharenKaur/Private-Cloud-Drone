from sqlalchemy.orm import Session

from app.models.telemetry import Telemetry


def get_telemetry_by_id(db: Session, telemetry_id: int):
    return db.query(Telemetry).filter(
        Telemetry.id == telemetry_id
    ).first()


def get_all_telemetry(db: Session):
    return db.query(Telemetry).all()
def get_telemetry_by_device(
    db: Session,
    device_id: int,
):
    return (
        db.query(Telemetry)
        .filter(Telemetry.device_id == device_id)
        .all()
    )
def get_latest_telemetry(
    db: Session,
    device_id: int,
):
    return (
        db.query(Telemetry)
        .filter(Telemetry.device_id == device_id)
        .order_by(Telemetry.timestamp.desc())
        .first()
    )
from sqlalchemy.orm import Session

from app.models.telemetry import Telemetry
from app.schemas.telemetry import TelemetryCreate


def create_telemetry(
    db: Session,
    telemetry: TelemetryCreate,
):
    db_telemetry = Telemetry(
        device_id=telemetry.device_id,
        latitude=telemetry.latitude,
        longitude=telemetry.longitude,
        altitude=telemetry.altitude,
        battery_level=telemetry.battery_level,
    )

    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)

    return db_telemetry


def get_all_telemetry(db: Session):
    return db.query(Telemetry).all()

def get_device_telemetry(db: Session, device_id: int):
    return (
        db.query(Telemetry)
        .filter(Telemetry.device_id == device_id)
        .order_by(Telemetry.timestamp.desc())
        .all()
    )
def delete_telemetry(db: Session, telemetry_id: int):
    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.id == telemetry_id)
        .first()
    )

    if telemetry is None:
        return None

    db.delete(telemetry)
    db.commit()

    return telemetry

def delete_telemetry(db: Session, telemetry_id: int):
    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.id == telemetry_id)
        .first()
    )

    if telemetry is None:
        return None

    db.delete(telemetry)
    db.commit()

    return telemetry

def update_telemetry(db: Session, telemetry_id: int, telemetry_data):
    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.id == telemetry_id)
        .first()
    )

    if telemetry is None:
        return None

    for key, value in telemetry_data.model_dump(exclude_unset=True).items():
        setattr(telemetry, key, value)

    db.commit()
    db.refresh(telemetry)

    return telemetry
