from __future__ import annotations

from typing import List, Optional

from parsers import ProductParser, StoreParser
from models import Product, Store
from .redis_repository import RedisRepository


class DataLoader:
    """Сервис для парса данных и сохранения их в Redis."""
    def __init__(
        self,
        repository: Optional[RedisRepository] = None,
        *,
        product_parser: Optional[ProductParser] = None,
        store_parser: Optional[StoreParser] = None,
    ) -> None:
        self.repository = repository or RedisRepository()
        self.product_parser = product_parser or ProductParser()
        self.store_parser = store_parser or StoreParser()

    async def load_products(self, ttl: int | None = 1800) -> List[Product]:
        products = await self.product_parser.parse()
        if not products:
            return []
        for product in products:
            await self.repository.add_product(product, ttl=ttl)
        return products

    async def load_stores(self, ttl: int | None = 1800) -> List[Store]:
        stores = await self.store_parser.parse()
        if not stores:
            return []
        for store in stores:
            await self.repository.add_store(store, ttl=ttl)
        return stores

    async def load_all(self, ttl: int | None = 1800) -> None:
        await self.load_products(ttl=ttl)
        await self.load_stores(ttl=ttl)

    async def close(self) -> None:
        await self.repository.close()