from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import register_user, authenticate_user, create_auth_token
from app.db.session import get_db
from app.core.config import settings
import httpx
from fastapi.responses import RedirectResponse
from app.services.auth_service import get_current_user, get_google_oauth2_config, create_jwt_token
from app.models.user import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    return {"access_token": token, "token_type": "bearer"}

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

