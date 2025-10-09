# app/main.py
from fastapi import FastAPI
from app.routes import bets, matches
from app.services.match_service import MatchService

app = FastAPI(title="Sports Bets API")

# Routes registrieren
app.include_router(bets.router)
app.include_router(matches.router)


@app.get("/")
def root():
    return {"message": "API läuft"}
