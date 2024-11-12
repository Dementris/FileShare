import os
from abc import ABC, abstractmethod
from pathlib import Path


class AbstractStorage(ABC):
    path = None

    @abstractmethod
    def get_file(self, file):
        pass

    @abstractmethod
    def save_file(self, file, container):
        pass

    @abstractmethod
    def delete_file(self, file):
        pass

class FileStorage(AbstractStorage):
    path = Path(__file__).parent.absolute()

    def get_file(self, file):
        pass

    def save_file(self, file, container):
        pass

    def delete_file(self, file_path):
        pass