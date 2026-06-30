from sqlalchemy.orm import Session

from app.models.image import Image


def get_image_by_id(db: Session, image_id: int):
    return db.query(Image).filter(Image.id == image_id).first()


def get_all_images(db: Session):
    return db.query(Image).all()


def get_image_by_filename(db: Session, filename: str):
    return db.query(Image).filter(
        Image.filename == filename
    ).first()
