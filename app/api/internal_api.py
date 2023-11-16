from api.internal import aws, example
from fastapi import APIRouter

api_router = APIRouter()

# Internal
api_router.include_router(example.router, tags=["Internal"])

# Internal - AWS
api_router.include_router(aws.router, tags=["Internal - AWS"])
