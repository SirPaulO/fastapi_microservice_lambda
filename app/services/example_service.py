from exceptions.generic import GenericException
from models.example import Example
from sqlalchemy.orm import Session


class ExampleService:
    """
    This class serves as an example of how to use services.
    """

    @staticmethod
    def get_example_by_uuid(session: Session, uuid: str) -> Example:
        """
        Gets an example by its uuid.

        :param session: ORM Session
        :param uuid: UUID to search in db
        :return: Example instance
        """
        example = session.query(Example).filter(Example.uuid == uuid).first()
        if not example:
            raise GenericException(GenericException.ErrorCode.Not_Found)
        return example

    @staticmethod
    def get_sum(num_a: float, num_b: float) -> float:
        return num_a + num_b
