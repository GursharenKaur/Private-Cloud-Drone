from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    device_name: str
    device_type: str
    serial_number: str


class DeviceCreate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    id: int
    status: str
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True)

