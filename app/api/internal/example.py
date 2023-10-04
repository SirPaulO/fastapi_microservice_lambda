import logging

from db.deps import get_session
from fastapi import APIRouter, Depends, Path
from schemas import InternalExampleOutput
from services.example_service import ExampleService
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(f"app.{__name__}")


@router.get("/{uuid}")
def get_user(
    session: Session = Depends(get_session),
    uuid: str = Path(..., title="UUID", description="Example's UUID"),
) -> InternalExampleOutput:
    example = ExampleService.get_example_by_uuid(session, uuid)
    return example
