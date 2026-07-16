from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.logging import log_security_event
from app.core.security import (
    get_current_user,
    get_current_device,
)
from app.crud.device import (
    create_device,
    get_all_devices,
    get_device_by_id,
    update_device_status,
    delete_device,
    count_devices,
    count_online_devices,
    authenticate_device,
)
from app.database.database import get_db
from app.models.user import User
from app.models.device import Device
from app.schemas.device_status import DeviceStatusUpdate
from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
    DeviceRegistrationResponse,
    DeviceAuthRequest,
    DeviceAuthResponse,
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
    result = create_device(db, device)

    log_security_event(
        f"DEVICE_REGISTERED | "
        f"device_uuid={result['device_uuid']} | "
        f"device_name={result['device_name']} | "
        f"device_type={result['device_type']} | "
        f"registered_by_user={current_user.id}"
    )

    return result


@router.post(
    "/auth",
    response_model=DeviceAuthResponse,
)
def device_authentication(
    credentials: DeviceAuthRequest,
    db: Session = Depends(get_db),
):
    token = authenticate_device(
        db=db,
        device_uuid=credentials.device_uuid,
        device_secret=credentials.device_secret,
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid device credentials",
        )

    return token


@router.get(
    "/me",
    response_model=DeviceResponse,
)
def get_current_authenticated_device(
    current_device: Device = Depends(get_current_device),
):
    return current_device


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
    device = get_device_by_id(
        db,
        device_id,
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    log_security_event(
        f"DEVICE_DELETE | "
        f"device_id={device.id} | "
        f"device_uuid={device.device_uuid} | "
        f"device_name={device.device_name} | "
        f"deleted_by_user={current_user.id}"
    )

    delete_device(
        db,
        device.id,
    )

    return {
        "message": "Device deleted successfully"
    }

@router.patch(
    "/{device_id}/status",
    response_model=DeviceResponse,
)
def update_status(
    device_id: int,
    status_update: DeviceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_device = get_device_by_id(
        db,
        device_id,
    )

    if existing_device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    old_status = existing_device.status

    device = update_device_status(
        db,
        device_id,
        status_update.status,
    )

    log_security_event(
        f"DEVICE_STATUS_UPDATED | "
        f"device_id={device.id} | "
        f"device_uuid={device.device_uuid} | "
        f"old_status={old_status} | "
        f"new_status={device.status} | "
        f"updated_by_user={current_user.id}"
    )

    return device