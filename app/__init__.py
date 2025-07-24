from fastapi import FastAPI
from app.core.logging import InterceptHandler
import logging

def create_app() -> FastAPI:
    app = FastAPI(title="My API", version="1.0.0")

    # Removing uvicorn default logger
    for name in logging.root.manager.loggerDict:
        if name in ("uvicorn"):
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.handlers.clear()
            uvicorn_logger.setLevel(level=logging.INFO)
            uvicorn_logger.addHandler(hdlr=InterceptHandler())

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "fast-food-api"}

    # Include routers or other components here
    # from .routers import example_router
    # app.include_router(example_router)

    return app