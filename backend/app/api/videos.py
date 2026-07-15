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

    # ------------------------------------------
    # Store File
    # ------------------------------------------

    os.makedirs("uploads", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{Path(video.filename).name}"
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

    return {
        "message": "Video uploaded successfully",
        "video_id": video_record.id,
        "filename": video_record.filename,
    }