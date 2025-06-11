import requests
from bs4 import BeautifulSoup

class ProductParser:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        return None

    def parse_product_name(self, product_item):
        """Извлекает название продукта из тега <h3> с классом page-fresh__name."""
        name_tag = product_item.find('h3', class_='page-fresh__name')
        return name_tag.get_text(strip=True) if name_tag else None

    def parse_product_img(self, product_item):
        """Извлекает URL изображения из тега <img>."""
        img_tag = product_item.find('img')
        return img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

    def parse_product_expiration(self, product_item):
        """
        Извлекает срок годности.
        Ищет все теги <p> и проверяет, содержит ли текст фразу 'Срок годности:'.
        Если такой тег найден, возвращает текст внутри <span>.
        """
        p_tags = product_item.find_all('p')
        for p in p_tags:
            if "Срок годности:" in p.get_text():
                span = p.find('span')
                return span.get_text(strip=True) if span else None
        return None

    def parse_product_ingredients(self, product_item):
        """
        Извлекает состав продукта.
        Ищет все теги <p> и проверяет, содержит ли текст фразу 'Состав:'.
        Если такой тег найден, возвращает текст внутри <span>.
        """
        p_tags = product_item.find_all('p')
        for p in p_tags:
            if "Состав:" in p.get_text():
                span = p.find('span')
                return span.get_text(strip=True) if span else None
        return None

    def parse_products(self):
        """Обходит все товары на странице и собирает данные для каждого из них."""
        html = self.get_html()
        if not html:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        for product_item in soup.find_all('div', class_='page-fresh__column'):
            product = {
                'Название': self.parse_product_name(product_item),
                'Картинка': self.parse_product_img(product_item),
                'Срок годности': self.parse_product_expiration(product_item),
                'Состав': self.parse_product_ingredients(product_item)
            }
            products.append(product)
        return products

# Пример использования:
if __name__ == '__main__':
    parser = ProductParser("https://mkgomel.by")
    products = parser.parse_products()
    print(products)
