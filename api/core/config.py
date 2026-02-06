"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    environment: str = "development"
    max_file_size_mb: int = 20
    analysis_timeout_sec: int = 300
    ws_heartbeat_sec: int = 30
    host: str = "0.0.0.0"
    port: int = 8080

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
