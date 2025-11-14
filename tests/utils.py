from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.activities import Activity
from app.models.buildings import Building
from app.models.cities import City
from app.models.organizations import Organization, activity_organization_association
from app.models.phones import Phone
from app.models.streets import Street


async def create_phone(pg_session: AsyncSession, number: str, organization_id: int) -> None:
    phone = Phone(number=number, organization_id=organization_id)
    pg_session.add(phone)
    await pg_session.commit()


async def get_phone(pg_session: AsyncSession, id: int) -> Phone:
    stmt = select(Phone).where(Phone.id == id)
    result = await pg_session.execute(stmt)
    return result.scalar_one()


async def create_organization(pg_session: AsyncSession, name: str, building_id: int) -> None:
    organization = Organization(name=name, building_id=building_id)
    pg_session.add(organization)
    await pg_session.commit()


async def get_organization(pg_session: AsyncSession, id: int) -> Organization:
    stmt = (
        select(Organization)
        .options(
            selectinload(Organization.activities),
            selectinload(Organization.building),
            selectinload(Organization.phones),
        )
        .where(Organization.id == id)
    )
    result = await pg_session.execute(stmt)
    return result.scalar_one()


async def connect_activity_and_organization(pg_session: AsyncSession, activity_id: int, organization_id: int) -> None:
    stmt = activity_organization_association.insert().values(
        activity_id=activity_id,
        organization_id=organization_id,
    )
    await pg_session.execute(stmt)
    await pg_session.commit()


async def create_activity(pg_session: AsyncSession, name: str, parent_id: int | None = None) -> None:
    depth = 0
    if parent_id is not None:
        stmt = select(Activity).where(Activity.id == parent_id)
        result = await pg_session.execute(stmt)
        parent = result.scalar_one()
        depth = parent.depth + 1

    activity = Activity(name=name, depth=depth, parent_id=parent_id)
    pg_session.add(activity)
    await pg_session.commit()


async def get_activity(pg_session: AsyncSession, id: int) -> Activity:
    stmt = select(Activity).where(Activity.id == id)
    result = await pg_session.execute(stmt)
    return result.scalar_one()


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
