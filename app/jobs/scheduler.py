from apscheduler.schedulers.background import BackgroundScheduler
from app.services.match_service import MatchService
from app.services.bet_service import BetService
import asyncio

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(fetch_matches_job, "interval", minutes=15)
    scheduler.add_job(check_bets_job, "interval", seconds=5)
    scheduler.start()

def fetch_matches_job():
    asyncio.run(MatchService.fetch_matches())
    print("Cronjob: Matches erfolgreich aktualisiert")

def check_bets_job():
    asyncio.run(BetService.check_bet())
    print("Cronjob: Check bets erfolgreich ausgeführt")
