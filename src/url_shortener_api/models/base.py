from sqlalchemy import Integer, func
from sqlalchemy import Integer, func, Uuid
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    declared_attr,
    mapped_column,
)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__
        return name + "s"
