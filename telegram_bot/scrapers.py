import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from telegram_bot.objects import Product
import json

HEADERS = {'user-agent': UserAgent().chrome}


class Base:
    def __init__(self, url):
        self.url = url
        r = requests.get(url=url, headers=HEADERS)
        self.status = r.status_code
        self.soup = BeautifulSoup(r.content, 'lxml')

    def __str__(self):
        return json.dumps({'url': self.url, 'status': self.status}, indent=2)

    @staticmethod
    def str_to_float(s: str) -> float:
        if s:
            translations = {',': '.'}
            return float(''.join([c if c.isdigit() else translations.get(c, '') for c in s]))


class ProductScraper(Base):
    @property
    def title(self):
        return self.soup.find('h1', {'class': 'product_title product-single__title'}).text

    @property
    def now_price(self):
        return self.str_to_float(self.soup.find('ins', {'class': 'product_price'}).text)

    @property
    def before_price(self):
        return self.str_to_float(self.soup.find('del', {'class': 'compare_at_price'}).text)

    @property
    def save(self):
        return self.str_to_float(self.soup.find('div', {'class': 'product__label label-sale'}).text)

    @property
    def picture_url(self):
        if partial_url := self.soup.find('a', {
            'class': 'product-single__thumbnail product-single__thumbnail--product-template'}):
            return 'https:' + partial_url.get('href')

    @property
    def description(self):
        return self.soup.find('div', {'class': 'bloque_info_producto descripcion'}).text

    @property
    def features(self):
        return [f for s in self.soup.find('div', {'id': 'tab-description'}).find_all('figcaption') if
                (f := s.text.strip())]

    @property
    def details(self):
        return Product(self.url,
                       self.title,
                       self.now_price,
                       self.before_price,
                       self.save,
                       self.picture_url,
                       self.description,
                       self.features)
