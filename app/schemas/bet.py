from typing import Literal

from pydantic import BaseModel, Field


class BetCreate(BaseModel):
    match_id: int
    stake: int = Field(gt=0)
    prediction: Literal["home", "draw", "away"]
