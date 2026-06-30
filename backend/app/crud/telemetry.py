from sqlalchemy.orm import Session

from app.models.telemetry import Telemetry


def get_telemetry_by_id(db: Session, telemetry_id: int):
    return db.query(Telemetry).filter(
        Telemetry.id == telemetry_id
    ).first()


def get_all_telemetry(db: Session):
    return db.query(Telemetry).all()


def get_latest_telemetry(db: Session):
    return (
        db.query(Telemetry)
        .order_by(Telemetry.timestamp.desc())
        .first()
    )
