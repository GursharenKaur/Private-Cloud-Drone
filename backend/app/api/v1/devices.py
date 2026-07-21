from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.device_auth_rate_limit import (
    is_device_auth_locked,
    record_failed_device_auth,
    reset_device_auth_failures,
)
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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Check whether authentication attempts for this
    # device UUID are temporarily locked.
    if is_device_auth_locked(
        db=db,
        device_uuid=form_data.username,
    ):
        raise HTTPException(
            status_code=429,
            detail=(
                "Too many failed device authentication attempts. "
                "Please try again later."
            ),
        )

    # Existing device authentication logic remains unchanged.
    token = authenticate_device(
        db=db,
        device_uuid=form_data.username, 
        device_secret=form_data.password,
    )

    # Record failed authentication attempt.
    if token is None:
        record_failed_device_auth(
            db=db,
            device_uuid=form_data.username,
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid device credentials",
        )

    # Successful authentication clears previous failures.
    reset_device_auth_failures(
    db=db,
    device_uuid=form_data.username,
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