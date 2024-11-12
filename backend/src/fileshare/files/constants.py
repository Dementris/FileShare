from enum import Enum


class Permissions(str, Enum):
    VIEW = 'V'
    DOWNLOAD = 'D'
