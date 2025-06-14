from __future__ import annotations

from .base_redis_repository import BaseRedisRepository
from .product_repository import ProductRedisRepository
from .store_repository import StoreRedisRepository

class RedisRepository(ProductRedisRepository, StoreRedisRepository):
    """Совмещенный репозиторий для объектов Store и Product."""

    def __init__(self, url: str = "redis://localhost", *, decode_responses: bool = True) -> None:
        BaseRedisRepository.__init__(self, url=url, decode_responses=decode_responses)