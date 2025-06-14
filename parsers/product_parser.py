from __future__ import annotations

import asyncio
import pprint
from typing import Optional, List

import aiohttp
from bs4 import BeautifulSoup

from models import Product
from parsers.base import BaseParser


class ProductParser(BaseParser):
    """Парсер списка продуктов с веб-страницы."""
    DEFAULT_URL = "https://mkgomel.by"

    def __init__(self, url: str = DEFAULT_URL) -> None:
        """Инициализирует парсер с помощью необязательного URL страницы."""
        super().__init__(url)

    @classmethod
    def _parse_name(cls, item) -> Optional[str]:
        """Извлекает название продукта."""
        tag = item.find("h3", class_="page-fresh__name")
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

    async def parse(self) -> Optional[List[Product]]:
        """Собирает данные о всех новых продуктах с сайта и приводит их к модели Product."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session)
            if not html:
                return None

            soup = BeautifulSoup(html, "html.parser")
            products: List[Product] = []
            for item in soup.find_all("div", class_="page-fresh__column"):
                products.append(
                    Product(
                        name=self._parse_name(item),
                        image=self._parse_image(item),
                        expiration_date=self._parse_expiration(item),
                        ingredients=self._parse_ingredients(item),
                    )
                )
            return products


async def main():
    parser = ProductParser()
    products = await parser.parse()
    if products:
        pprint.pprint([product.model_dump() for product in products])
    else:
        print("Не удалось получить данные.")

if __name__ == '__main__':
    asyncio.run(main())