from __future__ import annotations

from typing import Any, List, Optional

from models import Product

from .base_redis_repository import BaseRedisRepository


class ProductRedisRepository(BaseRedisRepository):
    """CRUD-операции для моделей Product в Redis."""

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