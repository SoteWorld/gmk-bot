from aiogram import Router

from . import start, help, products, stores, fallback

def setup_routers() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(help.router)
    router.include_router(products.router)
    router.include_router(stores.router)
    router.include_router(fallback.router)

    return router
