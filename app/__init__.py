from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="My API", version="1.0.0")

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "fast-food-api"}

    # Include routers or other components here
    # from .routers import example_router
    # app.include_router(example_router)

    return app