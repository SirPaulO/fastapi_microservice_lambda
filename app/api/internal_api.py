from api.internal import example
from fastapi import APIRouter

api_router = APIRouter()

# Internal
api_router.include_router(example.router, tags=["Internal"])
