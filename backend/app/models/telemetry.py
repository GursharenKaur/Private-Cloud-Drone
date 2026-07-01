from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)

    battery_level = Column(Integer)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

