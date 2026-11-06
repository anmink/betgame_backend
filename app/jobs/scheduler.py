import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.bet_service import BetService
from app.services.match_service import MatchService

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(fetch_matches_job, "interval", minutes=15)
    scheduler.add_job(check_bets_job, "interval", minutes=5)
    scheduler.add_job(check_current_round, trigger="cron", day_of_week="tue", hour=10, minute=0)
    """ scheduler.add_job(check_current_round, "interval", seconds=5) """
    scheduler.start()


def fetch_matches_job():
    asyncio.run(MatchService.fetch_matches())
    print("Cronjob: Matches erfolgreich aktualisiert", flush=True)


def check_bets_job():
    asyncio.run(BetService.check_bets())
    print("Cronjob: Check bets erfolgreich ausgeführt", flush=True)


def check_current_round():
    asyncio.run(MatchService.get_current_round())
    print("Cronjob: current round erfolgreich ausgeführt", flush=True)


def test():
    asyncio.run(MatchService.get_matches_by_rounds())
    print("Cronjob matches by rounds")
