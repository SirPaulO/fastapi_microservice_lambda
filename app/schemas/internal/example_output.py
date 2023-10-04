from pydantic import Field
from schemas.base import CamelModel


class InternalExampleOutput(CamelModel):
    """
    Always specify Field with description and example for documentation
    """

    uuid: str = Field(..., description="User UUID", example="test")
    text: str = Field(..., description="Text", example="user_example")
