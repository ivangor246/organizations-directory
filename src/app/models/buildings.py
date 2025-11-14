from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, num_9_6, str_10, str_255

if TYPE_CHECKING:
    from .organizations import Organization
    from .streets import Street


class Building(Base):
    __tablename__ = 'buildings'

    street_id: Mapped[int] = mapped_column(ForeignKey('streets.id', ondelete='RESTRICT'))
    number: Mapped[str_10]
    detail: Mapped[str_255]
    latitude: Mapped[num_9_6]
    longitude: Mapped[num_9_6]

    street: Mapped['Street'] = relationship(back_populates='buildings')
    organization: Mapped['Organization'] = relationship(
        back_populates='building',
        passive_deletes=True,
        uselist=False,
    )

    __table_args__ = (UniqueConstraint('number', 'street_id', name='number_street_uc'),)
