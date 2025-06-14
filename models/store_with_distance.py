from __future__ import annotations

from typing import Optional
from pydantic import Field

from .store import Store


class StoreWithDistance(Store):
    """Модель Store расширена расстоянием и URL маршрута."""
    distance: float = Field(..., description="Расстояние до пользователя в км")
    route_url: Optional[str] = Field(
        None, description="Ссылка для построения маршрута до магазина"
    )