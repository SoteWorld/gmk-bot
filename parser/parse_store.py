import aiohttp
import asyncio
from bs4 import BeautifulSoup
from models import Store
# Импортируем модель Store из внешнего файла (файл с моделью менять не нужно)
from models import store
# Предполагается, что класс Store определён в файле store.py

class AsyncStoreParser:
    def __init__(self, url: str):
        self.url = url

    async def fetch_html(self, session: aiohttp.ClientSession) -> str:
        """Асинхронно загружает HTML страницы."""
        async with session.get(self.url) as response:
            return await response.text() if response.status == 200 else None

    async def parse_store_name(self, store_item) -> str:
        """Извлекает название магазина."""
        name_tag = store_item.find('h2', class_='module-page__decor-title')
        return name_tag.get_text(strip=True) if name_tag else None

    async def parse_store_address(self, store_item) -> str:
        """Извлекает адрес магазина."""
        for p_tag in store_item.find_all('p'):
            if "Адрес:" in p_tag.get_text():
                return p_tag.get_text(strip=True).replace("Адрес:", "").strip()
        return None

    async def parse_store_hours(self, store_item) -> str:
        """Извлекает режим работы магазина."""
        for p_tag in store_item.find_all('p'):
            if "Режим работы:" in p_tag.get_text():
                return p_tag.get_text(strip=True).replace("Режим работы:", "").strip()
        return None

    async def parse_store_phone(self, store_item) -> str:
        """Извлекает телефон магазина."""
        for p_tag in store_item.find_all('p'):
            if "Телефон:" in p_tag.get_text():
                return p_tag.get_text(strip=True).replace("Телефон:", "").strip()
        return None

    async def parse_stores(self) -> list:
        """
        Асинхронно обходит все магазины, собирает данные
        и приводит их к модели Store.
        """
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session)
            if not html:
                return None

            soup = BeautifulSoup(html, 'html.parser')
            stores = []
            tasks = []

            # Ищем все блоки магазинов по соответствующему CSS-классу
            for store_item in soup.find_all('div', class_='module-page__column-md2'):
                tasks.append(
                    asyncio.gather(
                        self.parse_store_name(store_item),
                        self.parse_store_address(store_item),
                        self.parse_store_hours(store_item),
                        self.parse_store_phone(store_item)
                    )
                )

            results = await asyncio.gather(*tasks)

            # Для каждого результата создаём объект модели Store
            for result in results:
                store_obj = Store(
                    name=result[0],
                    address=result[1],
                    opening_hours=result[2],
                    phone=result[3],
                    latitude=None,
                    longitude=None
                )
                stores.append(store_obj)

            return stores

async def main():
    parser = AsyncStoreParser("https://mkgomel.by/firmennaya-torgovlya/")
    stores = await parser.parse_stores()
    if stores:
        # Вывод в виде списка словарей (можно использовать .dict() для каждого объекта)
        print([store.model_dump() for store in stores])

    else:
        print("Не удалось получить данные.")

if __name__ == '__main__':
    asyncio.run(main())
