from typing import Any, TypeVar

from db.base_class import Base
from sqlalchemy.ext.declarative import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=Base)


class Model(DeclarativeMeta):
    """
    This class is used to simulate a model of an SQLAlchemy table
    and try not to trick MyPy with too many type hints.

    It also serves as a validator for the @model_required decorator.
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # Not used, but needed to make MyPy happy
        pass

    def __getattribute__(self, item: Any) -> Any:
        # Not used, but needed to make MyPy happy
        pass
