from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_100

if TYPE_CHECKING:
    from .organizations import Organization


class Phone(Base):
    __tablename__ = 'phones'

    number: Mapped[str_100] = mapped_column(unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id', ondelete='CASCADE'))

    organization: Mapped['Organization'] = relationship(back_populates='phones')
