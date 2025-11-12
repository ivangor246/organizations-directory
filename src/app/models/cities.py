from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_100

if TYPE_CHECKING:
    from .streets import Street


class City(Base):
    __tablename__ = 'cities'

    name: Mapped[str_100] = mapped_column(unique=True)

    streets: Mapped[list['Street']] = relationship(
        back_populates='city',
        passive_deletes=True,
    )
