import sqlite3

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq
from dispatcher import dp, bot
# from files.bot import kb
from DatabaseFunctions import select_by_id_db, select_by_id_db_full
import re


def sql_start():
    global base, cur
    base = sq.connect('database.db')
    if base:
        print('Database connected.')
        cur = base.cursor()


@dp.message_handler(lambda message: message.text == "Інформація")
async def show_paid_orders(message: types.Message):
    sql_start()
    # orders = [i[0] for i in ]
    orders = cur.execute(f"SELECT * FROM Ordering WHERE idProfile = "
                                                         f"{message.from_user.id} AND pay=true;").fetchall()
    if len(orders) == 0:
        await message.answer("⚙️⚙️⚙️⚠️ It is so empty here... ⚠️ ⚙️⚙️⚙️")
    else:
        for t in orders:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            sql = f"SELECT * FROM FullProduct WHERE idFull = {int(t[1])};"
            k = cursor.execute(sql).fetchall()
            i = select_by_id_db(k[0][1])
            await bot.send_photo(message.from_user.id, photo=i[5])
            await bot.send_message(message.from_user.id, f'{i[1]}\nDescription: {i[2]}\nPrice: {i[3]*t[4]} Color: {k[0][3]} Size: {k[0][2]} Count: {t[4]}')

