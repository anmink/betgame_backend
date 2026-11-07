from app.core.dependencies import get_user_service
from app.main import app
from app.services.user_service import UserService
from tests.fakes import FakeUserRepository


def test_me_without_token_is_rejected(client):
    response = client.get("/auth/me")

    assert response.status_code in (401, 403)


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={"email": "neu@example.com", "password": "123"},
    )

    assert response.status_code == 422


def test_me_returns_current_user(logged_in_client):
    fake = FakeUserRepository(
        {"test-user-id": {"id": "test-user-id", "username": "test@example.com", "coins": 100}}
    )
    app.dependency_overrides[get_user_service] = lambda: UserService(fake)

    response = logged_in_client.get("/auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "test-user-id",
        "username": "test@example.com",
        "coins": 100,
    }
