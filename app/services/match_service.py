import httpx
import os
import json
from typing import List
from app.models.match import Match
from app.db.supabase_client import supabase

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
LEAGUE = "78"
SEASON = "2025"
BOOKMAKERS = "1"
BETS = "1"

class MatchService:
    @staticmethod
    async def fetch_matches():
        headers = {"X-RapidAPI-Key": API_KEY}
        url_fixtures = f"{BASE_URL}/fixtures?league={LEAGUE}&season={SEASON}"
        url_odds = f"{BASE_URL}/odds?league={LEAGUE}&season={SEASON}&bookmaker={BOOKMAKERS}&bet={BETS}"

        async with httpx.AsyncClient() as client:
            #response_fixtures = await client.get(url_fixtures, headers=headers)
            response_odds = await client.get(url_odds, headers=headers)
            
            """ if response_fixtures.status_code and response_odds.status_code != 200:
                raise ValueError(f"Fehler beim Abrufen der Matches: {response_fixtures.text} {response_odds.text}") """
            
            #fixtures = response_fixtures.json()
            odds = response_odds.json()


            """ with open("fixtures.json", "w") as f:
                json.dump(fixtures, f) """

            with open("odds.json", "w") as f:
                json.dump(odds, f)

            return odds

    async def save_matches():
        print("hi")
        with open("fixtures.json", "r") as f:
            fixtures = json.load(f)

        with open("odds.json", "r") as f:
            odds = json.load(f)

        combined = []
        odd_dict = {item["fixture"]["id"]: item for item in odds["response"]}

        for fixture in fixtures["response"]:
            fixture_id = fixture["fixture"]["id"]
            if fixture_id in odd_dict:
                merged = {**odd_dict[fixture_id], **fixture}
            else:
                merged = fixture
            combined.append(merged)

        with open("combined.json", "w") as f:
            json.dump(combined, f)
        
        matches = []
        for item in combined:
            #values = item.get("bookmakers", [{}])[0].get("bets", [{}])[0].get("values", [])
            match = Match(
                fixture_id=item.get("fixture", {}).get("id"),
                fixture_date=item.get("fixture", {}).get("date"),
                fixture_status=item.get("fixture", {}).get("status", {}).get("long"),
                league_id=item.get("league", {}).get("id"),
                league_name=item.get("league", {}).get("name"),
                league_round=item.get("league", {}).get("round", "Unknown").split("-")[-1].strip(),
                teamhome_name=item.get("teams", {}).get("home", {}).get("name"),
                teamhome_logo=item.get("teams", {}).get("home", {}).get("logo"),
                teamhome_winner=item.get("teams", {}).get("home", {}).get("winner"),
                teamaway_name=item.get("teams", {}).get("away", {}).get("name"),
                teamaway_logo=item.get("teams", {}).get("away", {}).get("logo"),
                teamaway_winner=item.get("teams", {}).get("away", {}).get("winner"),
                goal_home=item.get("goals", {}).get("home"),
                goal_away=item.get("goals", {}).get("away"),
                #odd_home = float(values[0]["odd"]) if len(values) > 0 else None,
                #odd_draw = float(values[1]["odd"]) if len(values) > 0 else None,
                #odd_away = float(values[2]["odd"]) if len(values) > 0 else None,
            )
            matches.append(match)

        with open("matches.json", "w") as f:
            json.dump([m.dict() for m in matches], f, indent=2)     