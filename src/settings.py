from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int = 1
    LOG_LEVEL: str = "INFO"


settings = Settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "service": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": settings.LOG_LEVEL,
            "formatter": "service",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {"": {"handlers": ["default"], "level": settings.LOG_LEVEL, "propagate": False}},
}
