from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.security import (
    get_current_device,
    authorize_device,
)
from app.core.device_capabilities import DeviceCapability

from app.crud.image import (
    create_image,
    get_all_images,
    get_image_by_id,
)
from app.database.database import get_db
from app.models.device import Device

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)

UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/upload")
async def upload_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_device: Device = Depends(get_current_device),
):
    """
    Upload an image from an authenticated device.

    Authorization:
        - Device must be active.
        - Device must have VIDEO_UPLOAD capability.
    """

    current_device = authorize_device(
        current_device,
        capability=DeviceCapability.VIDEO_UPLOAD,
    )

    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed",
        )

    filename = (
        f"{current_device.device_uuid}_"
        f"{image.filename}"
    )

    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as buffer:
        buffer.write(await image.read())

    image_record = create_image(
        db=db,
        device=current_device,
        filename=filename,
        filepath=str(filepath),
        file_size=filepath.stat().st_size,
    )

    return {
        "message": "Image uploaded successfully",
        "image_id": image_record.id,
        "filename": image_record.filename,
    }