from pydantic_settings import BaseSettings

from fileshare.constants import Environment


class Config(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8000/api/v1"
    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS_REGEX: str | None = None

    APP_VERSION: str = "1.0"

settings = Config()