from pydantic_settings import BaseSettings

from backend.src.fileshare.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: str

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1.0"

settings = Config()