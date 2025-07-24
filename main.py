from fastapi import FastAPI
from app import create_app
from app.core.config import settings

is_dev_environment: bool = settings.environment == "development"

# Create app instance at module level for uvicorn import string
app: FastAPI = create_app()


if __name__ == "__main__":
    import uvicorn
    if is_dev_environment:
        # Use import string for reload to work properly
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)
    else:
        # Use app instance for production
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_config=None)