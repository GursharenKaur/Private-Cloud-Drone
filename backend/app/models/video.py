from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.database.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(
        Integer,
        ForeignKey("devices.id"),
        nullable=False,
    )

    filename = Column(String(255), nullable=False)

    filepath = Column(String(500), nullable=False)

    duration = Column(Integer)

    resolution = Column(String(20))

    file_size = Column(Integer)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

