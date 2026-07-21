from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    get_current_user,
    get_current_device,
    authorize_device,
)
from app.core.telemetry_security import validate_telemetry
from app.core.device_capabilities import DeviceCapability

from app.crud.telemetry import (
    create_telemetry,
    get_all_telemetry,
    get_latest_telemetry,
    get_device_telemetry,
    update_telemetry,
    delete_telemetry,
)

from app.database.database import get_db

from app.models.user import User
from app.models.device import Device

from app.schemas.telemetry import (
    TelemetryCreate,
    TelemetryResponse,
)

router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"],
)


# =====================================================
# Get All Telemetry
# =====================================================

@router.get("/", response_model=list[TelemetryResponse])
def get_telemetry(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_telemetry(db)


# =====================================================
# Latest Device Telemetry
# =====================================================

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


# =====================================================
# Upload Telemetry
# =====================================================

@router.post("/", response_model=TelemetryResponse)
def add_telemetry(
    telemetry: TelemetryCreate,
    db: Session = Depends(get_db),
    current_device: Device = Depends(get_current_device),
):
    """
    Receive telemetry from an authenticated device.

    Authorization:
        - Device must be active.
        - Device must have TELEMETRY capability.
    """

    current_device = authorize_device(
        current_device,
        capability=DeviceCapability.TELEMETRY,
    )

    # Validate telemetry values
    validate_telemetry(telemetry)

    return create_telemetry(
        db,
        telemetry,
        current_device,
    )


# =====================================================
# Device Telemetry History
# =====================================================

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


# =====================================================
# Delete Telemetry
# =====================================================

@router.delete("/{telemetry_id}")
def remove_telemetry(
    telemetry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    telemetry = delete_telemetry(db, telemetry_id)

    if telemetry is None:
        raise HTTPException(
            status_code=404,
            detail="Telemetry not found",
        )

    return {
        "message": "Telemetry deleted successfully"
    }


# =====================================================
# Update Telemetry
# =====================================================

@router.put("/{telemetry_id}", response_model=TelemetryResponse)
def edit_telemetry(
    telemetry_id: int,
    telemetry: TelemetryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = update_telemetry(
        db,
        telemetry_id,
        telemetry,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Telemetry not found",
        )

    return updated