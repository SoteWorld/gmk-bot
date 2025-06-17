from __future__ import annotations

from typing import Optional, List

import aiohttp
from bs4 import BeautifulSoup

from server.models import Product
from server.parsers.base import BaseParser


class ProductParser(BaseParser):
    """Парсер списка продуктов с веб-страницы."""
    DEFAULT_URL = "https://mkgomel.by/category/products/"

    def __init__(self, url: str = DEFAULT_URL) -> None:
        super().__init__(url)

    @classmethod
    def _parse_name(cls, item) -> Optional[str]:
        """Извлекает название продукта."""
        tag = item.find("h2", class_="module-catalog__title")
        return tag.get_text(strip=True) if tag else None

    @classmethod
    def _parse_image(cls, item) -> Optional[str]:
        """Извлекает URL изображения продукта."""
        img = item.find("img")
        return img.get("src") if img else None

    @classmethod
    def _parse_expiration(cls, item) -> Optional[str]:
        """Извлекает срок годности продукта."""
        for p in item.find_all("p"):
            if "Срок годности:" in p.get_text():
                span = p.find("span")
                return span.get_text(strip=True) if span else None
        return None

    @classmethod
    def _parse_ingredients(cls, item) -> Optional[str]:
        """Извлекает состав продукта."""
        for p in item.find_all("p"):
            if "Состав:" in p.get_text():
                span = p.find("span")
                return span.get_text(strip=True) if span else None
        return None

    @classmethod
    def _parse_category(cls, item) -> Optional[str]:
        """Извлекает категорию продукта из классов элемента."""
        classes = item.get("class", [])
        for cls_name in classes:
            if cls_name not in {"module-catalog__column", "mix"}:
                return cls_name
        return None

    async def parse(self) -> Optional[List[Product]]:
        """Собирает данные о продуктах со страницы."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session)
            if not html:
                return None

            soup = BeautifulSoup(html, "html.parser")
            products: List[Product] = []
            for item in soup.select("div.module-catalog__column"):
                products.append(
                    Product(
                        name=self._parse_name(item),
                        image=self._parse_image(item),
                        expiration_date=self._parse_expiration(item),
                        ingredients=self._parse_ingredients(item),
                        category=self._parse_category(item),
                    )
                )
            return products
