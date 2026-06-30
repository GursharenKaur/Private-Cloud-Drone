from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
)

app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "Drone Cloud Project Backend Running",
        "project": settings.PROJECT_NAME,
        "version": settings.API_VERSION,
    }
