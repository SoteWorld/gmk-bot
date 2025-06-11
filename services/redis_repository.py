from __future__ import annotations

import json
from typing import Any, List, Optional

import redis.asyncio as redis

from models import Product, Store


class RedisRepository:
    """Асинхронный репозиторий для хранения объектов Store и Product в Redis."""

    def __init__(self, url: str = "redis://localhost", *, decode_responses: bool = True):
        self._redis = redis.from_url(url, decode_responses=decode_responses)

    async def close(self) -> None:
        await self._redis.close()

    # -------------------- вспомогательные методы --------------------
    async def _set_json(self, key: str, value: Any, ttl: int | None = 1800) -> None:
        data = json.dumps(value)
        await self._redis.set(key, data, ex=ttl)

    async def _get_json(self, key: str) -> Optional[Any]:
        data = await self._redis.get(key)
        return json.loads(data) if data else None

    async def _delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def _scan_keys(self, pattern: str) -> List[str]:
        cursor = 0
        keys: List[str] = []
        while True:
            cursor, batch = await self._redis.scan(cursor=cursor, match=pattern)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys

    # -------------------- методы для Store --------------------
    async def add_store(self, store: Store, ttl: int | None = 1800) -> None:
        await self._set_json(f"store:{store.id}", store.model_dump(), ttl)

    async def get_store(self, store_id: str) -> Optional[Store]:
        data = await self._get_json(f"store:{store_id}")
        return Store.model_validate(data) if data else None

    async def update_store(self, store_id: str, **fields: Any) -> Optional[Store]:
        existing = await self.get_store(store_id)
        if not existing:
            return None
        updated = existing.model_copy(update=fields)
        await self.add_store(updated)
        return updated

    async def delete_store(self, store_id: str) -> None:
        await self._delete(f"store:{store_id}")

    async def list_stores(self) -> List[Store]:
        keys = await self._scan_keys("store:*")
        stores: List[Store] = []
        for key in keys:
            data = await self._get_json(key)
            if data:
                stores.append(Store.model_validate(data))
        return stores

    # -------------------- методы для Product --------------------
    async def add_product(self, product: Product, ttl: int | None = 1800) -> None:
        await self._set_json(f"product:{product.id}", product.model_dump(), ttl)

    async def get_product(self, product_id: str) -> Optional[Product]:
        data = await self._get_json(f"product:{product_id}")
        return Product.model_validate(data) if data else None

    async def update_product(self, product_id: str, **fields: Any) -> Optional[Product]:
        existing = await self.get_product(product_id)
        if not existing:
            return None
        updated = existing.model_copy(update=fields)
        await self.add_product(updated)
        return updated

    async def delete_product(self, product_id: str) -> None:
        await self._delete(f"product:{product_id}")

    async def list_products(self) -> List[Product]:
        keys = await self._scan_keys("product:*")
        products: List[Product] = []
        for key in keys:
            data = await self._get_json(key)
            if data:
                products.append(Product.model_validate(data))
        return products
