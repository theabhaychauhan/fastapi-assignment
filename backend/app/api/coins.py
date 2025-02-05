import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.coin_price import CoinPrice
from app.db.session import get_db
from app.schemas.coin import CoinPriceResponse
from typing import List

router = APIRouter()

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

@router.post("/binance/data")
async def get_binance_data(db: Session = Depends(get_db)):
    try:
        response = requests.get(BINANCE_API_URL)
        if response.status_code == 200:
            coin_data = response.json()

            for coin in coin_data:
                new_coin = CoinPrice(symbol=coin['symbol'], price=float(coin['price']))
                db.add(new_coin)
            
            db.commit()
            return coin_data
        else:
            return {"error": "Failed to fetch data from Binance"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/coin-prices/{symbol}", response_model=List[CoinPriceResponse])
async def get_coin_prices(symbol: str, db: Session = Depends(get_db)):
    try:
        coin_prices = db.query(CoinPrice).filter(CoinPrice.symbol == symbol).all()
        if not coin_prices:
            return {"error": "No data found for this symbol"}
        return coin_prices
    except Exception as e:
        return {"error": str(e)}

