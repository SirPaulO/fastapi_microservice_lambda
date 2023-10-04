import logging
from typing import Dict, Union

from exceptions.generic import GenericException
from fastapi import APIRouter, Body
from fastapi_versioning import version
from schemas import ExternalExampleInput, ExternalExampleOutput
from services.example_service import ExampleService
from starlette import status

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.post("/example")
@version(1, 0)
def example(example_input: ExternalExampleInput = Body(...)) -> ExternalExampleOutput:
    sum_result = ExampleService.get_sum(example_input.num_a, example_input.num_b)

    is_correct_sum = sum_result == example_input.sum
    logger.info(f"is_correct_sum: {is_correct_sum}")

    if is_correct_sum:
        return ExternalExampleOutput(is_correct=is_correct_sum)

    raise GenericException(GenericException.ErrorCode.Incorrect_Sum)


@router.get("/")
async def external_root() -> Dict:
    logger.info("external_root endpoint log info")
    return {"hello": "world"}


@router.get("/exception", status_code=status.HTTP_200_OK)
async def throw_exception() -> None:
    # Throws custom error code anyway
    raise GenericException(GenericException.ErrorCode.Generic_Exception)


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None) -> Dict:
    return {"item_id": item_id, "q": q}
