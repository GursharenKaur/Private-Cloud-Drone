from datetime import datetime
from pathlib import Path
import os

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
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
from app.core.security import get_current_device
from app.models.device import Device

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
    db: Session = Depends(get_db),
    current_device: Device = Depends(get_current_device),
):
    os.makedirs("uploads", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{Path(video.filename).name}"
    file_path = f"uploads/{unique_filename}"

    file_data = await video.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    video_record = create_video(
        db=db,
        device=current_device,
        filename=unique_filename,
        filepath=file_path,
        file_size=len(file_data),
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
):
    return get_all_videos(db)


# =====================================================
# Stream Video
# =====================================================

@router.get("/{video_id}/stream")
def stream_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    video = get_video_by_id(db, video_id)

    if video is None:
        raise HTTPException(
            status_code=404,
            detail="Video not found",
        )

    if not os.path.exists(video.filepath):
        raise HTTPException(
            status_code=404,
            detail="Video file not found",
        )

    return FileResponse(
        path=video.filepath,
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
):
    video = delete_video(db, video_id)

    if video is None:
        raise HTTPException(
            status_code=404,
            detail="Video not found",
        )

    return {
        "message": "Video deleted successfully"
    }