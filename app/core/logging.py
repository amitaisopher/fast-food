import sys
import logging
from loguru import logger
from app.core.config import settings
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration


def setup_sentry_logging() -> None:
    """
    Setup logging configuration for the application.
    """
    sentry_logger = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events to Sentry
    )

    # Configure Sentry for error tracking
    if settings.sentry_enabled and settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            integrations=[FastApiIntegration(), sentry_logger],
            traces_sample_rate=1.0,  # Adjust this value for performance monitoring
            # Add data like request headers and IP for users,
            # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
            send_default_pii=True,
        )
        logger.info("Sentry logging initialized")
    else:
        logger.info("Sentry logging disabled")


def is_sentry_enabled() -> bool:
    """
    Check if Sentry logging is enabled.
    """
    return settings.sentry_enabled and bool(settings.sentry_dsn)


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
