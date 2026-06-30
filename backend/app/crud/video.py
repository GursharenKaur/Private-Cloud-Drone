from sqlalchemy.orm import Session

from app.models.video import Video


def get_video_by_id(db: Session, video_id: int):
    return db.query(Video).filter(Video.id == video_id).first()


def get_all_videos(db: Session):
    return db.query(Video).all()


def get_video_by_filename(db: Session, filename: str):
    return db.query(Video).filter(
        Video.filename == filename
    ).first()

