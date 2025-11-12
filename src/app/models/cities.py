from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, str_100


class City(Base):
    __tablename__ = 'cities'

    name: Mapped[str_100] = mapped_column(unique=True)
