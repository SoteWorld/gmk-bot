from __future__ import annotations

from typing import List, Optional

from server.parsers import ProductParser, StoreParser
from server.models import Product, Store
from server.repositories import RedisRepository


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

    async def reload_products(self, ttl: int | None = 1800, clear: bool = True) -> List[Product]:
        if clear: await self.repository.clear_products()
        products = await self.product_parser.parse()
        if not products:
            return []
        for product in products:
            await self.repository.add_product(product, ttl=ttl)
        return products

    async def reload_stores(self, ttl: int | None = 1800, clear: bool = True) -> List[Store]:
        if clear: await self.repository.clear_stores()
        stores = await self.store_parser.parse()
        if not stores:
            return []
        for store in stores:
            await self.repository.add_store(store, ttl=ttl)
        return stores

    async def reload_all(self, ttl: int | None = 1800) -> None:
        await self.repository.flush()
        await self.reload_products(ttl=ttl, clear=False)
        await self.reload_stores(ttl=ttl, clear=False)

    async def close(self) -> None:
        await self.repository.close()
