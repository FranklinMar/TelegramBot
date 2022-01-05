import asyncio
import sqlite3

import aioschedule


async def ordering():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    sql = f"SELECT * FROM Ordering WHERE pay=false;"
    order = cursor.execute(sql).fetchall()
    for i in order:
        s = f"SELECT idProduct FROM FullProduct WHERE idFull = {i[1]};"
        t = cursor.execute(s).fetchone()
        cursor.execute('INSERT INTO Basket (idProfile, idProduct) VALUES (?,?);', (i[2], t[0]))
        cursor.execute(f'UPDATE FullProduct SET count = count+{i[4]} WHERE idFull={i[1]};')
        connection.commit()
    cursor.execute(f"DELETE FROM Ordering WHERE pay=false;")
    connection.commit()
    print(632562562)


async def scheduler():
    aioschedule.every().day.at("00:01").do(ordering)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
