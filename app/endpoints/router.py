from fastapi import APIRouter

from . import (
    auth,
    product,
    payment
)


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(product.router, prefix="/product")
api_router.include_router(payment.router, prefix="/payment")