import asyncio
from database.session import session_factory
from repository.user_repo import UserRepository
from settings.config import config
from services.security import hash_password


async def seed():
    async with session_factory() as session:
        repo = UserRepository(session)
        existing = await repo.get_by_username(config.app.seed_username)
        if not existing:
            hashed = hash_password(config.app.seed_password)
            await repo.create(username=config.app.seed_username, password=hashed)
            await session.commit()
            print(f"Created user: {config.app.seed_username}")
        else:
            print(f"User {config.app.seed_username} already exists.")


if __name__ == "__main__":
    asyncio.run(seed())
