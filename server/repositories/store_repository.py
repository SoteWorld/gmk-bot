from __future__ import annotations

from typing import Any, List, Optional

from server.models import Store
from server.constants import STORE_TTL

from server.services.geocoder import Geocoder
from .base_redis_repository import BaseRedisRepository


class StoreRedisRepository(BaseRedisRepository):
    """CRUD-операции для моделей Store в Redis."""

    async def add_store(self, store: Store, ttl: int | None = STORE_TTL) -> None:
        await self._update_geocode_store(store)
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

    async def clear_stores(self) -> None:
        """Удаляет из Redis все записи о магазинах."""
        await self._delete_by_pattern("store:*")

    async def list_stores(self) -> List[Store]:
        keys = await self._scan_keys("store:*")
        stores: List[Store] = []
        for key in keys:
            data = await self._get_json(key)
            if data:
                stores.append(Store.model_validate(data))
        return stores

    @classmethod
    async def _update_geocode_store(cls, store: Store) -> Store:
        """Обновляет координаты магазина."""
        geocoder = Geocoder()
        latitude, longitude = await geocoder.geocode(store.address)
        store.latitude = latitude
        store.longitude = longitude
        return store