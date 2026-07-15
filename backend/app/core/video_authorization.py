from pathlib import Path

from fastapi import HTTPException, status

from app.models.video import Video


UPLOAD_DIRECTORY = Path("uploads")


def require_video_exists(video: Video) -> Video:
    """
    Ensure the requested video exists.
    """

    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        )

    return video


def authorize_video(video: Video) -> Video:
    """
    Centralized authorization for video resources.

    This function will be extended in future phases
    to support ownership checks, user roles,
    temporary URLs, etc.
    """

    return require_video_exists(video)


def resolve_video_path(video: Video) -> Path:
    """
    Resolve and validate the physical path
    of a stored video.
    """

    file_path = Path(video.filepath).resolve()
    upload_root = UPLOAD_DIRECTORY.resolve()

    if upload_root not in file_path.parents:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid video path",
        )

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video file not found",
        )

    return file_path