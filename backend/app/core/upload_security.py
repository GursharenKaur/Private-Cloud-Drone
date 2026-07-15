from pathlib import Path

from fastapi import HTTPException, UploadFile, status


# ==========================================
# Allowed File Types
# ==========================================

ALLOWED_VIDEO_EXTENSIONS = {
    ".webm",
    ".mp4",
    ".mov",
}

ALLOWED_VIDEO_MIME_TYPES = {
    "video/webm",
    "video/mp4",
    "video/quicktime",
}

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


# ==========================================
# File Extension Validation
# ==========================================

def validate_file_extension(
    file: UploadFile,
    allowed_extensions: set[str],
) -> str:
    """
    Validate the uploaded file extension.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
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
    Validate the uploaded file MIME type.
    """

    mime_type = file.content_type

    print("=" * 60)
    print("UPLOAD SECURITY")
    print("Filename :", file.filename)
    print("MIME Type:", mime_type)
    print("Allowed  :", allowed_mime_types)
    print("=" * 60)

    if mime_type not in allowed_mime_types:
        print("❌ INVALID MIME TYPE")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported MIME type: {mime_type}",
        )

    print("✅ VALID MIME TYPE")

    return mime_type