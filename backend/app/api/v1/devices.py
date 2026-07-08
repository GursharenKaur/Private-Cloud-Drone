from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.device import update_device_status
from app.schemas.device_status import DeviceStatusUpdate
from app.core.security import get_current_user
from app.crud.device import (
    create_device,
    get_all_devices,
    get_device_by_id,
    update_device_status,
    delete_device,
    count_devices,
    count_online_devices,
)
from app.database.database import get_db
from app.models.user import User
from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
    DeviceRegistrationResponse,
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.get("/", response_model=list[DeviceResponse])
def get_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_devices(db)


@router.post(
    "/register",
    response_model=DeviceRegistrationResponse,
)
def add_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_device(db, device)
@router.get("/stats")
def device_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {
        "total_devices": count_devices(db),
        "online_devices": count_online_devices(db),
    }
@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device = get_device_by_id(db, device_id)

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device
@router.delete("/{device_id}")
def remove_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_device(db, device_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return {
        "message": "Device deleted successfully"
    }
@router.patch("/{device_id}/status", response_model=DeviceResponse)
def update_status(
    device_id: int,
    status_update: DeviceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device = update_device_status(
        db,
        device_id,
        status_update.status,
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device
