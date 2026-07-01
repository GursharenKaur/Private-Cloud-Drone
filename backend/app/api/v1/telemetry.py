from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.crud.telemetry import (
    create_telemetry,
    get_all_telemetry,
    get_telemetry_by_device,
    get_latest_telemetry,
)
from app.database.database import get_db
from app.models.user import User
from app.schemas.telemetry import TelemetryCreate, TelemetryResponse
from app.crud.telemetry import get_device_telemetry
router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"],
)


@router.get("/", response_model=list[TelemetryResponse])
def get_telemetry(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_telemetry(db)
@router.get("/device/{device_id}", response_model=list[TelemetryResponse])
def get_telemetry_by_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_device_telemetry(db, device_id)
@router.get(
    "/device/{device_id}/latest",
    response_model=TelemetryResponse,
)
def latest_telemetry(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    telemetry = get_latest_telemetry(db, device_id)

    if telemetry is None:
        raise HTTPException(
            status_code=404,
            detail="No telemetry found for this device",
        )

    return telemetry
@router.post("/", response_model=TelemetryResponse)
def add_telemetry(
    telemetry: TelemetryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_telemetry(db, telemetry)

@router.get(
    "/device/{device_id}",
    response_model=list[TelemetryResponse],
)
def get_telemetry_by_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    telemetry = get_device_telemetry(db, device_id)

    if not telemetry:
        raise HTTPException(
            status_code=404,
            detail="No telemetry found for this device",
        )

    return telemetry
