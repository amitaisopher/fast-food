from fastapi import FastAPI
from app.create_app import create_app
from app.core.config import get_settings, Environment

settings = get_settings()
is_dev_environment: bool = settings.environment == Environment.DEVELOPMENT

# Create app instance at module level for uvicorn import string
app: FastAPI = create_app()


if __name__ == "__main__":
    import uvicorn
    import asyncio
    import uvloop
    
    # Replace asyncio default event loop with uvloop for increased performance.
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    if is_dev_environment:
        # Use import string for reload to work properly
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)
    else:
        # Use app instance for production
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_config=None)