from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging import (
    InterceptHandler,
    setup_sentry_logging,
    is_sentry_enabled,
    get_application_logger,
)
from app.db.database import engine, AsyncSessionLocal, get_db, Base
from app.core.config import get_settings
from app.core.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.wrappers import Limit
import logging
import traceback
from logging import Logger
import sentry_sdk
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    Handles startup and shutdown events.
    """

    # Startup tasks
    # Initialize database connection pool, cache, etc.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Initialize FastAPI Limiter
    settings = get_settings()
    logger = get_application_logger()
    redis = None

    try:
        redis = aioredis.from_url(
            settings.redis_url, encoding="utf-8", decode_responses=True
        )
        await FastAPILimiter.init(redis)
        logger.info("FastAPI Limiter initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize FastAPI Limiter: {e}")
        # You can choose to raise the exception or continue without rate limiting
        # raise

    yield  # Application is running

    # Shutdown tasks
    # Close database connections, cleanup, etc.
    await engine.dispose()
    
    # Cleanup resources (if needed)
    if redis is not None:
        await redis.aclose()
        logger.info("Redis connection closed")
    logger.info("Application shutting down")


def create_app() -> FastAPI:
    # Initialize Sentry logging prior to app creation
    # This ensures that any errors during app creation are captured by Sentry
    # and that the logging configuration is set up correctly.
    # This is particularly useful for capturing errors in the app startup phase.
    setup_sentry_logging()

    app = FastAPI(title="My API", version="1.0.0", lifespan=lifespan)
    uvicorn_logger: Logger = logging.getLogger("app")

    # Removing uvicorn default logger
    for name in logging.root.manager.loggerDict:
        if name in ("uvicorn"):
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.handlers.clear()
            uvicorn_logger.setLevel(level=logging.INFO)
            uvicorn_logger.addHandler(hdlr=InterceptHandler())

    # Custom logging middleware
    logger = get_application_logger()

    # Add global exception handlers
    # Global exception handler for unhandled exceptions

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # Add request context to Sentry if enabled
        if is_sentry_enabled():
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("handler", "global_exception_handler")
                scope.set_context(
                    "request",
                    {
                        "url": str(request.url),
                        "method": request.method,
                        "headers": dict(request.headers),
                    },
                )
            # Capture the exception in Sentry before handling it
            sentry_sdk.capture_exception(exc)

        logger.error(
            "\n".join(
                [
                    f"Unhandled exception occurred: {type(exc).__name__}: {str(exc)}",
                    f"Request URL: {request.url}",
                    f"Request method: {request.method}",
                    f"Traceback:\n{traceback.format_exc()}",
                ]
            )
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred. Please try again later.",
                "status_code": 500,
            },
        )

    # Exception handler for HTTP exceptions
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Capture HTTP exceptions with status code 500 or higher in Sentry if enabled
        if exc.status_code >= 500 and is_sentry_enabled():
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("handler", "http_exception_handler")
                scope.set_context(
                    "request",
                    {
                        "url": str(request.url),
                        "method": request.method,
                        "headers": dict(request.headers),
                    },
                )
            sentry_sdk.capture_exception(exc)

        logger.warning(
            "\n".join(
                [
                    f"HTTP exception: {exc.status_code} - {exc.detail}",
                    f"Request URL: {request.url}",
                    f"Request method: {request.method}",
                ]
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Error",
                "message": exc.detail,
                "status_code": exc.status_code,
            },
        )

    # Exception handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.warning(
            "\n".join(
                [
                    f"Validation error: {str(exc)}",
                    f"Request URL: {request.url}",
                    f"Request method: {request.method}",
                ]
            )
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "message": "Invalid request data",
                "details": exc.errors(),
                "status_code": 422,
            },
        )

    # Attach limiter + register custom RateLimitExceeded handler
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        """
        Return a proper 429 response with JSON detail.
        """
        # Get the path that was rate limited
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"

        # The limit string is available in the exception message
        # It typically looks like "5 per 1 minute" or similar
        limit_str = str(exc.detail) if hasattr(exc, "detail") else "Rate limit exceeded"
        limit_object: Limit | None = getattr(exc, "limit", None)

        logger.warning(f"Rate limit exceeded for {client_host} on {path}")

        return JSONResponse(
            status_code=429,
            content={
                "error": "Too Many Requests",
                "message": "Rate limit exceeded. Please try again later.",
                "detail": limit_str,
                "path": path,
                "status_code": 429,
            },
            headers={
                "Retry-After": str(
                    limit_object.limit.multiples
                    * limit_object.limit.GRANULARITY.seconds
                )
                if limit_object
                else "60"  # Suggest retry after 60 seconds
            },
        )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        # Return service health status
        return {"status": "healthy", "service": "fast-food-api"}

    # Example endpoint with rate limit - 2 requests per 30 seconds
    # Using string format: "count/period" where period can be: second, minute, hour, day
    @app.get("/throtteled_hello")
    @limiter.limit("2/30seconds")
    async def throtteled_hello(request: Request):
        return {"message": "Hello world!"}

    # Alternative: 5 requests per minute
    @app.get("/example1")
    @limiter.limit("5/minute")
    async def example1(request: Request):
        return {"message": "Limited to 5 requests per minute"}

    # Alternative: 100 requests per hour
    @app.get("/example2")
    @limiter.limit("100/hour")
    async def example2(request: Request):
        return {"message": "Limited to 100 requests per hour"}

    # Alternative: Multiple limits (most restrictive applies)
    @app.get("/example3")
    @limiter.limit("10/minute;100/hour;1000/day")
    async def example3(request: Request):
        return {"message": "Multiple rate limits applied"}

    @app.get("/test-error")
    async def test_error():
        """Test endpoint to trigger an error for Sentry testing"""
        raise ValueError("This is a test error for Sentry integration")

    @app.get("/sentry-debug")
    async def trigger_error():
        """Test endpoint to trigger a division by zero error"""
        division_by_zero = 1 / 0

    @app.get("/sentry-status")
    async def sentry_status():
        """Check if Sentry logging is enabled"""
        return {
            "sentry_enabled": is_sentry_enabled(),
            "message": "Sentry is enabled"
            if is_sentry_enabled()
            else "Sentry is disabled",
        }

    # Include routers or other components here
    # from .routers import example_router
    # app.include_router(example_router)

    return app
