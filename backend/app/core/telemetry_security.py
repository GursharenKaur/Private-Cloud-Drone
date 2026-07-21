from fastapi import HTTPException

from app.schemas.telemetry import TelemetryCreate


def validate_telemetry(
    telemetry: TelemetryCreate,
) -> None:
    """
    Validate telemetry values before they are
    stored in the database.
    """

    # -----------------------------------------
    # Latitude
    # -----------------------------------------

    if not (-90 <= telemetry.latitude <= 90):
        raise HTTPException(
            status_code=400,
            detail="Invalid latitude value.",
        )

    # -----------------------------------------
    # Longitude
    # -----------------------------------------

    if not (-180 <= telemetry.longitude <= 180):
        raise HTTPException(
            status_code=400,
            detail="Invalid longitude value.",
        )

    # -----------------------------------------
    # Altitude
    # -----------------------------------------

    if not (-500 <= telemetry.altitude <= 10000):
        raise HTTPException(
            status_code=400,
            detail="Invalid altitude value.",
        )

    # -----------------------------------------
    # Battery
    # -----------------------------------------

    if not (0 <= telemetry.battery_level <= 100):
        raise HTTPException(
            status_code=400,
            detail="Invalid battery level.",
        )