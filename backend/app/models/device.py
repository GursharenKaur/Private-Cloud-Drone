from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from app.database.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    device_uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )

    device_name = Column(String(100), nullable=False)

    device_type = Column(String(50), nullable=False)

    firmware_version = Column(
        String(50),
        default="1.0.0",
        nullable=False,
    )

    serial_number = Column(String(100), unique=True, nullable=False)

    status = Column(String(20), default="offline")

    registered_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    secret_hash = Column(
        String(255),
        nullable=False,
    )

    capabilities = Column(
        Text,
        nullable=False,
        default="video,telemetry,commands",
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    last_seen = Column(DateTime(timezone=True), server_default=func.now())
