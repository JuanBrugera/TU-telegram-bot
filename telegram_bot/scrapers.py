import json
import sys

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from telegram_bot.objects import Product
from telegram_bot.regexs import *

HEADERS = {'user-agent': UserAgent().chrome}


class Base:
    def __init__(self, url, **kwargs):
        try:
            url_base, url_params = url.split("?")
        except:
            url_base, url_params = url, ''

        self.url = url_base
        self.params = dict([param.split("=") for param in url_params.split("&")]) if url_params else {}
        self.params.update(kwargs.get('tracking_params', {}))
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
    product_json = None

    def _set_product_json(self):
        if raw := self.soup.find('script', text=TU_PRODUCT_JSON_REGEX).contents.pop().strip():
            data = TU_PRODUCT_JSON_REGEX.search(raw).group(1)
            self.product_json = json.loads(data)

    @property
    def title(self):
        if title := self.product_json.get("title"):
            return title.strip()
        else:
            return self.soup.find('h1', {'class': 'product_title product-single__title'}).text.strip()

    @property
    def product_type(self):
        if t := self.product_json.get("type", None):
            return t.lower()

    @property
    def now_price(self):
        if price := self.product_json.get("price", None):
            return price / 100
        else:
            price = self.soup.find('ins', {'class': 'product_price'})
            price = price if price else self.soup.find('span', {'class': 'product_price'})
            return self.str_to_float(price.text)

    @property
    def before_price(self):
        if price := self.product_json.get("compare_at_price", None):
            return price / 100
        elif price := self.soup.find('del', {'class': 'compare_at_price'}):
            return self.str_to_float(price.text)

    @property
    def save(self):
        if save := self.soup.find('div', {'class': 'product__label label-sale'}):
            return self.str_to_float(save.text)
        elif self.before_price:
            return round(100 * (1 - self.now_price / self.before_price))

    @property
    def picture_url(self):
        if images := self.product_json.get("images", None):
            return 'https:' + images.pop(0)
        elif partial_url := self.soup.find('a', {
            'class': 'product-single__thumbnail product-single__thumbnail--product-template'}):
            return 'https:' + partial_url.get('href')

    @property
    def description(self):
        if desc := self.soup.find('div', {'class': 'bloque_info_producto descripcion'}):
            text = desc.text
            if matches := TU_PRODUCT_DESCRIPTION_UPPERS.findall(text):
                add_whitspace = lambda s: s.replace(".", ". ")
                for match in matches:
                    text = text.replace(match, add_whitspace(match))
            return text

    @property
    def features(self):
        if info := self.soup.find('div', {'class': TU_PRODUCT_INFO_REGEX}):
            return [f for s in info.find_all('figcaption') if
                    (f := s.text.strip().replace("\n", ", "))]

    @property
    def url_to_sent(self):
        if self.params:
            return self.url + "?" + '&'.join([f"{tag}={value}" for tag, value in self.params.items() if value])
        else:
            return self.url

    @property
    def stock(self):
        if stock := self.soup.find('div', {'data-stock': True}):
            return int(stock.get('data-stock'))
        else:
            return sys.maxsize

    @property
    def details(self):
        self._set_product_json()
        return Product(self.url,
                       self.url_to_sent,
                       self.title,
                       self.product_type,
                       self.now_price,
                       self.before_price,
                       self.save,
                       self.picture_url,
                       self.description,
                       self.features,
                       self.stock)
