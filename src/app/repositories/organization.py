from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.organizations import Organization, activity_organization_association

from .base import Repository


class OrganizationRepository(Repository[Organization]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Organization)

    def add(self, organization: Organization) -> None:
        super().add(organization)

    async def get(self, id: int) -> Organization:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.building),
                selectinload(Organization.phones),
            )
            .where(Organization.id == id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def associate_with_activity(self, id: int, activity_id: int) -> None:
        stmt = activity_organization_association.insert().values(
            activity_id=activity_id,
            organization_id=id,
        )
        await self._session.execute(stmt)
