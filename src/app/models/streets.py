from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_100

if TYPE_CHECKING:
    from .buildings import Building
    from .cities import City


class Street(Base):
    __tablename__ = 'streets'

    name: Mapped[str_100]
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id', ondelete='RESTRICT'))

    city: Mapped['City'] = relationship(back_populates='streets')
    buildings: Mapped[list['Building']] = relationship(
        back_populates='street',
        passive_deletes=True,
    )

    __table_args__ = (UniqueConstraint('name', 'city_id', name='name_city_uc'),)
