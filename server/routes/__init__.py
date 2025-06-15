from __future__ import annotations

from fastapi import APIRouter

from .webhook import router as webhook_router
from .products import router as products_router
from .stores import router as stores_router


def setup_routers() -> APIRouter:
    router = APIRouter()
    router.include_router(webhook_router)
    router.include_router(products_router)
    router.include_router(stores_router)
    return router