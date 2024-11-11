from abc import ABC, abstractmethod


class AbstractStorage(ABC):

    @abstractmethod
    def download(self, file):
        pass

    @abstractmethod
    def upload(self, file):
        pass

    @abstractmethod
    def delete(self, file):
        pass

    @abstractmethod
    def list_files(self):
        pass