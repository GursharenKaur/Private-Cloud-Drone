import os

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Form,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.video import VideoResponse

from app.crud.video import (
    create_video,
    get_all_videos,
    get_video_by_id,
    delete_video,
)

from app.core.logging import log_security_event

from app.core.security import (
    get_current_user,
    authorize_device,
)

from app.core.video_authorization import (
    authorize_video,
    resolve_video_path,
)

from app.core.upload_security import (
    validate_file_extension,
    validate_mime_type,
    validate_file_size,
    generate_secure_filename,
    ALLOWED_VIDEO_EXTENSIONS,
    ALLOWED_VIDEO_MIME_TYPES,
    MAX_VIDEO_FILE_SIZE,
)

from app.models.user import User
from app.models.device import Device
from app.core.device_capabilities import DeviceCapability


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


# =====================================================
# Upload Video
# =====================================================

@router.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    device_uuid: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device = (
        db.query(Device)
        .filter(Device.device_uuid == device_uuid)
        .first()
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    device = authorize_device(
        device,
        capability=DeviceCapability.VIDEO_UPLOAD,
    )

    # ------------------------------------------
    # Upload Security
    # ------------------------------------------

    validate_file_extension(
        video,
        ALLOWED_VIDEO_EXTENSIONS,
    )

    validate_mime_type(
        video,
        ALLOWED_VIDEO_MIME_TYPES,
    )

    await validate_file_size(
        video,
        MAX_VIDEO_FILE_SIZE,
    )

    # ------------------------------------------
    # Store File
    # ------------------------------------------

    os.makedirs("uploads", exist_ok=True)

    unique_filename = generate_secure_filename(
        video.filename
    )

    file_path = f"uploads/{unique_filename}"

    file_data = await video.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    video_record = create_video(
        db=db,
        device=device,
        filename=unique_filename,
        filepath=file_path,
        file_size=len(file_data),
    )

    # ------------------------------------------
    # Audit Logging
    # ------------------------------------------

    log_security_event(
        f"VIDEO_UPLOAD_SUCCESS | "
        f"video_id={video_record.id} | "
        f"filename={video_record.filename} | "
        f"device_uuid={device.device_uuid} | "
        f"user_id={current_user.id}"
    )

    return {
        "message": "Video uploaded successfully",
        "video_id": video_record.id,
        "filename": video_record.filename,
    }


# =====================================================
# Get All Videos
# =====================================================

@router.get("/", response_model=list[VideoResponse])
def get_videos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_videos(db)


# =====================================================
# Stream Video
# =====================================================

@router.get("/{video_id}/stream")
def stream_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    video = get_video_by_id(
        db,
        video_id,
    )

    video = authorize_video(video)

    file_path = resolve_video_path(video)

    return FileResponse(
        path=str(file_path),
        media_type="video/webm",
        filename=video.filename,
    )


# =====================================================
# Delete Video
# =====================================================

@router.delete("/{video_id}")
def delete_video_endpoint(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    video = get_video_by_id(
        db,
        video_id,
    )

    video = authorize_video(video)

    log_security_event(
        f"VIDEO_DELETE | "
        f"video_id={video.id} | "
        f"filename={video.filename} | "
        f"device_uuid={video.device.device_uuid} | "
        f"deleted_by_user={current_user.id}"
    )

    delete_video(
        db,
        video.id,
    )

    return {
        "message": "Video deleted successfully",
    }