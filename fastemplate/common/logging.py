from __future__ import annotations

import logging
import sys

import loguru


# Intercept logs from python standard logging module
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Convert python logging record into a Loguru log
        try:
            level: str | int = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        loguru.logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


_LOG_BASE = (
    "<green>{time:YYYY-MM-DDTHH:mm:ss.SSS}</green> | <level>{level:<8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)


def _log_formatter(record: loguru.Record) -> str:
    if record["exception"]:
        return _LOG_BASE + "\n{exception}"
    return _LOG_BASE + "\n"


def setup_logging(log_level: str = "INFO") -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    handler: loguru.BasicHandlerConfig = {
        "sink": sys.stdout,
        "level": log_level,
        "format": _log_formatter,
        "backtrace": False,  # reduce framework noise in logs
    }
    loguru.logger.configure(handlers=[handler])
