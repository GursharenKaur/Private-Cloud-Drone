from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.logging import log_security_event

from app.core.security import (
    get_current_device,
    authorize_device,
)

from app.core.device_capabilities import DeviceCapability

from app.core.upload_security import (
    validate_file_extension,
    validate_mime_type,
    validate_file_size,
    generate_secure_filename,
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_IMAGE_MIME_TYPES,
    MAX_IMAGE_FILE_SIZE,
)

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


# =====================================================
# Upload Image
# =====================================================

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

    # ------------------------------------------
    # Upload Security
    # ------------------------------------------

    validate_file_extension(
        image,
        ALLOWED_IMAGE_EXTENSIONS,
    )

    validate_mime_type(
        image,
        ALLOWED_IMAGE_MIME_TYPES,
    )

    await validate_file_size(
        image,
        MAX_IMAGE_FILE_SIZE,
    )

    # ------------------------------------------
    # Store File
    # ------------------------------------------

    filename = generate_secure_filename(
        image.filename,
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

    # ------------------------------------------
    # Audit Logging
    # ------------------------------------------

    log_security_event(
        f"IMAGE_UPLOAD_SUCCESS | "
        f"image_id={image_record.id} | "
        f"filename={image_record.filename} | "
        f"device_uuid={current_device.device_uuid}"
    )

    return {
        "message": "Image uploaded successfully",
        "image_id": image_record.id,
        "filename": image_record.filename,
    }


# =====================================================
# Get All Images
# =====================================================

@router.get("/")
def get_images(
    db: Session = Depends(get_db),
):
    return get_all_images(db)


# =====================================================
# Get Image By ID
# =====================================================

@router.get("/{image_id}")
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
):
    image = get_image_by_id(
        db,
        image_id,
    )

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    return image