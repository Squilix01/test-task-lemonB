from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db, get_current_user
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from services.auth_service import AuthService
from models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(session)
    return await auth_service.register(username=data.username, password=data.password)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(session)
    access_token = await auth_service.authenticate(username=data.username, password=data.password)
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
