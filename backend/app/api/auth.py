from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services.auth_service import register_user, authenticate_user, create_auth_token, get_current_user, create_jwt_token, get_password_hash
from app.db.session import get_db
import httpx
from fastapi.responses import RedirectResponse
from app.models.user import User
from app.core.config import settings
import os
from app.schemas.user import PasswordReset

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_data.email, user_data.password, user_data.full_name)
    return user

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    token = create_auth_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
def get_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return user

@router.get("/login/google")
async def login_with_google():
    config = await get_google_oauth2_config()
    authorization_url = config["authorization_endpoint"]
    redirect_uri = "http://localhost:8000/auth/callback"
    scope = "openid profile email"
    
    url = f"{authorization_url}?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}"
    
    return RedirectResponse(url)

@router.get("/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    config = await get_google_oauth2_config()
    
    token_url = config["token_endpoint"]
    redirect_uri = "http://localhost:8000/auth/callback"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        })
        token_data = response.json()
        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail="Google login failed")

    user_info = await get_google_user_info(token_data["access_token"])

    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        user = User(
            email=user_info["email"],
            full_name=user_info.get("name"),
            is_active=True
        )
        db.add(user)
        db.commit()

    token = create_jwt_token(user)
    redirect_url = f"http://localhost:5173/profile?token={token}"
    return RedirectResponse(url=redirect_url)


async def get_google_oauth2_config():
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.GOOGLE_DISCOVERY_URL)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=500, detail="Could not fetch Google OAuth2 config")

async def get_google_user_info(access_token: str):
    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        return response.json()

@router.put("/profile/update", response_model=UserResponse)
async def update_user_profile(
    updated_user: UserUpdate,
    photo: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.id == current_user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if updated_user.password:
        updated_user.password = get_password_hash(updated_user.password)

    if photo:
        photo_path = f"uploads/{current_user.id}_profile.jpg"
        with open(photo_path, "wb") as buffer:
            buffer.write(await photo.read())
        db_user.photo = photo_path
    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return UserResponse(
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active,
        bio=db_user.bio,
        phone=db_user.phone,
    )

@router.put("/profile/reset-password")
def reset_password(
    password_data: PasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.id == current_user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.password = get_password_hash(password_data.new_password)
    db.commit()
    db.refresh(db_user)
    return {"message": "Password updated successfully"}

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@router.post("/profile/upload-photo")
async def upload_photo(
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.id == current_user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    photo_path = f"uploads/{current_user.id}_profile.jpg"
    with open(photo_path, "wb") as buffer:
        buffer.write(await photo.read())

    db_user.photo = photo_path
    db.commit()
    db.refresh(db_user)

    return {"message": "Photo uploaded successfully", "photo_url": photo_path}