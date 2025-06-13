import aiohttp
import asyncio
import re
from datetime import date, timedelta
from bs4 import BeautifulSoup
from models import Product

class AsyncProductParser:
    def __init__(self, url: str):
        self.url = url

    async def fetch_html(self, session: aiohttp.ClientSession) -> str:
        """Асинхронно загружает HTML страницы."""
        async with session.get(self.url) as response:
            return await response.text() if response.status == 200 else None

    async def parse_product_name(self, product_item) -> str:
        """Извлекает название продукта."""
        name_tag = product_item.find('h3', class_='page-fresh__name')
        return name_tag.get_text(strip=True) if name_tag else None

    async def parse_product_img(self, product_item) -> str:
        """Извлекает URL изображения продукта."""
        img_tag = product_item.find('img')
        return img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

    async def parse_product_expiration(self, product_item) -> str:
        """
        Извлекает срок годности продукта.
        Если в теге содержится текст вида "60 суток", возвращает этот текст.
        Если формат не соответствует ожидаемому, возвращается None.
        """
        p_tags = product_item.find_all('p')
        for p in p_tags:
            if "Срок годности:" in p.get_text():
                span = p.find('span')
                if span:
                    exp_text = span.get_text(strip=True)
                    return exp_text
        return None

    async def parse_product_ingredients(self, product_item) -> str:
        """Извлекает состав продукта."""
        p_tags = product_item.find_all('p')
        for p in p_tags:
            if "Состав:" in p.get_text():
                span = p.find('span')
                return span.get_text(strip=True) if span else None
        return None

    async def parse_products(self) -> list:
        """Асинхронно обходит все товары и приводит полученные данные к модели Product."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session)
            if not html:
                return None

            soup = BeautifulSoup(html, 'html.parser')
            tasks = []
            for product_item in soup.find_all('div', class_='page-fresh__column'):
                tasks.append(asyncio.gather(
                    self.parse_product_name(product_item),
                    self.parse_product_img(product_item),
                    self.parse_product_expiration(product_item),
                    self.parse_product_ingredients(product_item)
                ))

            results = await asyncio.gather(*tasks)
            products = []
            for result in results:
                product_obj = Product(
                    name=result[0],
                    image=result[1],
                    expiration_date=result[2],
                    ingredients=result[3],
                    description=None
                )
                products.append(product_obj)

            return products

async def main():
    parser = AsyncProductParser("https://mkgomel.by")
    products = await parser.parse_products()
    if products:
        print([product.model_dump() for product in products])
    else:
        print("Не удалось получить данные.")

if __name__ == '__main__':
    asyncio.run(main())
