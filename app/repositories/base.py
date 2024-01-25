"""
The idea of the BaseRepository is simply to abstract the CRUD operations,
thus allowing to respect the same flow for all other repositories.

Q: Why not use the ABC module?
A: Because there would be many decorators and the messages they return are not so explicit.
"""

import os
from functools import wraps
from typing import Any, Callable, List, Optional, Union, cast, no_type_check

from schemas.types import Model, ModelType
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


# region Decorators
@no_type_check
def model_required(method: classmethod) -> Any:
    """Check if model is assigned in the inheritance"""

    @wraps(method)
    def wrapper(self=None, *args: Any, **kwargs: Any) -> Any:
        if self is None:
            raise TypeError(f"The '{method.__name__}' is not a class method")
        if not isinstance(self.model, type(Model)):
            raise ValueError(f"The '{self.__name__}' unassigned model's instance")
        return method(self, *args, **kwargs)

    return wrapper


@no_type_check
def only_tests(method_or_func: Union[classmethod, staticmethod, Callable[..., Any]]) -> Any:
    """Limits its use, it can only be used in test environments."""

    @wraps(method_or_func)
    def wrapper(self=None, *args: Any, **kwargs: Any) -> Any:
        if not os.environ.get("PYTEST_RUNNING") == "true":
            raise NotImplementedError("You cannot use this method outside test environment")
        if self:
            return method_or_func(self, *args, **kwargs)
        return method_or_func(*args, **kwargs)

    return wrapper


# endregion


class ModelRepository:
    model: Any = cast(Model, None)

    def __init__(self, session: Session):
        self.session = session

    @model_required
    def save(self, instance: ModelType) -> ModelType:
        """
        Saves a model instance in the database.
        IMPORTANT: This method may be overridden.

        :param instance: Model instance
        :returns: an instance of the model
        """
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    @model_required
    def get(self, pk: Union[int, str]) -> Optional[ModelType]:
        """
        Gets a record by its primary key or None if it does not exist.

        :param pk: record's primary key.
        :return: an instance of model or None, example: <ModelType 1> | None
        """
        return self.session.query(self.model).get(pk)

    @model_required
    def get_all(self) -> List[ModelType]:
        """
        Gets all records from the table.

        :return: a list of models, example = ["<ModelType 1>", "<ModelType 2>", ...]
        """
        return self.session.query(self.model).all()  # noqa

    def __update(self, instance: ModelType, **new_values: Any) -> ModelType:
        for attribute, new_value in new_values.items():
            setattr(instance, attribute, new_value)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    @model_required
    def update(self, pk: Union[int, str], **kwargs: Any) -> Optional[ModelType]:
        """
        Updates a record by its primary key.

        :param pk: record's primary key
        :param kwargs: new values for the record
        :return: The updated record as model
        """
        instance = self.get(pk)
        return self.__update(instance, **kwargs) if instance else None

    @model_required
    def update_instance(self, instance: ModelType, **kwargs: Any) -> ModelType:
        """
        Updates a record by its instance.

        :param instance: ModelType instance
        :param kwargs:  the new values of record
        :return: The updated model
        """
        return self.__update(instance, **kwargs)

    @model_required
    def delete(self, pk: Union[str, int]) -> ModelType:
        """
        Deletes a record by its primary key.

        :param pk: record's primary key.
        :returns: a deleted instance.
        """
        instance = self.get(pk)
        if instance:
            self.session.delete(instance)
            self.session.commit()
        return instance

    @model_required
    def delete_instance(self, instance: ModelType) -> ModelType:
        """
        Deletes a record by its instance.

        :param instance: ModelType instance
        :returns: the deleted instance
        """
        self.session.delete(instance)
        self.session.commit()
        return instance

    @model_required
    def bulk_insert(self, list_instances: List[ModelType]) -> bool:
        """
        Inserts a list of instances in the database.

        :param list_instances: A list of instances to be inserted
        :returns: True if the operation is completed, False if an error generated.
        """
        try:
            self.session.bulk_save_objects(list_instances)
            self.session.commit()
            return True
        except SQLAlchemyError:
            return False

    @model_required
    def count(self) -> int:
        """
        Counts the number of rows in the table.

        Returns: returns the total number of rows in the table
        """
        return self.session.query(self.model).count()
