import sqlite3
import io


class Factory:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, name_db):
        self.connector = sqlite3.connect(name_db)
        self.cursor = self.connector.cursor()

    def get_ordering(self, user_id, ind):
        order = self.cursor.execute(f"SELECT * FROM Ordering WHERE idProfile = "
                                    f"{user_id} AND pay={ind};").fetchall()
        return order

    def get_full_product(self, id_full):
        fulls = self.cursor.execute(f"SELECT * FROM FullProduct WHERE idFull = {id_full};").fetchall()
        return fulls

    def insert_db(self, name, description=None, price=0, sex=None, image=None, types=None):
        if not name:
            raise TypeError("Not Null exception.")
        if not image:
            blob = None
        if not isinstance(price, (int, float)):
            raise TypeError(f"'price' unsupported type of '{type(price).__name__}'.")
        if price < 0:
            raise ValueError(f"'price' unsupported value of '{price}'.")
        if not isinstance(sex, str):
            raise TypeError(f"'sex' unsupported type of '{type(sex).__name__}'.")
        if not isinstance(types, str):
            raise TypeError(f"'types' unsupported type of '{type(types).__name__}'.")
        else:
            if not isinstance(image, str):
                raise TypeError("Image path is not 'str'.")
            byte_array = bytearray()
            with open(image, 'rb') as input_file:
                for i in input_file:
                    byte_array += bytearray(i)
            blob = bytes(byte_array)
        sql = "INSERT INTO Product (name, description, price, sex, image, type) VALUES (?, ?, ?, ?, ?, ?);"
        self.connector.execute(sql, (name, description, price, sex, blob, types))
        self.connector.commit()

    def select_by_id_db(self, ids):
        if not isinstance(ids, int):
            raise TypeError("Id is not 'int'.")
        if ids <= 0:
            raise ValueError("Id value negative.")

        sql = f"SELECT * FROM Product WHERE idProduct = {ids}"
        temp = [*self.cursor.execute(sql).fetchone()]
        if temp[5]:
            temp[5] = io.BufferedReader(io.BytesIO(temp[5]))
        return temp
