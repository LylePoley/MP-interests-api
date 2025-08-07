import logging
from enum import Enum
import os

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
    CURRENT_WORKING_DIR: str = os.getcwd()
    SQLITE_DB_PATH: str = os.path.join(CURRENT_WORKING_DIR, "app", "data", "members.db")
    SQLITE_DB: str = "sqlite:///" + SQLITE_DB_PATH

    LOG_LEVEL: LogLevel = LogLevel.INFO


settings = Settings()
