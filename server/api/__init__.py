from __future__ import annotations

from fastapi import APIRouter

from .webhook import router as webhook_router
from .products import router as products_router
from .stores import router as stores_router


def setup_routers() -> APIRouter:
    """Configure all API routers."""

    router = APIRouter()

    # Webhook router is left without the /api prefix to avoid breaking
    # Telegram webhook URL configured in the environment variables.
    router.include_router(webhook_router)

    api_router = APIRouter(prefix="/api")
    api_router.include_router(products_router)
    api_router.include_router(stores_router)

    router.include_router(api_router)
    return router