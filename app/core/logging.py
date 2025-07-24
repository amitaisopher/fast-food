import sys
import logging
from loguru import logger
from app.core.config import settings


ENV = settings.environment
logger.remove()  # Remove default logger

if ENV == "development":
    logger.add(sys.stdout)
elif ENV == "production":
    logger.add(sys.stdout, serialize=True)

class InterceptHandler(logging.Handler):
    """
    Custom logging handler to intercept log messages and redirect them to Loguru.
    """
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level: str = logger.level(record.levelname).name
        except ValueError:
            level: int = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )