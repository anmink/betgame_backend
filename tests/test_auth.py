from app.services.user_service import UserService


def test_me_without_token_is_rejected(client):
    response = client.get("/auth/me")

    assert response.status_code in (401, 403)


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={"email": "neu@example.com", "password": "123"},
    )

    assert response.status_code == 422


def test_me_returns_current_user(logged_in_client, monkeypatch):
    async def fake_get_user(user_id):
        return {"id": user_id, "username": "test@example.com", "coins": 100}

    monkeypatch.setattr(UserService, "get_user", fake_get_user)

    response = logged_in_client.get("auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "test-user-id",
        "username": "test@example.com",
        "coins": 100,
    }
