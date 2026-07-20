from sqlalchemy import Column, DateTime, Integer, String, func

from app.database.database import Base


class DeviceAuthAttempt(Base):
    """
    Tracks consecutive failed authentication attempts
    for an edge device.

    The device is identified using its device UUID.
    """

    __tablename__ = "device_auth_attempts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    device_uuid = Column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )

    failure_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    last_failure_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    locked_until = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )