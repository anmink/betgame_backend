# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import bets, matches, auth, user
from app.jobs.scheduler import start_scheduler

app = FastAPI(title="Sports Bets API")

app.include_router(bets.router)
app.include_router(matches.router)
app.include_router(auth.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

start_scheduler()


@app.get("/")
def root():
    return {"message": "API läuft"}


""" @app.on_event("shutdown")
def shutdown_event():
    from app.jobs.scheduler import scheduler
    scheduler.shutdown() """
