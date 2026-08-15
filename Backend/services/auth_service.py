from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from repository.user_repo import UserRepository
from models.user import User
from services.security import hash_password, verify_password, create_access_token


class AuthService:
    """Сервіс для бізнес-логіки авторизації та керування користувачами."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(self, username: str, password: str) -> User:
        existing = await self.user_repo.get_by_username(username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Користувач з таким ім'ям вже існує.",
            )
        hashed = hash_password(password)
        return await self.user_repo.create(username=username, password=hashed)

    async def authenticate(self, username: str, password: str) -> str:
        user = await self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний логін або пароль.",
            )
        return create_access_token(subject=user.username)
