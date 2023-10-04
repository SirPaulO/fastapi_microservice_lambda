from pydantic import Field
from schemas.base import CamelModel


class ExternalExampleInput(CamelModel):
    """
    Always specify Field with description and example for documentation
    """

    num_a: float = Field(..., description="Number A", example=2.42)
    num_b: float = Field(..., description="Number B", example=3.25)
    sum: float = Field(..., description="Sum A + B", example=7.65)
