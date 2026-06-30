from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DroneCloudProject"
    API_VERSION: str = "v1"

    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int

    # Security
    SECRET_KEY: str = "ChangeThisToAVeryLongRandomSecretKey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Storage
    UPLOAD_DIR: str = "/app/uploads"
    VIDEO_DIR: str = "/app/videos"
    RECORDING_DIR: str = "/app/recordings"
    LOG_DIR: str = "/app/logs"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
