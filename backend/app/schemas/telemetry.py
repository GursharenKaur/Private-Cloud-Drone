from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TelemetryBase(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    speed: float
    heading: float
    battery: int


class TelemetryCreate(TelemetryBase):
    pass


class TelemetryResponse(TelemetryBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
from datetime import datetime

from pydantic import BaseModel


class TelemetryCreate(BaseModel):
    device_id: int
    latitude: float
    longitude: float
    altitude: float
    battery_level: int


class TelemetryResponse(BaseModel):
    id: int
    device_id: int
    latitude: float
    longitude: float
    altitude: float
    battery_level: int
    timestamp: datetime

    class Config:
        from_attributes = True
