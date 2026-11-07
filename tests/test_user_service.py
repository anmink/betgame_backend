import pytest
from fastapi import HTTPException

from app.services.user_service import UserService
from tests.fakes import FakeUserRepository


def test_get_user_returns_existing_user():
    repository = FakeUserRepository({"u1": {"id": "u1", "username": "usery", "coins": 50}})
    service = UserService(repository)

    user = service.get_user("u1")

    assert user["username"] == "usery"


def test_get_user_raises_404_when_missing():
    service = UserService(FakeUserRepository())

    with pytest.raises(HTTPException) as error:
        service.get_user("gibt-es-nicht")

    assert error.value.status_code == 404
