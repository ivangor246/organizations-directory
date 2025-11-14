from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cities import City


async def create_city(pg_session: AsyncSession, name: str) -> None:
    city = City(name=name)
    pg_session.add(city)
    await pg_session.commit()


async def get_city(pg_session: AsyncSession, id: int) -> City:
    stmt = select(City).where(City.id == id)
    result = await pg_session.execute(stmt)
    return result.scalar_one()
