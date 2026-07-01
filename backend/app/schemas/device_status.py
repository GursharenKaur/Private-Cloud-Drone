from pydantic import BaseModel


class DeviceStatusUpdate(BaseModel):
    status: str

