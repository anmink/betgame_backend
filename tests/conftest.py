import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.security import get_current_user


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def logged_in_client():
    app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-id"}
    yield TestClient(app)
    app.dependency_overrides.clear()