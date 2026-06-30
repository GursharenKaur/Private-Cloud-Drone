from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImageBase(BaseModel):
    filename: str
    filepath: str
    file_size: int | None = None


class ImageCreate(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: int
    captured_at: datetime

    model_config = ConfigDict(from_attributes=True)

