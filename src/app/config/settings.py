"""Application settings configuration"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    APP_NAME: str = "llmplan"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    CORS_ALLOW_ORIGINS: list[str] = ["*"]

    # LMStudio Configuration
    LMSTUDIO_BASE_URL: str = "http://localhost:1234/v1"
    LMSTUDIO_API_KEY: str = "lm-studio"
    LMSTUDIO_TIMEOUT: int = 30
    LMSTUDIO_MAX_RETRIES: int = 3

    # Summary Configuration
    DEFAULT_MODEL_NAME: str = "qwen/qwen3-4b"
    DEFAULT_MAX_TOKENS: int = 1000
    DEFAULT_TEMPERATURE: float = 0.3
    DEFAULT_SUMMARY_TYPE: str = "concise"
    DEFAULT_LANGUAGE: str = "korean"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
