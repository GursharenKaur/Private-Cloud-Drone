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
