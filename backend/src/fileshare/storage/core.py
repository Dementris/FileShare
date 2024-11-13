import logging
import os
import pathlib
from abc import ABC, abstractmethod
from os import write
from pathlib import Path

from fileshare.storage.config import storage_settings
from fileshare.storage.utils import encrypt_content, decrypt_content, name_generator


class FileStorage:
    def __init__(self):
        self.path = Path(storage_settings.DATA_PATH).absolute()

    def get_file(self, file_path) -> bytes | None:
        file = self.path.joinpath(file_path)
        if file.is_file():
            file_data = decrypt_content(file.read_bytes(), key=storage_settings.SECRET_KEY)
            return file_data
        else:
            return None

    def save_file(self, content):
        file_path = self.path.joinpath(name_generator())
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(encrypt_content(content, key=storage_settings.SECRET_KEY))
        return file_path.relative_to(self.path)

    def delete_file(self, file_path):
        file_path = self.path.joinpath(file_path)
        try:
            file_path.unlink()
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logging.exception(e)
            return False