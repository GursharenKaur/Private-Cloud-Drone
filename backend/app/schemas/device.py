from datetime import datetime

from pydantic import BaseModel

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

class DeviceCreate(BaseModel):
    device_name: str
    device_type: str
    firmware_version: str = "1.0.0"
    capabilities: str = "video,telemetry,commands"


class DeviceResponse(BaseModel):
    id: int
    device_uuid: str
    device_name: str
    device_type: str
    firmware_version: str
    status: str
    registered_at: datetime
    last_seen: datetime
    is_active: bool

    class Config:
        from_attributes = True

class DeviceRegistrationResponse(BaseModel):
    device_uuid: str
    device_name: str
    device_type: str
    device_secret: str
    message: str

class DeviceAuthRequest(BaseModel):
    device_uuid: str
    device_secret: str


class DeviceAuthResponse(BaseModel):
    access_token: str
    token_type: str