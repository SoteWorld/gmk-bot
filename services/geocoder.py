from __future__ import annotations

import asyncio
from typing import Optional, Tuple

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


class Geocoder:
    """Простой асинхронный геокодер с использованием Nominatim."""

    def __init__(self, user_agent: str = "gmk-bot") -> None:
        self._geocoder = Nominatim(user_agent=user_agent)
        self._rate_limited = RateLimiter(self._geocoder.geocode, min_delay_seconds=1)

    async def geocode(self, query: str) -> Tuple[Optional[float], Optional[float]]:
        """"""
        loop = asyncio.get_event_loop()
        try:
            location = await loop.run_in_executor(None, self._rate_limited, query)
        except Exception:
            return None, None
        if location:
            return location.latitude, location.longitude
        return None, None