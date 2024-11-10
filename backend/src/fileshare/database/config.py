from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str = 'sqlite+aiosqlite:///test.db'

settings = DatabaseSettings()