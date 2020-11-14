import json


class Product:
    def __init__(self, url, title, now_price, before_price, save, picture_url, description, features):
        self.url = url
        self.title = title
        self.now_price = now_price
        self.before_price = before_price
        self.save = save
        self.picture_url = picture_url
        self.description = description
        self.features = features

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)
