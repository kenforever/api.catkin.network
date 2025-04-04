from fastapi import APIRouter

from . import (
    auth,
    product
)


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(product.router, prefix="/product")