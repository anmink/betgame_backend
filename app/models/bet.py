from pydantic import BaseModel, Field

class Bet(BaseModel):
    match_id: str
    amount: float = Field(gt=0, description="Bet amount must be greater than zero")
    odds: float
    prediction: str