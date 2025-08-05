import logging
from enum import Enum

class LogLevel(Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING= logging.WARNING
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR


class Settings:
    FRONTEND_HOST: str = "http://localhost:8000"
    SQLITE_DB: str = "sqlite:///members.db"

    LOG_LEVEL: LogLevel = LogLevel.INFO


settings = Settings()
