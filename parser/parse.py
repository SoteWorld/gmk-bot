import aiohttp
import asyncio
from bs4 import BeautifulSoup

class AsyncProductParser:
    def __init__(self, url):
        self.url = url

    async def fetch_html(self, session):
        """Асинхронно загружает HTML страницы."""
        async with session.get(self.url) as response:
            return await response.text() if response.status == 200 else None

    async def parse_product_name(self, product_item):
        """Асинхронно извлекает название продукта."""
        name_tag = product_item.find('h3', class_='page-fresh__name')
        return name_tag.get_text(strip=True) if name_tag else None

    async def parse_product_img(self, product_item):
        """Асинхронно извлекает URL изображения."""
        img_tag = product_item.find('img')
        return img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

    async def parse_product_expiration(self, product_item):
        """Асинхронно извлекает срок годности."""
        p_tags = product_item.find_all('p')
        for p in p_tags:
            if "Срок годности:" in p.get_text():
                span = p.find('span')
                return span.get_text(strip=True) if span else None
        return None

    async def parse_product_ingredients(self, product_item):
        """Асинхронно извлекает состав."""
        p_tags = product_item.find_all('p')
        for p in p_tags:
            if "Состав:" in p.get_text():
                span = p.find('span')
                return span.get_text(strip=True) if span else None
        return None

    async def parse_products(self):
        """Асинхронно обходит все товары и собирает данные."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session)
            if not html:
                return None

            soup = BeautifulSoup(html, 'html.parser')
            products = []

            tasks = []
            for product_item in soup.find_all('div', class_='page-fresh__column'):
                tasks.append(asyncio.gather(
                    self.parse_product_name(product_item),
                    self.parse_product_img(product_item),
                    self.parse_product_expiration(product_item),
                    self.parse_product_ingredients(product_item)
                ))

            results = await asyncio.gather(*tasks)

            for result in results:
                products.append({
                    'Название': result[0],
                    'Картинка': result[1],
                    'Срок годности': result[2],
                    'Состав': result[3]
                })

            return products

# Запуск:
async def main():
    parser = AsyncProductParser("https://mkgomel.by")
    products = await parser.parse_products()
    print(products)

asyncio.run(main())
