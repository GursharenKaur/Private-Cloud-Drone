from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VideoBase(BaseModel):
    filename: str
    filepath: str
    duration: int | None = None
    resolution: str | None = None
    file_size: int | None = None


class VideoCreate(VideoBase):
    pass


class VideoResponse(VideoBase):
    id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
