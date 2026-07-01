from datetime import datetime

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    device_name: str
    device_type: str
    serial_number: str

class DeviceResponse(BaseModel):
    id: int
    device_name: str
    device_type: str
    serial_number: str
    status: str
    last_seen: datetime

    class Config:
        from_attributes = True
