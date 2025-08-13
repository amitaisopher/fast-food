import pytest
from fastapi.testclient import TestClient
from app import create_app


@pytest.fixture
def app():
    """Create a new FastAPI app instance for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Return a TestClient for the FastAPI app."""
    return TestClient(app)
