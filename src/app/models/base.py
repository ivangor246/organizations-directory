from datetime import datetime
from typing import Annotated

from sqlalchemy import Numeric, String, func, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

str_1 = Annotated[str, 1]
str_10 = Annotated[str, 10]
str_100 = Annotated[str, 100]
str_255 = Annotated[str, 255]
num_9_6 = Annotated[float, (9, 6)]


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    type_annotation_map = {
        str_1: String(1),
        str_10: String(10),
        str_100: String(100),
        str_255: String(255),
        num_9_6: Numeric(9, 6),
    }

    def to_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
