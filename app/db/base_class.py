from typing import Any

from humps import decamelize
from sqlalchemy import DATETIME, MetaData, func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s-%(column_0_name)s",
        "fk": "fk_%(table_name)s-%(column_0_name)s-%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    }
)


@as_declarative(metadata=meta)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return decamelize(cls.__name__)

    updated_at: Mapped[DATETIME] = mapped_column(DATETIME, nullable=True, default=func.now(), onupdate=func.now())
    created_at: Mapped[DATETIME] = mapped_column(DATETIME, nullable=True, default=func.now())
