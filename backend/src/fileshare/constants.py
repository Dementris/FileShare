from enum import Enum


class Environment(str, Enum):
    PRODUCTION = 'PRODUCTION'
    DEVELOPMENT = 'DEVELOPMENT'
    TESTING = 'TESTING'