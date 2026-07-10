from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func

from app.database.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    filepath = Column(String(500), nullable=False)

    file_size = Column(Integer)

    captured_at = Column(DateTime(timezone=True), server_default=func.now())
