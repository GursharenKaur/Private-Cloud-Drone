from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TelemetryCreate(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)