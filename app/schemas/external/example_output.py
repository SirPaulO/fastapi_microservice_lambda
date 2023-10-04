from pydantic import Field
from schemas.base import CamelModel


class ExternalExampleOutput(CamelModel):
    """
    Always specify Field with description and example for documentation
    """

    is_correct: bool = Field(..., description="Boolean indicating if the sum was correct", example=True)
