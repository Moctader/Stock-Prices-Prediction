import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from functools import partial
from app.db.base import Base
from app.core.settings import settings
from app.core.serializer import DatetimeAwareJSONEncoder
from app.core.logging import logger

custom_serializer = partial(
    json.dumps,
    cls=DatetimeAwareJSONEncoder,
    ensure_ascii=False
)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.POSTGRES_ECHO,
    future=True,
    isolation_level="READ COMMITTED",
    json_serializer=custom_serializer,
    pool_pre_ping=True,
    pool_timeout=1,
    pool_size=10,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def connect_with_retries(retries=5, delay=2):
    """Attempt to connect to the database with retries."""
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info(
                "Database initialized and all tables created if they didn't exist.")
            return
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} of {retries} failed: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise e


async def init_db():
    try:
        await connect_with_retries()
    except Exception as e:
        logger.error(f"Error initializing database after retries: {e}")
        raise e
