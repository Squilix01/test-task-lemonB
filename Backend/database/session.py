from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from database.engine import engine


session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
