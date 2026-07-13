print("🚀 NEW MAIN.PY LOADED")
from pathlib import Path

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.api.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.devices import router as devices_router
from app.api.v1.telemetry import router as telemetry_router
from app.api.v1.users import router as users_router
from app.core.config import settings
from app.streaming.websocket import router as websocket_router
from app.api.videos import router as videos_router
from app.api.images import router as images_router
from fastapi.responses import FileResponse


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
)

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)
# -------------------------------
# Existing API Routes
# -------------------------------

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(devices_router)
app.include_router(telemetry_router)
app.include_router(websocket_router)
app.include_router(videos_router)
app.include_router(images_router)

@app.get("/")
def root():
    return {
        "message": "Drone Cloud Project Backend Running",
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION,
    }

@app.get("/camera", include_in_schema=False)
def camera_page():
    return FileResponse(FRONTEND_DIR / "camera" / "index.html")

@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return FileResponse(
        FRONTEND_DIR / "dashboard" / "index.html"
    )

@app.get("/recordings", include_in_schema=False)
def recordings_page():
    return FileResponse(
        FRONTEND_DIR / "recordings" / "index.html"
    )