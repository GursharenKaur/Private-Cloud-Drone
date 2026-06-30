from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)

    latitude = Column(Float)

    longitude = Column(Float)

    altitude = Column(Float)

    speed = Column(Float)

    heading = Column(Float)

    battery = Column(Integer)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

