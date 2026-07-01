from fastapi import FastAPI
from app.api.v1.users import router as users_router
from app.api.health import router as health_router
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.devices import router as devices_router
from app.api.v1.telemetry import router as telemetry_router
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(devices_router)
app.include_router(telemetry_router)
@app.get("/")
def root():
    return {
        "message": "Drone Cloud Project Backend Running",
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION,
    }
