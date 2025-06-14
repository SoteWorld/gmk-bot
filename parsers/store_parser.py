from __future__ import annotations

from typing import Optional, List

import aiohttp
from bs4 import BeautifulSoup

from models import Store
from parsers.base import BaseParser


class StoreParser(BaseParser):
    """Парсер списка магазинов с веб-страницы."""
    DEFAULT_URL = "https://mkgomel.by/firmennaya-torgovlya"

    def __init__(self, url: str = DEFAULT_URL) -> None:
        super().__init__(url)

    @classmethod
    def _parse_name(cls, item) -> Optional[str]:
        """Извлекает название магазина."""
        tag = item.find("h2", class_="module-page__decor-title")
        return tag.get_text(strip=True) if tag else None

    @classmethod
    def _parse_address(cls, item) -> Optional[str]:
        """Извлекает адрес магазина."""
        for p in item.find_all("p"):
            if "Адрес:" in p.get_text():
                return p.get_text(strip=True).replace("Адрес:", "").strip()
        return None

    @classmethod
    def _parse_hours(cls, item) -> Optional[str]:
        """Извлекает режим работы магазина."""
        for p in item.find_all("p"):
            if "Режим работы:" in p.get_text():
                return p.get_text(strip=True).replace("Режим работы:", "").strip()
        return None

    @classmethod
    def _parse_phone(cls, item) -> Optional[str]:
        """Извлекает телефон магазина."""
        for p in item.find_all("p"):
            if "Телефон:" in p.get_text():
                return p.get_text(strip=True).replace("Телефон:", "").strip()
        return None


    async def parse(self) -> Optional[List[Store]]:
        """Собирает данные о всех магазинах с сайта и приводит их к модели Store."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session)
            if not html:
                return None

            soup = BeautifulSoup(html, "html.parser")
            stores: List[Store] = []
            for item in soup.find_all("div", class_="module-page__column-md2"):
                stores.append(
                    Store(
                        name=self._parse_name(item),
                        address=self._parse_address(item),
                        opening_hours=self._parse_hours(item),
                        phone=self._parse_phone(item),
                        latitude=None,
                        longitude=None,
                    )
                )
            return stores
