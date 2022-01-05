import sqlite3
import io
#import os


def insert_db(name, description=None, price=0, sex=None, image=None, types=None):
    if not name:
        raise TypeError("Not Null exception.")
    if not image:
        blob = None
    else:
        if not isinstance(image, str):
            raise TypeError("Image path is not 'str'.")
        byte_array = bytearray()
        with open(image, 'rb') as input_file:
            for i in input_file:
                byte_array += bytearray(i)
        blob = bytes(byte_array)

    connection = sqlite3.connect("database.db")
    sql = "INSERT INTO Product (name, description, price, sex, image, type) VALUES (?, ?, ?, ?, ?, ?);"
    connection.execute(sql, (name, description, price, sex, blob, types))
    connection.commit()


def select_by_id_db(ids):
    if not isinstance(ids, int):
        raise TypeError("Id is not 'int'.")
    if ids <= 0:
        raise ValueError("Id value negative.")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    sql = f"SELECT * FROM Product WHERE idProduct = {ids}"
    temp = [*cursor.execute(sql).fetchone()]
    if temp[5]:
        temp[5] = io.BufferedReader(io.BytesIO(temp[5]))
    return temp


def select_by_id_db_full(ids):
    if not isinstance(ids, int):
        raise TypeError("Id is not 'int'.")
    if ids <= 0:
        raise ValueError("Id value negative.")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    sql = f"SELECT * FROM FullProduct WHERE idFull = {ids}"
    temp = [*cursor.execute(sql).fetchone()]
    return temp


def extract_picture(database_path): #, picture_id):
    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()
    #sql = "SELECT PICTURE, TYPE, FILE_NAME FROM PICTURES WHERE id = :id"
    #param = {'id': picture_id}
    #cursor.execute(sql, param)
    #ablob, ext, afile = cursor.fetchone()
    #filename = afile + ext
    #with open(filename, 'wb') as output_file:
    #    output_file.write(ablob)
    # return filename
    sql = "SELECT image FROM Product WHERE idProduct = 1"
    temp = cursor.execute(sql)
    ablob = temp.fetchone()[0]#cursor.fetchone()[5]
    print(type(ablob).__name__)
    # bytes(ablob, encoding="raw_unicode_escape")
    # photo =
    return io.BufferedReader(io.BytesIO(ablob))

# def insert_picture(database_path, picture_file):
#     connection = sqlite3.connect(database_path)
#
#     cursor = connection.cursor()
#     abyte = bytearray()
#     with open(picture_file, 'rb') as input_file:
#         for i in input_file:
#             abyte
#         #ablob = input_file.read()
#         ablob = sum(i for i in input_file)
#         print(type(ablob).__name__)


def insert_picture(database_path, picture_file):
    connection = sqlite3.connect(database_path)

    # cursor = connection.cursor()
    abyte_array = bytearray()
    with open(picture_file, 'rb') as input_file:
        for i in input_file:
            abyte_array += bytearray(i)
    ablob = bytes(abyte_array)
    # with open(picture_file, 'rb') as input_file:
    #     ablob = input_file.read()
    #ablob = sum(i for i in input_file)
    with open(picture_file, 'rb') as input_file:
        print(type(input_file).__name__)
    # print(type(ablob).__name__)
    # base = os.path.basename(picture_file)
    # afile, ext = os.path.splitext(base) # ext - type (.jpg, .png, ...)
    # # afile - filename (photo, ...)
    # sql = '''INSERT INTO PICTURES
    # (PICTURE, TYPE, FILE_NAME)
    # VALUES(?, ?, ?);'''
    # connection.execute(sql, [sqlite3.Binary(ablob), ext, afile])
    # connection.commit()
    # sql = f"UPDATE Product SET image = '{sqlite3.Binary(ablob)}' WHERE idProduct = {1};"
    #sql = f"UPDATE Product SET idProduct = 1 WHERE idProduct = 3;"
    #sql = f"UPDATE Product SET image = '?' WHERE idProduct = 1;"
    sql = "INSERT INTO Product (idProduct, name, description, price, image, type) VALUES (?, ?, ?, ?, ?, ?);"
    connection.execute(sql, (1,"T-Shirt", 'T-Shirt with "Puma" label', 100, ablob, "Top"))
    connection.commit()


# if __name__ == "__main__":
#     insert_picture("database.db", "1.jpg")
#     extract_picture("database.db")


def ordering():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Ordering WHERE pay=false;")
    connection.commit()
    print(632562562)

if __name__ == "__main__":
    insert_db("Woman hoodie", "Beautiful oversize hoodie", 500, "Woman", "1.jpg", "Hoodies_woman")
    insert_db('Hoodie "dino"', "Hoodie with dino print", 600, "Woman", "2.jpg", "Hoodies_woman")