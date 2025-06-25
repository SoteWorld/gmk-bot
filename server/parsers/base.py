from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import aiohttp

from server.constants import HTTP_OK


class BaseParser(ABC):
    """Базовый класс для асинхронных HTML-парсеров."""

    def __init__(self, url: str) -> None:
        self.url = url

    async def fetch_html(self, session: aiohttp.ClientSession) -> Optional[str]:
        async with session.get(self.url) as response:
            if response.status != HTTP_OK:
                return None
            return await response.text()

    @abstractmethod
    async def parse(self):
        """Return parsed objects."""
        raise NotImplementedError