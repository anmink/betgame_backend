from datetime import datetime

from pydantic import BaseModel


class CollectResponse(BaseModel):
    collected: int
    becher: int
    next_collect_at: datetime
