import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.logging import log_security_event


# ==========================================
# Allowed File Types
# ==========================================

ALLOWED_VIDEO_EXTENSIONS = {
    ".webm",
    ".mp4",
    ".mov",
}

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


# ==========================================
# Allowed MIME Types
# ==========================================

ALLOWED_VIDEO_MIME_TYPES = {
    "video/webm",
    "video/mp4",
    "video/quicktime",
}

ALLOWED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
}


# ==========================================
# Maximum File Sizes
# ==========================================

MAX_VIDEO_FILE_SIZE = 500 * 1024 * 1024
MAX_IMAGE_FILE_SIZE = 10 * 1024 * 1024


# ==========================================
# File Extension Validation
# ==========================================

def validate_file_extension(
    file: UploadFile,
    allowed_extensions: set[str],
) -> str:
    """
    Validate uploaded file extension.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:

        log_security_event(
            f"UPLOAD_REJECTED | "
            f"reason=invalid_extension | "
            f"filename={file.filename} | "
            f"extension={extension}"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension: {extension}",
        )

    return extension


# ==========================================
# MIME Type Validation
# ==========================================

def validate_mime_type(
    file: UploadFile,
    allowed_mime_types: set[str],
) -> str:
    """
    Validate uploaded MIME type.
    """

    mime_type = file.content_type

    if mime_type not in allowed_mime_types:

        log_security_event(
            f"UPLOAD_REJECTED | "
            f"reason=invalid_mime_type | "
            f"filename={file.filename} | "
            f"mime_type={mime_type}"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported MIME type: {mime_type}",
        )

    return mime_type


# ==========================================
# File Size Validation
# ==========================================

async def validate_file_size(
    file: UploadFile,
    max_size: int,
) -> int:
    """
    Validate uploaded file size.
    """

    file_data = await file.read()

    file_size = len(file_data)

    if file_size > max_size:

        log_security_event(
            f"UPLOAD_REJECTED | "
            f"reason=file_too_large | "
            f"filename={file.filename} | "
            f"file_size={file_size} | "
            f"max_allowed={max_size}"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"File size exceeds the maximum allowed limit "
                f"of {max_size} bytes."
            ),
        )

    await file.seek(0)

    return file_size


# ==========================================
# Secure Filename Generation
# ==========================================

def generate_secure_filename(
    original_filename: str,
) -> str:
    """
    Generate a secure unique filename while
    preserving the original extension.
    """

    extension = Path(original_filename).suffix.lower()

    return f"{uuid.uuid4()}{extension}"