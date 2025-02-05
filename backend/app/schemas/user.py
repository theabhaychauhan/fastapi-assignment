from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool
    phone: Optional[str]
    bio: Optional[str]

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    bio: str = None
    phone: str = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str]
    bio: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True

class PasswordReset(BaseModel):
    new_password: str
