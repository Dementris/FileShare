from pydantic_settings import BaseSettings


class StorageConfig(BaseSettings):
    SECRET_KEY: str = "DAt24N49xTzEIw2qfHdSi8Z4X75ezWhINdm807irjiE="
    DATA_PATH: str = "./data"

storage_settings = StorageConfig()