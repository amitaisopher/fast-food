from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging import InterceptHandler
import logging
import traceback
from logging import Logger

def create_app() -> FastAPI:
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
        raise ValueError("This is a test error for health check")
        return {"status": "healthy", "service": "fast-food-api"}

    # Include routers or other components here
    # from .routers import example_router
    # app.include_router(example_router)

    return app