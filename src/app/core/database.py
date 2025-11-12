from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import config

engine = create_async_engine(url=config.DB_URI)


def get_session_factory() -> async_sessionmaker:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


DEFAULT_SESSION_FACTORY = get_session_factory()
