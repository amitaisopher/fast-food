# FastAPI Boilerplate Project

A comprehensive boilerplate for FastAPI applications with modern Python tooling, containerization, and a well-organized project structure.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **UV Package Manager**: Ultra-fast Python package installer and resolver
- **Docker Support**: Multi-stage builds for both development and production
- **Docker Compose**: Easy orchestration for development and production environments
- **Structured Architecture**: Clean, scalable folder organization
- **Singleton Pattern**: Configuration and logging using singleton pattern for optimal resource usage
- **Environment-Specific Config**: Separate `.env` files per environment (`.env.development`, `.env.production`, `.env.staging`)
- **Enhanced Performance**: uvloop integration for improved asyncio performance
- **Advanced Logging**: Loguru-based logging with Sentry integration and custom application logger
- **Error Tracking**: Optional Sentry integration for production error monitoring
- **Health Checks**: Built-in health monitoring and debug endpoints
- **Global Exception Handlers**: Standardized error responses across the application

## 📁 Project Structure

```
fast-food/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── create_app.py            # FastAPI app factory with exception handlers
│   ├── api/                     # API layer
│   │   ├── __init__.py
│   │   ├── deps/                # API dependencies (auth, database, etc.)
│   │   └── v1/                  # API version 1 routes
│   │       └── __init__.py
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration (Singleton pattern)
│   │   ├── logging.py          # Logging setup with Loguru and Sentry
│   │   └── security.py         # Security utilities (auth, hashing, etc.)
│   ├── crud/                    # CRUD operations
│   ├── db/                      # Database layer
│   │   ├── __init__.py
│   │   ├── base.py             # Base database model
│   │   ├── init_db.py          # Database initialization
│   │   └── session.py          # Database session management
│   ├── models/                  # Database models (SQLAlchemy, etc.)
│   ├── schemas/                 # Pydantic schemas for request/response
│   ├── services/                # Business logic layer
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── tests/                       # Test suite
│   ├── __init__.py
│   └── conftest.py             # Test configuration and fixtures
├── .env.example                 # Example environment configuration
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Production Docker image
├── Dockerfile.simple           # Development Docker image
├── main.py                      # Application entry point with uvloop
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Locked dependencies
└── README.md                   # This file
```

### Folder Structure Explanation

#### `app/` - Main Application Package
- **`__init__.py`**: Package initialization file
- **`create_app.py`**: FastAPI application factory function that creates and configures the app instance with global exception handlers
- **`api/`**: API layer with route definitions, dependencies, and versioning
- **`core/`**: Core application functionality
  - **`config.py`**: Application settings with singleton pattern and environment-specific `.env` file loading
  - **`logging.py`**: Logging configuration using Loguru with singleton pattern, Sentry integration, and custom application logger
  - **`security.py`**: Security utilities including authentication and hashing
- **`crud/`**: Create, Read, Update, Delete operations for data models
- **`db/`**: Database-related modules including models, sessions, and initialization
- **`models/`**: Database models (typically SQLAlchemy models)
- **`schemas/`**: Pydantic schemas for request/response validation and serialization
- **`services/`**: Business logic layer that orchestrates between CRUD and API layers
- **`utils/`**: Utility functions and helpers used across the application

#### `tests/` - Test Suite
Contains all test files and test configuration for the application.

## 🏃‍♂️ How to Run the Application

### Prerequisites

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose (for containerized deployment)

### Method 1: Local Development with UV

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup the project**:
   ```bash
   git clone <your-repo-url>
   cd fast-food
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Create environment file**:
   ```bash
   cp .env.example .env.development
   # Edit .env.development with your configuration
   ```

   The application uses environment-specific configuration files:
   - `.env.development` - Development environment
   - `.env.production` - Production environment  
   - `.env.staging` - Staging environment
   
   Set the `ENVIRONMENT` variable to load the appropriate file:
   ```bash
   export ENVIRONMENT=development  # Loads .env.development
   ```

5. **Run the application**:
   ```bash
   uv run python main.py
   ```

The application will be available at `http://localhost:8000`

### Method 2: Docker Development

1. **Run with Docker Compose (development)**:
   ```bash
   docker-compose --profile dev up --build
   ```

This will start the development server with hot reload on `http://localhost:8001`

### Method 3: Docker Production

1. **Run with Docker Compose (production)**:
   ```bash
   docker-compose up --build
   ```

This will start the production server on `http://localhost:8000`

### Method 4: Direct Docker Build

1. **Build and run production image**:
   ```bash
   docker build -t fast-food .
   docker run -p 8000:8000 fast-food
   ```

2. **Build and run simple development image**:
   ```bash
   docker build -f Dockerfile.simple -t fast-food-dev .
   docker run -p 8000:8000 -v $(pwd):/app fast-food-dev
   ```

## 🔧 Configuration

### Environment Variables

The application uses environment-specific configuration files with a singleton pattern for optimal performance:

#### Configuration Files
- **`.env.development`** - Development environment settings
- **`.env.production`** - Production environment settings
- **`.env.staging`** - Staging environment settings

Set the `ENVIRONMENT` variable to specify which configuration file to load:
```bash
export ENVIRONMENT=development  # Loads .env.development
export ENVIRONMENT=production   # Loads .env.production
export ENVIRONMENT=staging      # Loads .env.staging
```

#### Example Configuration (`.env.development`)

```env
# Environment Configuration
ENVIRONMENT=development

# Application Configuration
APP_NAME=FastAPI Boilerplate
APP_VERSION=1.0.0
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging Configuration
SENTRY_ENABLED=false              # Set to true to enable Sentry error tracking
SENTRY_DSN="https://<your-sentry-dsn>"  # Your Sentry DSN (required if SENTRY_ENABLED=true)
LOG_LEVEL=info

# Database Configuration (if needed)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security Configuration (if needed)
# SECRET_KEY=your-secret-key-here
# ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Key Features

#### 1. Singleton Pattern Configuration
The settings are loaded once and reused throughout the application lifecycle using the `get_settings()` function, ensuring optimal performance and consistency.

#### 2. Singleton Pattern Logging
Application logger is initialized once using `get_application_logger()` and reused throughout the application.

#### 3. Enhanced Performance with uvloop
The application replaces the default asyncio event loop with uvloop for significantly improved performance in production environments.

#### 4. Optional Sentry Integration
- Set `SENTRY_ENABLED=true` to enable error tracking to Sentry.io
- Requires `SENTRY_DSN` to be configured
- Automatically captures unhandled exceptions and HTTP 5xx errors
- Includes request context (URL, method, headers) in error reports
- Check Sentry status at `/sentry-status` endpoint

#### 5. Advanced Logging
- **Loguru** for structured, colored logging
- Custom log format for development and JSON serialization for production
- Intercepts uvicorn logs and redirects them through Loguru
- Singleton pattern application logger accessible via `get_application_logger()`

### Development vs Production

- **Development**: 
  - Uses human-readable log format
  - Hot reload enabled
  - Debug endpoints available
  - uvloop enabled for better performance
  
- **Production**: 
  - JSON serialized logs for log aggregation
  - No reload
  - Sentry error tracking recommended
  - uvloop enabled for maximum performance

## 🏥 Health Check & Debug Endpoints

The application includes several built-in endpoints:

### Health Check
**GET** `/health` - Returns service health status
```json
{
  "status": "healthy",
  "service": "fast-food-api"
}
```

### Sentry Status
**GET** `/sentry-status` - Check if Sentry integration is enabled
```json
{
  "sentry_enabled": true,
  "message": "Sentry is enabled"
}
```

### Debug Endpoints (for testing error handling)
- **GET** `/test-error` - Triggers a ValueError to test exception handling
- **GET** `/sentry-debug` - Triggers a division by zero error

## 📝 API Documentation

Once the application is running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

## 🏗️ Architecture & Design Patterns

### Singleton Pattern

The application implements the singleton pattern for critical components to ensure single initialization and optimal resource usage:

#### Settings Singleton
```python
from app.core.config import get_settings

settings = get_settings()  # Always returns the same instance
```

Benefits:
- Single source of truth for configuration
- Environment-specific `.env` files (`.env.development`, `.env.production`, etc.)
- Loads configuration once at startup
- Consistent settings across the application

#### Logger Singleton
```python
from app.core.logging import get_application_logger

logger = get_application_logger()  # Always returns the same Loguru instance
```

Benefits:
- Centralized logging configuration
- Structured logging with Loguru
- Automatic integration with Sentry
- Intercepts and redirects uvicorn logs

### Application Factory Pattern

The `create_app()` function in `app/create_app.py` creates and configures the FastAPI application:

```python
from app.create_app import create_app

app = create_app()
```

This pattern:
- Separates app creation from app execution
- Registers global exception handlers
- Configures middleware and logging
- Makes testing easier with different configurations

### Global Exception Handlers

The application includes comprehensive exception handling:

1. **Global Exception Handler**: Catches all unhandled exceptions
   - Returns standardized 500 error response
   - Logs full traceback
   - Sends to Sentry (if enabled)

2. **HTTP Exception Handler**: Catches HTTP exceptions
   - Returns appropriate status codes
   - Sends 5xx errors to Sentry (if enabled)
   
3. **Validation Exception Handler**: Catches request validation errors
   - Returns 422 status code with detailed validation errors

### Performance Optimization: uvloop

The application uses **uvloop** as a drop-in replacement for the default asyncio event loop:

```python
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```

Benefits:
- 2-4x faster than the default event loop
- Lower latency for I/O operations
- Better performance under high load
- Production-grade asyncio performance

## 📊 Logging System

The application features an advanced logging system built on **Loguru** with optional **Sentry** integration:

### Features

1. **Structured Logging with Loguru**
   - Colored output for better readability in development
   - JSON serialization in production for log aggregation
   - Automatic exception tracking with full traceback
   - Easy-to-use API

2. **Singleton Pattern Logger**
   ```python
   from app.core.logging import get_application_logger
   
   logger = get_application_logger()
   logger.info("Application started")
   logger.error("An error occurred", extra={"user_id": 123})
   ```

3. **Uvicorn Log Interception**
   - All uvicorn logs are intercepted and redirected through Loguru
   - Consistent log format across the entire application
   - Better control over log levels and formatting

4. **Optional Sentry Integration**
   - Error tracking to Sentry.io for production monitoring
   - Automatically captures exceptions with request context
   - Configurable via environment variables
   - Check status at `/sentry-status` endpoint

### Configuration

Enable Sentry in your environment file:
```env
SENTRY_ENABLED=true
SENTRY_DSN=https://your-key@o1234567.ingest.sentry.io/1234567
```

Disable Sentry for local development:
```env
SENTRY_ENABLED=false
```

## 🧪 Running Tests

```bash
# Install test dependencies (if not already installed)
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app
```

## 🚀 Deployment

This boilerplate is ready for deployment to various platforms:

- **Docker-based platforms**: Use the production `Dockerfile`
- **Cloud platforms**: Configure environment variables and use the provided Docker setup
- **Kubernetes**: The Docker images can be easily deployed to Kubernetes clusters

## 📦 Adding New Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Update dependencies
uv sync
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.