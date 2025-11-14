from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.buildings import Building
from app.models.cities import City
from app.models.streets import Street


async def create_city(pg_session: AsyncSession, name: str) -> None:
    city = City(name=name)
    pg_session.add(city)
    await pg_session.commit()


async def get_city(pg_session: AsyncSession, id: int) -> City:
    stmt = select(City).where(City.id == id)
    result = await pg_session.execute(stmt)
    return result.scalar_one()


async def create_street(pg_session: AsyncSession, city_id: int, name: str) -> None:
    street = Street(city_id=city_id, name=name)
    pg_session.add(street)
    await pg_session.commit()


async def get_street(pg_session: AsyncSession, id: int) -> Street:
    stmt = select(Street).where(Street.id == id)
    result = await pg_session.execute(stmt)
    return result.scalar_one()


async def create_building(
    pg_session: AsyncSession,
    street_id: int,
    number: int,
    detail: int,
    latitude: float,
    longitude: float,
) -> None:
    building = Building(street_id=street_id, number=number, detail=detail, latitude=latitude, longitude=longitude)
    pg_session.add(building)
    await pg_session.commit()


async def get_building(pg_session: AsyncSession, id: int) -> Building:
    stmt = select(Building).where(Building.id == id)
    result = await pg_session.execute(stmt)
    return result.scalar_one()
