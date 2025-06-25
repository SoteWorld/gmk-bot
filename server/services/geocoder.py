from __future__ import annotations

from typing import Optional, Tuple

from geopy.geocoders import ArcGIS
from geopy.adapters import AioHTTPAdapter
from geopy.distance import geodesic

from server.constants import GEOCODER_TIMEOUT

class Geocoder:
    """Простой асинхронный геокодер с использованием Nominatim."""

    def __init__(self) -> None:
        # Use an asynchronous adapter to avoid blocking calls
        self._geocoder = ArcGIS(
            timeout=GEOCODER_TIMEOUT, adapter_factory=AioHTTPAdapter
        )

    async def geocode(self, query: str) -> Tuple[Optional[float], Optional[float]]:
        """Возвращает координаты места по текстовому адресу."""
        try:
            query = "Беларусь, " + query
            query = query.replace("г.", "город")
            async with self._geocoder as geocoder:
                location = await geocoder.geocode(query=query)
        except Exception:
            return None, None

        if location:
            return location.latitude, location.longitude
        return None, None

    @staticmethod
    def distance(
            origin: Tuple[float, float], destination: Tuple[float, float]
    ) -> float:
        """Возвращает расстояние между двумя точками в километрах."""
        return geodesic(origin, destination).kilometers

    @staticmethod
    def route_url(
            origin: Tuple[float, float], destination: Tuple[float, float]
    ) -> str:
        """Формирует ссылку для построения маршрута на OpenStreetMap."""
        o_lat, o_lon = origin
        d_lat, d_lon = destination
        return (
            "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car"
            f"&route={o_lat}%2C{o_lon}%3B{d_lat}%2C{d_lon}"
        )
