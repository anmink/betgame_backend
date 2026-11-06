from pydantic import BaseModel


class Match(BaseModel):
    fixture_id: int
    fixture_date: str
    fixture_status: str
    league_id: int
    league_name: str
    league_round: str
    teamhome_name: str
    teamhome_logo: str
    teamhome_winner: bool | None = None
    teamaway_name: str
    teamaway_logo: str
    teamaway_winner: bool | None = None
    goal_home: int | None = None
    goal_away: int | None = None
    odd_home: float | None = None
    odd_draw: float | None = None
    odd_away: float | None = None
