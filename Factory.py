import sqlite3


class Factory:
    def __init__(self, name_db):
        self.connector = sqlite3.connect(name_db)
        self.cursor = self.connector.cursor()

