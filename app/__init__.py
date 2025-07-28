from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging import InterceptHandler, setup_sentry_logging, is_sentry_enabled
import logging
import traceback
from logging import Logger
import sentry_sdk


def create_app() -> FastAPI:

    # Initialize Sentry logging prior to app creation
    # This ensures that any errors during app creation are captured by Sentry
    # and that the logging configuration is set up correctly.
    # This is particularly useful for capturing errors in the app startup phase.
    setup_sentry_logging()

    app = FastAPI(title="My API", version="1.0.0")
    uvicorn_logger: Logger = logging.getLogger("app")

    # Removing uvicorn default logger
    for name in logging.root.manager.loggerDict:
        if name in ("uvicorn"):
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.handlers.clear()
            uvicorn_logger.setLevel(level=logging.INFO)
            uvicorn_logger.addHandler(hdlr=InterceptHandler())

    # Add global exception handlers
    # Global exception handler for unhandled exceptions

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # Add request context to Sentry if enabled
        if is_sentry_enabled():
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("handler", "global_exception_handler")
                scope.set_context("request", {
                    "url": str(request.url),
                    "method": request.method,
                    "headers": dict(request.headers),
                })
            # Capture the exception in Sentry before handling it
            sentry_sdk.capture_exception(exc)

        uvicorn_logger.error(
            f"Unhandled exception occurred: {type(exc).__name__}: {str(exc)}\n"
            f"Request URL: {request.url}\n"
            f"Request method: {request.method}\n"
            f"Traceback:\n{traceback.format_exc()}"
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
                scope.set_context("request", {
                    "url": str(request.url),
                    "method": request.method,
                    "headers": dict(request.headers),
                })
            sentry_sdk.capture_exception(exc)

        uvicorn_logger.warning(
            f"HTTP exception: {exc.status_code} - {exc.detail}\n"
            f"Request URL: {request.url}\n"
            f"Request method: {request.method}"
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
        uvicorn_logger.warning(
            f"Validation error: {str(exc)}\n"
            f"Request URL: {request.url}\n"
            f"Request method: {request.method}"
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

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        # Remove the test error and return proper health check
        return {"status": "healthy", "service": "fast-food-api"}

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
            "message": "Sentry is enabled" if is_sentry_enabled() else "Sentry is disabled"
        }

    # Include routers or other components here
    # from .routers import example_router
    # app.include_router(example_router)

    return app
