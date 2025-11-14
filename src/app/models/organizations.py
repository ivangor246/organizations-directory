from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_100

if TYPE_CHECKING:
    from .activities import Activity
    from .buildings import Building
    from .phones import Phone


activity_organization_association = Table(
    'activity_organization_associations',
    Base.metadata,
    Column('activity_id', ForeignKey('activities.id', ondelete='RESTRICT'), primary_key=True),
    Column('organization_id', ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True),
)


class Organization(Base):
    __tablename__ = 'organizations'

    name: Mapped[str_100]
    building_id: Mapped[int] = mapped_column(ForeignKey('buildings.id', ondelete='RESTRICT'))

    building: Mapped['Building'] = relationship(back_populates='organization')
    activities: Mapped[list['Activity']] = relationship(
        secondary=activity_organization_association,
        back_populates='organizations',
        passive_deletes=True,
    )
    phones: Mapped[list['Phone']] = relationship(
        back_populates='organization',
        passive_deletes=True,
    )
