from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_100

if TYPE_CHECKING:
    from .cities import City


class Street(Base):
    __tablename__ = 'streets'

    name: Mapped[str_100]
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id', ondelete='RESTRICT'))

    city: Mapped['City'] = relationship(back_populates='streets')
