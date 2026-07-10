import os
from sqlalchemy.orm import Session
from app.models.device import Device
from app.models.video import Video


def get_video_by_id(db: Session, video_id: int):
    return db.query(Video).filter(Video.id == video_id).first()


def get_all_videos(db: Session):
    return db.query(Video).all()


def get_video_by_filename(db: Session, filename: str):
    return db.query(Video).filter(
        Video.filename == filename
    ).first()


def create_video(
    db: Session,
    device: Device,
    filename: str,
    filepath: str,
    file_size: int,
    duration: int = None,
    resolution: str = None,
):

    video = Video(
        device_id=device.id,
        filename=filename,
        filepath=filepath,
        file_size=file_size,
        duration=duration,
        resolution=resolution,
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return video

    


def delete_video(db: Session, video_id: int):

    video = get_video_by_id(db, video_id)

    if video is None:
        return None

    if os.path.exists(video.filepath):
        os.remove(video.filepath)

    db.delete(video)

    db.commit()

    return video