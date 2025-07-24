from fastapi import FastAPI
from app import create_app
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
is_dev_environment: bool = dotenv.get_key(".env", "ENVIRONMENT") == "development"


if __name__ == "__main__":
    import uvicorn
    app: FastAPI = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=is_dev_environment, log_config=None)