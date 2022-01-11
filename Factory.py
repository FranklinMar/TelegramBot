import sqlite3


class Factory:
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

