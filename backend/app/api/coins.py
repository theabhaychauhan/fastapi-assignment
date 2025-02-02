import requests
from fastapi import APIRouter

router = APIRouter()

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

@router.get("/binance/data")
async def get_binance_data():
    try:
        response = requests.get(BINANCE_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data from Binance"}
    except Exception as e:
        return {"error": str(e)}
