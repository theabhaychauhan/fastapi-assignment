from sqlalchemy import Column, String, Boolean, Integer
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    signup_source = Column(String, default='platform')

