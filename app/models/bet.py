from pydantic import BaseModel
from typing import Optional

class Bet(BaseModel):
    id: int
    user_id: int
    match_id: int
    amount: float
    odds: float
    result: Optional[str] = None