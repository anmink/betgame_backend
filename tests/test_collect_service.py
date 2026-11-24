from datetime import UTC, datetime, timedelta

import pytest

from app.core.errors import CooldownActiveError
from app.core.game_config import CUPS_PER_COLLECT, CUPS_PER_COLLECT_MATCHDAY
from app.services.collect_service import CollectService
from tests.fakes import FakeMatchRepository, FakeUserRepository

NOW = datetime(2026, 11, 21, 10, 0, tzinfo=UTC)


def make_service(kickoffs=None):
    users = FakeUserRepository({"u1": {"id": "u1", "becher": 0}})
    return CollectService(users, FakeMatchRepository(kickoffs))


def test_collects_normal_amount_without_match():
    result = make_service().collect("u1", NOW)

    assert result.collected == CUPS_PER_COLLECT
    assert result.becher == CUPS_PER_COLLECT


def test_collects_more_on_matchday():
    kickoff = NOW + timedelta(hours=4)
    result = make_service([kickoff]).collect("u1", NOW)

    assert result.collected == CUPS_PER_COLLECT_MATCHDAY


def text_next_collect_is_two_hours_later():
    result = make_service().collect("u1", NOW)

    assert result.next_collect_at == NOW + timedelta(hours=2)


def test_cannot_collect_twice_within_cooldown():
    service = make_service()
    service.collect("u1", NOW)

    with pytest.raises(CooldownActiveError):
        service.collect("u1", NOW + timedelta(minutes=30))


def test_can_collect_again_after_cooldown():
    service = make_service()
    service.collect("u1", NOW)

    result = service.collect("u1", NOW + timedelta(hours=2))

    assert result.becher == 2 * CUPS_PER_COLLECT
