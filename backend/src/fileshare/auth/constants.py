from enum import Enum


class Roles(str, Enum):
    ADMIN = 'A'
    USER = 'U'