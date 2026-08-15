from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        self.session.add(user)
        await self.session.flush()
        return user
