from pydantic import BaseModel
from datetime import datetime
from typing import List

class CoinPriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime

    class Config:
        orm_mode = True