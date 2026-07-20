from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root = DroneCloudProject/
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )

    PROJECT_NAME: str = "DroneCloudProject"
    API_VERSION: str = "v1"

    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    LOGIN_MAX_FAILURES: int = 5
    LOGIN_LOCKOUT_MINUTES: int = 15
    DEVICE_AUTH_MAX_FAILURES: int = 5
    DEVICE_AUTH_LOCKOUT_MINUTES: int = 15
    # Storage
    UPLOAD_DIR: str = "/app/uploads"
    VIDEO_DIR: str = "/app/videos"
    RECORDING_DIR: str = "/app/recordings"
    LOG_DIR: str = "/app/logs"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
