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
    FRONTEND_HOST: str = "http://localhost:8000"
    SQLITE_DB: str = "sqlite:///members.db"

    GETATTR_LOG_LEVEL: LogLevel = LogLevel.CRITICAL
    UPSERT_LOG_LEVEL: LogLevel = LogLevel.WARNING
    LOG_LEVEL: LogLevel = LogLevel.INFO


settings = Settings()
