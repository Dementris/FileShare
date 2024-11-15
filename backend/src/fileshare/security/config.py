from pydantic_settings import BaseSettings


class SecurityConfig(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str

settings = SecurityConfig()