from fastapi import FastAPI
from app.api import auth
from app.api import coins
from app.api import weather
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(coins.router, tags=["Coins"])
app.include_router(weather.router, tags=["Weather"])
