from datetime import datetime

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    device_name: str
    device_type: str
    firmware_version: str = "1.0.0"


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
    device_secret: str
    message: str