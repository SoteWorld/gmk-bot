from aiogram import Router

from . import start, products, stores

def setup_routers() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(products.router)
    router.include_router(stores.router)
    return router