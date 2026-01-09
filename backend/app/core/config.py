from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import (
    DEFAULT_CORS_ORIGINS,
    DEFAULT_DB_URL,
    JWT_ALGORITHM,
    JWT_DEFAULT_EXPIRES_MINUTES,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DB_URL: str = DEFAULT_DB_URL

    JWT_SECRET: str
    JWT_ALGORITHM: str = JWT_ALGORITHM
    JWT_EXPIRES_MINUTES: int = JWT_DEFAULT_EXPIRES_MINUTES

    CORS_ORIGINS: str = DEFAULT_CORS_ORIGINS

    SUPERADMIN_USERNAME: str
    SUPERADMIN_PASSWORD: str

    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]


def get_settings() -> Settings:
    """Get settings instance with validation."""
    settings = Settings()
    
    # Validate required environment variables
    if not settings.JWT_SECRET or settings.JWT_SECRET == "CHANGE_ME_DEV_SECRET":
        raise ValueError(
            "JWT_SECRET environment variable is required and must be set to a secure value. "
            "Please set it in your .env file or environment variables."
        )
    
    if not settings.SUPERADMIN_USERNAME:
        raise ValueError(
            "SUPERADMIN_USERNAME environment variable is required. "
            "Please set it in your .env file or environment variables."
        )
    
    if not settings.SUPERADMIN_PASSWORD:
        raise ValueError(
            "SUPERADMIN_PASSWORD environment variable is required. "
            "Please set it in your .env file or environment variables."
        )
    
    return settings


settings = get_settings()
