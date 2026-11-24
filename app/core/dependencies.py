from app.repositories.match_repository import MatchRepository
from app.repositories.user_repository import UserRepository
from app.services.collect_service import CollectService
from app.services.user_service import UserService


def get_user_service() -> UserService:
    return UserService(UserRepository())


def get_collect_service() -> CollectService:
    return CollectService(UserRepository(), MatchRepository())
