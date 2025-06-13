import aiohttp
import asyncio
from bs4 import BeautifulSoup
from models import Store

class AsyncStoreParser:
    def __init__(self, url):
        self.url = url

    async def fetch_html(self, session):
        """Асинхронно загружает HTML страницы."""
        async with session.get(self.url) as response:
            return await response.text() if response.status == 200 else None

    async def parse_store_name(self, store_item):
        """Асинхронно извлекает название магазина."""
        name_tag = store_item.find('h2', class_='module-page__decor-title')
        return name_tag.get_text(strip=True) if name_tag else None

    async def parse_store_address(self, store_item):
        """Асинхронно извлекает адрес магазина."""
        for p_tag in store_item.find_all('p'):
            if "Адрес:" in p_tag.get_text():
                return p_tag.get_text(strip=True).replace("Адрес:", "").strip()
        return None

    async def parse_store_hours(self, store_item):
        """Асинхронно извлекает время работы магазина."""
        for p_tag in store_item.find_all('p'):
            if "Режим работы:" in p_tag.get_text():
                return p_tag.get_text(strip=True).replace("Режим работы:", "").strip()
        return None
    async def parse_store_phone(self, store_item):
        """Асинхронно извлекает телефон магазина."""
        for p_tag in store_item.find_all('p'):
            if "Телефон:" in p_tag.get_text():
                return p_tag.get_text(strip=True).replace("Телефон:", "").strip()
        return None
    async def parse_stores(self):
        """Асинхронно обходит все магазины и собирает данные."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session)
            if not html:
                return None

            soup = BeautifulSoup(html, 'html.parser')
            stores = []

            tasks = []
            for store_item in soup.find_all('div', class_='module-page__column-md2'):
                tasks.append(asyncio.gather(
                    self.parse_store_name(store_item),
                    self.parse_store_address(store_item),
                    self.parse_store_hours(store_item),
                    self.parse_store_phone(store_item)
                ))

            results = await asyncio.gather(*tasks)

            for result in results:
                stores.append({
                    'Название': result[0],
                    'Адрес': result[1],
                    'Режим работы': result[2],
                    'Телефон': result[3]
                })

            return stores

# Запуск:
async def main():
    parser = AsyncStoreParser("https://mkgomel.by/firmennaya-torgovlya/")
    stores = await parser.parse_stores()
    print(stores)

asyncio.run(main())
