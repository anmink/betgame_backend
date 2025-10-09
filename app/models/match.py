from pydantic import BaseModel
from typing import Optional

class Match(BaseModel):
    fixture_id: int
    fixture_date: str
    fixture_status: str
    league_id: int
    league_name: str
    league_round: str
    teamhome_name: str
    teamhome_logo: str
    teamhome_winner: Optional[bool] = None
    teamaway_name: str
    teamaway_logo: str
    teamaway_winner: Optional[bool] = None
    goal_home: Optional[int] = None
    goal_away: Optional[int] = None
    odd_home: Optional[float] = None
    odd_draw: Optional[float] = None
    odd_away: Optional[float] = None
