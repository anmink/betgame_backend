from apscheduler.schedulers.background import BackgroundScheduler
from app.services.match_service import MatchService
import asyncio

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(fetch_matches_job, "interval", minutes=1)
    scheduler.start()

def fetch_matches_job():
    asyncio.run(MatchService.fetch_matches())
    print("Cronjob: Matches erfolgreich aktualisiert")
