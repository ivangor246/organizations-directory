from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import config
from app.models.base import Base


@pytest.fixture
def pg_engine() -> AsyncEngine:
    return create_async_engine(config.DB_URI)


@pytest_asyncio.fixture
async def pg_session_factory(pg_engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=pg_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def pg_session(pg_session_factory: async_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with pg_session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def clean_db(pg_session: AsyncSession) -> None:
    for table in reversed(Base.metadata.sorted_tables):
        await pg_session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))
    await pg_session.commit()
