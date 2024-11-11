from typing import Annotated

from fastapi.params import Depends

from fileshare.files.repositories import FilesRepository, FilesStorage


class FilesService:
    def __init__(self, repository: Annotated[FilesRepository, Depends()], storage: Annotated[FilesStorage, Depends()]):
        self.repository = repository
        self.storage = storage


