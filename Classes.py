import geonamescache


class Product:
    def __init__(self, name, description, price, size, *args, **kwargs):
        self.idn = 0

        self.name = name
        self.description = description
        self.price = price
        self.size = size
        self.image_list = []


class Basket:
    def signIn(self, ):


    def addProduct(self, idn):
