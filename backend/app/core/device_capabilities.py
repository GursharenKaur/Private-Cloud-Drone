from enum import StrEnum


class DeviceCapability(StrEnum):
    VIDEO_STREAM = "video_stream"
    VIDEO_UPLOAD = "video_upload"
    TELEMETRY = "telemetry"
    COMMANDS = "commands"