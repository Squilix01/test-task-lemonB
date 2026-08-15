from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from settings.config import config


engine: AsyncEngine = create_async_engine(
    url=config.db.get_connection_string(),
    echo=False,
)
