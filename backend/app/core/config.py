from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_provider: str = "stub_openai"
    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
