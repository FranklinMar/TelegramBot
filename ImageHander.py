import sqlite3
import os
import io

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
        #ablob = input_file.read()
    #ablob = sum(i for i in input_file)
    ablob = bytes(abyte_array)
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
    sql = f"UPDATE Product SET image = '{sqlite3.Binary(ablob)}' WHERE idProduct = {1}"
    #sql = f"UPDATE Product SET idProduct = 1 WHERE idProduct = 3"
    connection.execute(sql)
    connection.commit()



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
    photo = io.BytesIO(bytes(ablob, encoding="raw_unicode_escape"))
    return photo


if __name__ == "__main__":
    insert_picture("database.db", "1.jpg")
