import json


class Product:
    def __init__(self, origin_url, url_to_sent, title, product_type, now_price, before_price, save, picture_url,
                 description, features, stock):
        self.origin_url = origin_url
        self.url_to_sent = url_to_sent
        self.title = title
        self.product_type = product_type
        self.now_price = now_price
        self.before_price = before_price
        self.save = save
        self.picture_url = picture_url
        self.description = description
        self.features = features
        self.stock = stock

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)
