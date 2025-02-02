import requests
from fastapi import APIRouter

router = APIRouter()

WEATHER_API_URL = "https://api.data.gov.sg/v1/environment/air-temperature"

@router.get("/weather/data")
async def get_weather_data():
    try:
        response = requests.get(WEATHER_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch weather data"}
    except Exception as e:
        return {"error": str(e)}
