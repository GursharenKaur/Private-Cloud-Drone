from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.crud.video import create_video

import os

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{video.filename}"

    file_data = await video.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_data)

    video_record = create_video(
        db=db,
        filename=video.filename,
        filepath=file_path,
        file_size=len(file_data),
    )

    return {
        "message": "Video uploaded successfully",
        "video_id": video_record.id,
        "filename": video_record.filename,
    }