from pydantic_settings import BaseSettings


class SecurityConfig(BaseSettings):
    SECRET_KEY: str = "mXtdoTcJhT-rMHasUlvxcIa277JU2EMYSG5aXGt54IY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    ALGORITHM: str = 'HS256'

settings = SecurityConfig()