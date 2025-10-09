# app/main.py
from fastapi import FastAPI
from app.routes import bets, matches
from app.jobs.scheduler import start_scheduler

app = FastAPI(title="Sports Bets API")

app.include_router(bets.router)
app.include_router(matches.router)

start_scheduler()

@app.get("/")
def root():
    return {"message": "API läuft"}

@app.on_event("shutdown")
def shutdown_event():
    from app.jobs.scheduler import scheduler
    scheduler.shutdown()
