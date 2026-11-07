from pydantic import BaseModel, Field


class Bet(BaseModel):
    match_id: int
    stake: int = Field(gt=0, description="Bet stake must be greater than zero")
    odds: float
    prediction: str
