from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_provider: str = "stub_anthropic"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    anthropic_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
