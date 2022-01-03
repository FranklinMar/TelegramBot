
class Product:
    def __init__(self, idProduct, name, description, price, sex, image, type):
        self.idProduct = idProduct
        self.name = name
        self.description = description
        self.price = price
        self.sex = sex
        self.image = image
        self.type = type

    @property
    def idProduct(self):
        return self.__idProduct

    @idProduct.setter
    def idProduct(self, value):
        self.__idProduct = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name=value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, value):
        self.__sex = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value


class Profile:
    def __init__(self, id, name, surname, patronymic, country, city, post, delivery, card, date, phone_number):
        pass


class FullProduct:
    def __init__(self, idFull, idProduct, size, color, count):
        pass

