import logging
from enum import Enum


class LogLevel(Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR


class Settings:
    FASTAPI_HOST: str = "localhost"  # or "127.0.0.1"
    FASTAPI_PORT: int = 8000
    SQLITE_DB: str = "sqlite:///./app/data/members.db"

    LOG_LEVEL: LogLevel = LogLevel.INFO


settings = Settings()
