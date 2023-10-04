from api.external import example
from fastapi import APIRouter

api_router = APIRouter()

# External
api_router.include_router(example.router, tags=["External"])
