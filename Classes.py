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
    def addProduct(self):
        pass

    def delProduct(self):
        pass

    def payProducts(self):
        pass


class Profile:
    def signIn(self):
        pass

    def changeData(self):
        pass


class Information:
    def addResponse(self):
        pass

    def viewResponses(self):
        pass

    def viewInformation(self):
        pass