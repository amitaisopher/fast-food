# FastAPI Boilerplate Project

A comprehensive boilerplate for FastAPI applications with modern Python tooling, containerization, and a well-organized project structure.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **UV Package Manager**: Ultra-fast Python package installer and resolver
- **Docker Support**: Multi-stage builds for both development and production
- **Docker Compose**: Easy orchestration for development and production environments
- **Structured Architecture**: Clean, scalable folder organization
- **Health Checks**: Built-in health monitoring endpoints
- **Environment Configuration**: Flexible environment-based configuration

## 📁 Project Structure

```
fast-food/
├── app/                          # Main application package
│   ├── __init__.py              # App factory and main FastAPI instance
│   ├── api/                     # API layer
│   │   ├── __init__.py
│   │   ├── deps/                # API dependencies (auth, database, etc.)
│   │   └── v1/                  # API version 1 routes
│   │       └── __init__.py
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration
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
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Production Docker image
├── Dockerfile.simple           # Development Docker image
├── main.py                      # Application entry point
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Locked dependencies
└── README.md                   # This file
```

### Folder Structure Explanation

#### `app/` - Main Application Package
- **`__init__.py`**: Contains the FastAPI app factory function that creates and configures the application instance
- **`api/`**: API layer with route definitions, dependencies, and versioning
- **`core/`**: Core application functionality including configuration and security
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

4. **Create environment file** (optional):
   ```bash
   cp .env.example .env  # If you have an example file
   # or create .env manually with:
   echo "ENVIRONMENT=development" > .env
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

Create a `.env` file in the root directory with the following variables:

```env
ENVIRONMENT=development  # or production
# Add other configuration variables as needed
```

### Development vs Production

- **Development**: Uses `Dockerfile.simple` with hot reload and volume mounting
- **Production**: Uses multi-stage `Dockerfile` with optimized image size and security

## 🏥 Health Check

The application includes a health check endpoint at `/health` that returns:

```json
{
  "status": "healthy",
  "service": "fast-food-api"
}
```

## 📝 API Documentation

Once the application is running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

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