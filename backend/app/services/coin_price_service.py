from sqlalchemy.orm import Session
from app.models.coin_price import CoinPrice
from datetime import datetime

def get_all_coin_prices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CoinPrice).offset(skip).limit(limit).all()

def get_coin_price_by_symbol(db: Session, symbol: str):
    return db.query(CoinPrice).filter(CoinPrice.symbol == symbol).first()

def create_coin_price(db: Session, symbol: str, price: float):
    db_coin_price = CoinPrice(symbol=symbol, price=price, timestamp=datetime.utcnow())
    db.add(db_coin_price)
    db.commit()
    db.refresh(db_coin_price)
    return db_coin_price
