from __future__ import annotations

from typing import List, Optional, Tuple

from server.models import Product, StoreWithDistance
from server.repositories import RedisRepository

from .data_loader import DataLoader
from .geocoder import Geocoder


class DataProvider:
    """Сервис, загружающий данные из Redis и обновляющий их, если они пусты."""
    def __init__(
        self,
        repository: Optional[RedisRepository] = None,
        *,
        data_loader: Optional[DataLoader] = None,
    ) -> None:
        self.repository = repository or RedisRepository()
        self.data_loader = data_loader or DataLoader(repository=self.repository)
        self._geocoder = Geocoder()

    async def list_stores_sorted(
        self, user_location: Tuple[float, float]
    ) -> List[StoreWithDistance]:
        """Возвращает все магазины, отсортированные по расстоянию к пользователю."""
        stores = await self.repository.list_stores()
        if not stores:
            await self.data_loader.reload_stores(clear=True)
            stores = await self.repository.list_stores()
        if not stores:
            return []

        user_lat, user_lon = user_location
        stores_with_distance: List[StoreWithDistance] = []
        for store in stores:
            if store.latitude is not None and store.longitude is not None:
                distance = self._geocoder.distance(
                    (user_lat, user_lon), (store.latitude, store.longitude)
                )
                route = self._geocoder.route_url(
                    (user_lat, user_lon), (store.latitude, store.longitude)
                )
            else:
                distance = float("0")
                route = None
            stores_with_distance.append(
                StoreWithDistance(
                    **store.model_dump(), distance=distance, route_url=route
                )
            )
        stores_with_distance.sort(key=lambda x: x.distance)
        return stores_with_distance

    async def list_products(self) -> List[Product]:
        """Возвращает все продукты из Redis."""
        products = await self.repository.list_products()
        if not products:
            await self.data_loader.reload_products(clear=True)
            products = await self.repository.list_products()
        return products or []

    async def list_categories(self) -> List[str]:
        """Возвращает все доступные категории продуктов."""
        products = await self.list_products()
        categories = {product.category for product in products if product.category}
        priority = {"fresh": 0, "other": 2}
        return sorted(categories, key=lambda c: (priority.get(c, 1), c))

    async def list_products_by_category(self, category: str) -> List[Product]:
        """Возвращает продукты, принадлежащие указанной категории."""
        products = await self.list_products()
        return [p for p in products if p.category == category]