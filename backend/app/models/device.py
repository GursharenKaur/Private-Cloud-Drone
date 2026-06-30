from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    device_name = Column(String(100), nullable=False)

    device_type = Column(String(50), nullable=False)

    serial_number = Column(String(100), unique=True, nullable=False)

    status = Column(String(20), default="offline")

    last_seen = Column(DateTime(timezone=True), server_default=func.now())
