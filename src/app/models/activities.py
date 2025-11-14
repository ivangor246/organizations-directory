from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_100
from .organizations import activity_organization_association

if TYPE_CHECKING:
    from .organizations import Organization


class Activity(Base):
    __tablename__ = 'activities'

    name: Mapped[str_100] = mapped_column(unique=True)
    depth: Mapped[int] = mapped_column(default=0)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('activities.id', ondelete='RESTRICT'))

    parent: Mapped['Activity'] = relationship(
        back_populates='children',
        remote_side='Activity.id',
    )
    children: Mapped[list['Activity']] = relationship(
        back_populates='parent',
        passive_deletes=True,
    )
    organizations: Mapped[list['Organization']] = relationship(
        secondary=activity_organization_association,
        back_populates='activities',
        passive_deletes=True,
    )
